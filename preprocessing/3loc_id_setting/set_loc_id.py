import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import string
import os

import descartes
import geopandas as gpd
from shapely.geometry import Point, Polygon

from timeit import default_timer as timer
pd.options.display.max_rows = 5

dpath = '/Users/sai/Documents/00 NEU/Semester 1/1 DS 5110 - Introduction to Data Management and Processing/Project/NYC-Taxi-Data-Analysis/data_sampled/green/'
shp_path = '/Users/sai/Documents/00 NEU/Semester 1/1 DS 5110 - Introduction to Data Management and Processing/Project/NYC-Taxi-Data-Analysis/taxi_zones/'
curr_dir = os.getcwd()
fname = 'tripdata_green_samp.csv'

green = pd.read_csv(dpath + fname)

N = green.shape[0]
rperm = np.random.permutation(N)

# Hard limits
lon_min = -74.3
lon_max = -73.6

lat_min = 40.4
lat_max = 41.0

# Basemap
base_map = gpd.read_file(shp_path + 'taxi_zones.shp')
base_map = base_map.to_crs({'init': 'epsg:4326'})

# Setting up (for loop)
n_subs = 10
index_splits = np.array_split(rperm, n_subs)

# Utility functions
# ---------------------------

# Get location id from lon-lat pair
geometries = base_map.geometry.values


def assign_locid2(lon, lat):
    point = Point(lon, lat)

    for idx, geometry in enumerate(geometries):
        if geometry.contains(point):
            return(idx + 1)
    return(9999)

# Print during the start of an iteration in loop


def print_curr_subset(i_sub, n_subs):
    print("\n\n#####")
    print("Processing subset {0} / {1}".format(i_sub + 1, n_subs))

# Print after the iteration


def print_end_of_subset(N, count, n, start_, s_):
    print("\nProcessing ...DONE")
    e_ = timer()
    print("Time taken for {0:.3f}M observations: {1:.3f}".format(n / 1e+6, e_ - s_))
    print("Time taken until from start of loop: {:.3f}".format(e_ - start_))
    print("Total progress: {:.2f}".format(count / N))
    print("#####")


# For time complexity analysis
durations = np.zeros(n_subs)
lengths = [len(array) for array in index_splits]

# The loop
count = 0

PULOCID = np.zeros(N)
DOLOCID = np.zeros(N)

start_ = timer()

for i_sub in range(n_subs):
    s_ = timer()

    subset = green.iloc[index_splits[i_sub], :]
    n = subset.shape[0]
    print_curr_subset(i_sub, n_subs)

    pulocid = np.zeros(n).astype(int)
    dolocid = np.zeros(n).astype(int)

    pulon = subset.pickup_longitude.values
    pulat = subset.pickup_latitude.values

    dolon = subset.dropoff_longitude.values
    dolat = subset.dropoff_latitude.values

    pulocationid = subset.pulocationid.values
    dolocationid = subset.dolocationid.values

    for i in range(n):
        if not np.isnan(pulon[i]):
            pulocid[i] = assign_locid2(pulon[i], pulat[i])
            dolocid[i] = assign_locid2(dolon[i], dolat[i])
        else:
            pulocid[i] = pulocationid[i]
            dolocid[i] = dolocationid[i]

    PULOCID[count:count + n] = pulocid
    DOLOCID[count:count + n] = dolocid

    count = count + n
    durations[i_sub] = timer() - s_

    print_end_of_subset(N, count, n, start_, s_)

# Permutate the index (and df) to match the evaluated ??LOCIDs
green_perm = green.iloc[rperm, :]

# Replace the ??LOCID in the dataframe
green_perm.loc[:, 'pulocationid'] = PULOCID
green_perm.loc[:, 'dolocationid'] = DOLOCID

# Write to a file
green_perm.to_csv(dpath + 'green_samp_locid.csv', index=False)
