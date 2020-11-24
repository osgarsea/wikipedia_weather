__author___ = "Oscar Garcia"
__version__ = "1.0.0"
__copyright__ = "Copyright (c) 2020 - 2021 Oscar Garcia-Costa"
__file__ = 'wikipedia_scrapping.py'


"""
Created on Wed Nov 13 18:02:32 2019

@author: costao1
"""

import wikipedia_scrapping_functions as wsf


# cities_climate, cities_without_page, cities_with_errors, cities_without_table, all_headers, cities = wsf.extract_all_climate_data ()
# wsf.export_data(all_headers, cities_climate)




import pandas as pd
# from wikipedia_scrapping_parameters import wiki_cities_100k_url, csvs_folder




cities_climate = wsf.import_and_reformat_climate_table()


# cities_climate['rnk_asc'] = cities_climate.groupby(['City', 'Measure'])['Value'].rank(method = 'first', ascending=True)


cities_climate['rnk_asc'] = cities_climate.loc[cities_climate['Month'] != 'Annual']\
    .groupby(['City', 'Measure'])[['Value', 'Month_id']].rank(method = 'first', ascending=True)
cities_climate['rnk_desc'] = cities_climate.loc[cities_climate['Month'] != 'Annual']\
    .groupby(['City', 'Measure'])[['Value', 'Month_id']].rank(method = 'first', ascending=False)


cities_climate.loc[cities_climate['rnk_desc']<= 3]\
    .groupby(['City', 'Measure'])['Value'].mean()
    



conditions = {
    'Sun hours' : ['Annual', 'Mean monthly sunshine hours', [1800, 3000]],
    'Max summer' : ['Top 3', 'Average high (°C)', [22, 28]],
    'Min summer' : ['Bottom 3', 'Average low (°C)', [-2, 6]]
    
    }

import statistics
l = [22, 29]
statistics.mean(l)


for key, value in conditions.items():
    print(key)
    print(value)
    
a = ((cities_climate['Month'] == 'Annual') &
     (cities_climate['Measure'] == 'Mean monthly sunshine hours') &
     (cities_climate['Value'] >= 1800) &
     (cities_climate['Value'] <= 3000) )
                   
b = ((cities_climate['Month'] == 'Annual') &
     (cities_climate['Measure'] == 'Mean monthly sunshine hours') &
     (cities_climate['Value'] >= 1800) &
     (cities_climate['Value'] <= 3000) )


statistics.mean(conditions['Sun hours'][2])
                   
selected_cities = cities_climate.loc[a].copy()
selected_cities['Dif'] = selected_cities['Value'] - statistics.mean(conditions['Sun hours'][2])

                   \
    .groupby(['City', 'Measure'])['Value'].mean()