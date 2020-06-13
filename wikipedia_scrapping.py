# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 18:02:32 2019

@author: costao1


Additional info:
    
https://realpython.com/python-requests/
https://www.crummy.com/software/BeautifulSoup/
https://medium.com/analytics-vidhya/web-scraping-wiki-tables-using-beautifulsoup-and-python-6b9ea26d8722

"""

import sys, os
sys.path.append('C:\Personal_GIT_repositories\wikipedia_weather')


from bs4 import BeautifulSoup as bs
import csv
import itertools
from operator import itemgetter
import pandas as pd
import requests
import string
import unicodedata as ud 


# My libraries
import wikipedia_scrapping_functions as wsf




wiki_cities_100k_url = 'https://en.wikipedia.org/wiki/List_of_towns_and_cities_with_100,000_or_more_inhabitants/cityname:_'

cities_without_page = []
cities_without_table = []
all_headers = {}#set([])


cities = wsf.import_cities (wiki_cities_100k_url)



#df_col_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Annual']
##df_idx_names = ['City', 'Measure']
#cities_climate = pd.DataFrame( columns=df_col_names)


cities_sample = dict(itertools.islice(cities.items(), 0, 4))

cities_sample = {key: cities[key] for key in cities.keys() 
                               & {  'Abakan'}} 

print(cities_sample)
#key = 'İstanbul'
#cities_sample = cities[key]

i = 0
# Loop through the dictionary entries and retrieve the Wikipedia climate webpage for that city
for key in cities.keys():
    i +=1
    print("----------------------------------------------------")
    print(key)
    print('PROCESSING: {}'.format(key.upper()))
    print('City number {0}'.format(i))
    
    # Extract the link for the city climate webpage
    link = cities[key][1] + '#Climate'
    print('{}\n'.format(link))
    
    
    # Get the webpage as text
    webpage_climate = requests.get(link).text
    
    cities_without_page = wsf.check_if_page_exists (webpage_climate, cities_without_page, key)
    
    # Read the webpage with Beautiful Soup so we can work with it
    soup = bs(webpage_climate,'lxml')

    # Extract the whole table from the webpage
    climate_table = wsf.extract_table(soup, cities_without_table, key)
    
    if climate_table is None:
        continue
    else:
        record, city_climate_df, all_headers = wsf.extract_climate_data (climate_table, key, all_headers)

  
    if i == 1:
        cities_climate = city_climate_df.copy(deep = True)
    else:
        cities_climate = cities_climate.append(city_climate_df)#, verify_integrity = True)
    print(city_climate_df)

#print(cities_climate)
#print(all_headers)


#for key in cities.keys():
#    
#    if 'bul' in cities[key][1]:
#        print(key)
#        print(cities[key])
#        exit
#    print(key)
#print('done')


csv_file = 'outputs/all_headers.csv'
csv_columns = ['city', 'values_all']


with open(csv_file, 'w', encoding="utf-8") as f:
    for key in all_headers.keys():
        f.write("\"{0}\"\t{1}\t\"{2}\"\n".format(key,all_headers[key][0], all_headers[key][1]))



# ==============================================================================
# ==============================================================================
# ==============================================================================
# ==============================================================================



"""

# Read the webpage with Beautiful Soup so we can work with it
soup = bs(webpage_climate,'lxml')

# Extract the whole table from the webpage
climate_table = wsf.extract_table(soup, cities_without_table, key)

#def extract_climate_data (climate_table, key, all_headers):
all_values = []

for record in climate_table.find_all('tr')[2:-1]: # Extract each record of the table
    
#        print('------')
    # Get header and the unit I should choose
    values, unit_pos, all_headers = get_headers(record, all_headers, key)
    
    # Get all the values in each record
    values = get_column_values(record, values, unit_pos)
    
    # Put all the values for the city in the same list of list
    all_values.append(values)
    
    city_climate_df = data_to_dataframe(all_values, key)
    
    values = []

print(climate_table)
"""