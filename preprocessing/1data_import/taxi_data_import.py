from urllib.request import urlopen
from bs4 import BeautifulSoup as BS
import webbrowser

import pandas as pd
import os

import requests

source_url = "https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page"
page = urlopen(source_url)
soup = BS(page)

all_links = soup.find_all(name='a')

relevant_links = [str(link.get('href')) for link in all_links
                  if ('green_trip' in str(link))]
# [print(link) for link in relevant_links]

# prettyHTML = soup.prettify()
# print(prettyHTML)

# DO NOT RUN THIS! VERY COMPUTATIONALLY HEAVY!
i = 0
for url in relevant_links:
    total = len(relevant_links)
    fname = url.split('/')[-1]

    print('\n################################\n')
    print('FILE {0} OF {1}'.format(i + 1, total))
    print('\nDownloading csv from:', url)

    r = requests.get(url)

    with open('/Users/sai/Downloads/' + fname, 'wb') as file:
        file.write(r.content)

    csv_data = pd.read_csv('~/Downloads/' + fname)
    sample_df = csv_data.sample(frac=0.1, random_state=0)
    sample_df.to_csv(os.getcwd() + '/sampled_data/green/' + fname, index=False)
    os.remove('/Users/sai/Downloads/' + fname)
    print('\nProcessing ' + fname + ' ...DONE')
    print('\n################################\n')

    i = i + 1

    if i == 2:
        break
