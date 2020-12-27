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




# import pandas as pd
# import numpy as np
# # from wikipedia_scrapping_parameters import wiki_cities_100k_url, csvs_folder

# import statistics



cities_climate, cities_list = wsf.import_and_reformat_climate_table()



cities_list = wsf.flag_conditions (cities_climate, cities_list)

