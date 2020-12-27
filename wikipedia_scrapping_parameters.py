__author___ = "Oscar Garcia"
__version__ = "1.0.0"
__copyright__ = "Copyright (c) 2020 - 2021 Oscar Garcia-Costa"
__file__ = 'wikipedia_scrapping_parameters.py'

"""
Created on Tue Nov 17 06:43:03 2020

@author: costao1
"""


wiki_cities_100k_url = 'https://en.wikipedia.org/wiki/List_of_towns_and_cities_with_100,000_or_more_inhabitants/cityname:_'
csvs_folder = 'outputs'


conditions = {
    'Sun hours' : ['Annual', 'Mean monthly sunshine hours', [1800, 3000]],
    'Max summer' : ['Top 3', 'Average high (°C)', [22, 28]],
    'Min winter' : ['Bottom 3', 'Average low (°C)', [-2, 6]]
    
    }