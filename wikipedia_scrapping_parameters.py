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

# Oscar
# conditions = {
#     'Sun hours' : ['Annual', 'Mean monthly sunshine hours', [2200, 3000], [1600, 3800]],
#     'Max summer' : ['Top 3', 'Average high (°C)', [25, 28], [20, 35]],
#     'Max winter' : ['Bottom 3', 'Average high (°C)', [5, 10], [-2, 20]],
#     # 'Min winter' : ['Bottom 3', 'Average low (°C)', [-2, 10], [-5, 20]],
#     'Rainy days' : ['Annual', 'Average rainy days', [50, 120], [40, 200]],
#     'Total rain' : ['Annual', 'Average precipitation (mm)', [600, 1200], [300, 2000]],
#     'Hummidity' : ['Annual', 'Average relative humidity (%)', [40, 60], [0, 80]]
#     }

conditions = {
    'Sun hours' : ['Annual', 'Mean monthly sunshine hours', [2100, 2500], [1600, 3800]],
    'Max summer' : ['Top 3', 'Average high (°C)', [25, 30], [20, 35]],
    'Max winter' : ['Bottom 3', 'Average high (°C)', [10, 15], [-2, 20]],
    # 'Min winter' : ['Bottom 3', 'Average low (°C)', [-2, 10], [-5, 20]],
    'Rainy days' : ['Annual', 'Average rainy days', [80, 160], [40, 200]],
    # 'Total rain' : ['Annual', 'Average precipitation (mm)', [600, 1200], [300, 2000]],
    # 'Hummidity' : ['Annual', 'Average relative humidity (%)', [40, 60], [0, 80]]
    }


# Add no less and no more than