import numpy as np
import pandas as pd
import string
import os
from timeit import default_timer as timer

# Setting paths
dpath = '/Users/sai/Documents/00 NEU/Semester 1/1 DS 5110 - Introduction to Data Management and Processing/Project/NYC-Taxi-Data-Analysis/data_sampled/green/'
curr_dir = os.getcwd()

# Getting datafile names
csv_fnames = list(os.walk(dpath))[0][2]

# Initializing concatenated dataframe and timers
stime = timer()
concat_df = pd.read_csv(dpath + csv_fnames[0])
concat_df.columns = [col.lower().strip() for col in concat_df.columns]

concat_dur = [timer() - stime]
concat_obs = [concat_df.shape[0]]

for idx, fname in enumerate(csv_fnames[1:]):
    print("\n------")
    print("File {0} of {1}".format(idx + 2, len(csv_fnames)))
    print("BEFORE CONCAT: Line count: {}".format(concat_df.shape[0]))

    stime_ = timer()

    curr_df = pd.read_csv(dpath + fname)
    curr_df.columns = [col.lower().strip() for col in curr_df.columns]
    concat_df = pd.concat([concat_df, curr_df], axis=0, ignore_index=True, sort=True)

    etime_ = timer()
    concat_dur.append(etime_ - stime_)
    concat_obs.append(curr_df.shape[0])

    print("AFTER CONCAT: Line count: {}".format(concat_df.shape[0]))
    print("Time elapsed: {0:.3f}".format(etime_ - stime_))
    print("Observations added:", str(curr_df.shape[0]))
    print("------\n")


print("TOTAL TIME OF CONCATENATION: {0:.3f}".format(timer() - stime))

# Write data to .csv
concat_df.to_csv(dpath + 'tripdata_green_samp', index=False)
