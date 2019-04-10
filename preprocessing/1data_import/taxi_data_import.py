from urllib.request import urlopen
from bs4 import BeautifulSoup as BS
import webbrowser
import string

import pandas as pd
import os

import requests

source_url = "https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page"
page = urlopen(source_url)
soup = BS(page)

all_links = soup.find_all(name='a')

# Download filters
year_ = 2013
taxi_type_ = 'yellow'
filter_ = taxi_type_ + '_tripdata_' + str(year_)

# No filter: download all
filter_ = taxi_type_ + '_tripdata_'

relevant_links = [str(link.get('href')) for link in all_links
                  if (filter_ in str(link))]
# [print(link) for link in relevant_links]

# prettyHTML = soup.prettify()
# print(prettyHTML)

# DO NOT RUN THIS! VERY COMPUTATIONALLY HEAVY!
count = 0
fpath = '/Users/sai/Downloads/'
for url in relevant_links:
    total = len(relevant_links)

    fname = url.split('/')[-1]

    print('\n################################\n')
    print('FILE {0} OF {1}'.format(count + 1, total))
    print('\nDownloading csv from:', url)
    print(fname + '\n')

    r = requests.get(url)

    # Download the .csv file
    with open(fpath + fname, 'wb') as file:
        file.write(r.content)

    # Read in the .csv and sample
    with open(fpath + fname, 'r') as file:
        header = file.readline()
        first_line = file.readline()

        while first_line.isspace():
            first_line = file.readline()

    n_header = len(header.split(','))
    n_first = len(first_line.split(','))
    n_commas = n_first - n_header

    colnames = header.split(',')
    colnames[-1] = colnames[-1][:-1]

    colnames_buffer = list(string.ascii_uppercase)

    for i in range(n_commas):
        colnames.append(colnames_buffer.pop(0))

    cols_to_drop = list(set(list(string.ascii_uppercase)) - set(colnames_buffer))

    csv_data = pd.read_csv(fpath + fname, skiprows=1,
                           header=None, names=colnames)
    csv_data = csv_data.drop(cols_to_drop, axis=1)
    sample_df = csv_data.sample(frac=0.1, random_state=0)

    # Write data to .csv
    sample_df.to_csv(os.getcwd() + '/sampled_data/' + taxi_type_ + '/' + fname, index=False)

    # Remove original file
    os.remove('/Users/sai/Downloads/' + fname)
    print('\nProcessing ' + fname + ' ...DONE')
    print('\n################################\n')

    count = count + 1
