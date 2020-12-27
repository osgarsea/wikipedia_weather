__author___ = "Oscar Garcia"
__version__ = "1.0.0"
__copyright__ = "Copyright (c) 2020 - 2021 Oscar Garcia-Costa"
__file__ = 'wikipedia_scrapping_functions.py'


"""
Created on Thu Nov 14 07:07:43 2019

@author: costao1

Additional info:
    
https://realpython.com/python-requests/
https://www.crummy.com/software/BeautifulSoup/
https://medium.com/analytics-vidhya/web-scraping-wiki-tables-using-beautifulsoup-and-python-6b9ea26d8722

"""


import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import string
from operator import itemgetter
# import unicodedata as ud 
import datetime
import numpy as np
import statistics

from wikipedia_scrapping_parameters import wiki_cities_100k_url, csvs_folder, conditions

def import_cities (wiki_cities_100k_url):
    """
    This functions loops through all the wikipedia pages with the list of
    the towns and cities over 100k people and extracts the link to the wikipedia
    webpage
    
    - Parameters:
        wiki_cities_100k_url (str): URL with the url to the wiki pages (without letter)
    - Returns:
        cities (dic): dictionary with the name of the cities and the URL to the
                      webpage and also the country name and wiki url
    """
    
    # https://realpython.com/python-requests/
    # https://www.crummy.com/software/BeautifulSoup/
    
    # https://medium.com/analytics-vidhya/web-scraping-wiki-tables-using-beautifulsoup-and-python-6b9ea26d8722
    
    
    start_time = datetime.datetime.now()
    print_start('Exporting climate data for cities', start_time)
    
    # Empty dictionary to store all the cities and the Wikipedia links
    cities = {}
    
    # Loop through all the lists in the alphabet
    for letter in string.ascii_uppercase:
        
        # Get the webpage as text
        webpage_cities = requests.get(wiki_cities_100k_url + letter).text
        
        # Read the webpage with Beautiful Soup so we can work with it
        soup = bs(webpage_cities,'lxml')
        
        # Extract the table where the list of cities is
        cities_table = soup.find('table',{'class':'wikitable sortable'})
        
        # Extract each record of the table
        cities_records = cities_table.find_all('td')
        
        # Loop through all the records to copy the city name and link in the dictionary
        i = 1
        for record in cities_records:
            # Loop through all the links
            for cell in record.find_all('a'):            
                # Check if it's the odd record
                if i%2 != 0:
                    # Extract the city data
                    city_name = cell.get('title')
                    city_link = 'https://en.wikipedia.org{0}'.format(cell.get('href'))
                    city_list = [None, city_link, None]
                    cities.update({city_name: city_list})
            
                # If it's the even record then...
                else:
                    # Extract the country data
                    country_name = cell.get('title')
                    country_link = 'https://en.wikipedia.org{0}'.format(cell.get('href'))
                    city_list = [country_name, city_link, country_link]
                    cities.update({city_name: city_list})            
            i+=1
    
    print_last(start_time)
    
    return cities



def extract_table (soup, cities_without_table, key):
    """
    Extracts the table where the list of cities is,
    it considers the different tags that are used to define the table
    
    - Parameters:
        soup (Beautiful Soup): html webpage extracted using Beautiful Soup
     - Return:
         climate_table (str): text file with the table data in HTML format
    """
    
    # print_start('extract_table')
    
    if soup.find('table',{'class':'wikitable collapsible'}) is not None:
        climate_table = soup.find('table',{'class':'wikitable collapsible'})
    elif soup.find('table',{'class':'wikitable collapsible collapsed'}) is not None:
        climate_table = soup.find('table',{'class':'wikitable collapsible collapsed'})
    else:
        climate_table = None
        cities_without_table.append(key)
        print('Table not found in {}'.format(key))
#        continue
    
    return climate_table

# https://stackoverflow.com/questions/16036913/minimum-of-list-of-lists


#  I need to pass the information whether to choose the first value or the l
# https://stackoverflow.com/questions/16036913/minimum-of-list-of-lists


#  I need to pass the information whether to choose the first value or the l
def unit_position(text):
    """
    
    Return:
    - selected_units (list): list in the format [units, rank priority, position, multiplier]
    """
    
    units_list = [
                  ['°C'     , 1, text.find('°C')     , lambda a : a            ],
                  ['°F'     , 2, text.find('°F')     , lambda a : (a - 32)*5/9 ],
                  ['mm'     , 1, text.find('mm')     , lambda a : a            ],
                  ['cm'     , 2, text.find('cm')     , lambda a : a*10         ], # This could be change so when talking about snow it is measured in cm rather than mm
                  ['inches' , 3, text.find('inches') , lambda a : a*25.4       ],
                  ['daily sunshine hours', 1, text.find('daily sunshine hours'), lambda a : a*365/12] # This one will need to be improved so it can be multiplied by the exact number of days for each month
                 ]
     
    
    if len(list((x for x in units_list if x[2] != -1))) > 0:
        gen = (x for x in units_list if x[2] != -1)
        selected_units = min(gen,key=itemgetter(1))
        
        gen2 = (x for x in units_list if x[2] != -1)
        first_units = min(gen2,key=itemgetter(2))

        if first_units[0] == selected_units[0]:
            selected_units.append(0)
        else:
            selected_units.append(1)
#        print(selected_units)
    else:
        selected_units = [None,None,None,lambda a : a,0]
    
    return selected_units




def new_record_title (header_text):
    """
    As the tables might have slightly different record names,
    this module transforms the title of the record in a standrad one
    
    - Parameters:
        header_text: record name extracted from the Wikipedia table
    - Returns
        record title: The final standard record name
    """
    
    # print_start('new_record_title')
    
    names = {
            'record high humidex'         : 'Record high humidex (°C)',
            'record high'                 : 'Record high (°C)',
            'mean maximum'                : 'Mean maximum (°C)',
            'average high'                : 'Average high (°C)',
            'daily mean'                  : 'Daily mean (°C)',
            'average low'                 : 'Average low (°C)',
            'mean minimum'                : 'Mean minimum (°C)',
            'record low wind chill'       : 'Record low wind chill (°C)',
            'record low'                  : 'Record low (°C)',
            'average precipitation mm'    : 'Average precipitation (mm)',
            'average precipitation cm'    : 'Average precipitation (mm)',
            'average rainfall'            : 'Average precipitation (mm)',
            'average precipitation inches': 'Average precipitation (mm)',
            'average precipitation days'  : 'Average rainy days',
            'average rainy days'          : 'Average rainy days',
            'average snowy days'          : 'Average snowy days',
            'average snowfall'            : 'Average snowfall (mm)',
            'relative humidity'           : 'Average relative humidity (%)',
            'monthly sunshine hours'      : 'Mean monthly sunshine hours',
            'daily sunshine hours'        : 'Mean daily sunshine hours',
            'percent possible sunshine'   : 'Percent possible sunshine',
            'average ultraviolet index'   : 'Average ultraviolet index',
            'average dew point'           : 'Average dew point (°C)',
            'mean daily daylight hours'   : 'Mean daily daylight hours'
            }

    for key in names.keys():
        if key in header_text.lower():
            record_title = names[key]
            break
    else:
        record_title = header_text
    
    return record_title



def format_climate_table (all_values, key):
    """
    Converts the list with the table data
    in a dataframe in the correct format
    
    - Parameters:
        all_values: values extracted from the table without reformating
        key: the city name
    - Return
        df (DataFrame): the climate table as a dataframe in the correct format
    """
    
    # print_start('format_climate_table')
    
    # Convert the list to a dataframe
    df = pd.DataFrame(all_values)
    
    # Format the table as desired
    df.dropna(how = 'all', inplace = True)              # Drop records with no data
    df.rename(columns = df.iloc[0], inplace = True)    # Assign the first record as column name
    df.drop(labels = 1, axis = 0, inplace = True)      # Drop the first record
    df['City'] = key                                   # Add the city name in a column
    df.rename(columns = {'Month': 'Climate_data'}, inplace = True)   # Rename the 'Month' column
    df.set_index(['City', 'Climate_data'], inplace = True)           # Create the index
    
    return df


def check_if_page_exists (webpage_climate, cities_without_page, key):
    """
    Function to check whether the imported wikipedia page exists or not
    
    - Parameters:
        webpage_climate (str): previously downloaded wbpage
        cities_without_page (list): list to copy all the cities that don't
                                    have Wikipedia page
    - Return:
        cities_withour_page (list): updated list
    """
    
    
    if 'Wikipedia does not have an article with this exact name' in webpage_climate:
        print('Article not found in ', key)
        cities_without_page.append(key)
        
    return cities_without_page


def get_headers(record, all_headers, key):
    """
    Extract the header of one record and copy it in a list
    
    - Prameters:
        record (bs4 object): data for one record
        
    - Return:
        values (list): list where the header is copied    
            selected_units (list): list with the information to select/transform
                                   the values extracted from the table
    """
    
    def insert_header_value(all_headers, orig_header_text, key):
        """
        Updates the all_headers dictionary, adding a new header used or
        incrementing the existing ones
        
        - Parameters:
            all_headers (dictionary): dictionary with the headers information
            orig_header_text (str): name of the new header to evaluate
            key (str): Name of the city
            
        - Return:
            all_headers (dic): updated dictionary with the updated information
        """
    
        if orig_header_text in all_headers:#.keys():
            all_headers[orig_header_text][0] += 1
            all_headers[orig_header_text][1].append(key)
        else:
            all_headers.update( {orig_header_text : [1,[key]]} )
    
        return all_headers
    
    
    # print_start('get_headers')
    
    values = []
    
    if len(record.find_all('th')) == 1:
        header = record.find_all('th')[0]
        
        orig_header_text = header.get_text().replace('\n', '')
        # print(orig_header_text)
        
        all_headers = insert_header_value(all_headers, orig_header_text, key)
        #all_headers.add(orig_header_text)
        
        selected_units = unit_position(orig_header_text)
        header_text = new_record_title(orig_header_text)
        
#        print('{0} in process'.format(header_text))
        # print(selected_units)
        values.append(header_text)
    elif len(record.find_all('th')) == 0:
        selected_units = [None,None,None,None,0]
        print('This record had no header')
    else:
        print('This record has multiple headers')
    
    return values, selected_units, all_headers
  
    
def get_column_values(record, values, selected_units):
    """
    Loop through all the columns in one record to extract all the values
    Copy the values in a list
    
    - Prameters:
        record (bs4 object): data for one record
        values (list): list where the data is copied (it already has the header value)
        selected_units (list):
        
    - Return:
        values (list): completed list with all the values of one record including the header
    """
    
    # print_start('get_column_values')
    
    for col in record.find_all('td'):
#
#        # Extract the text of each cell, replace some characters, split by the new character
#        # and get the first (or second) value depending on the temperature units
        
#        https://stackoverflow.com/questions/45269652/python-convert-string-to-float-error-with-negative-numbers
        # print('______________________________')
        # print(col)
        cell_text = col.get_text()\
                .replace('—', '0(0)').replace('trace', '0(0)')\
                .replace('(','_').replace(')', '').replace('\n', '')\
                .replace(',', '').replace('\U00002013', '—')\
                .split('_')[selected_units[4]]
        cell_text = cell_text.translate({0x2c: '.', 0xa0: None, 0x2212: '-'})
        # print('##{}##'.format(cell_text))
        # print(*map(ud.name, cell_text), sep=', ')
        
        try:
            values.append(selected_units[3](float(cell_text)))
        except:
            values.append(None)
        
#    selected_units[3](value[selected_units[4]])
#    print ('Values extracted')
    return values


  
def data_to_dataframe(all_values, key):
    """
    Create a dataframe with the climate data for the city from the list
    Reformat the dataframe
    
    - Parameters:
        all_values (list): list of lists with the climate data for the city
        key (str): name of the city in this loop
    
    - Return:
        df (dataframe): formatted dataframe with the climate values for the city
    """
    
    # print_start('data_to_dataframe')
    
    fields_dict = {0  : 'Measure',
                   1  : 'Jan',
                   2  : 'Feb',
                   3  : 'Mar',
                   4  : 'Apr',
                   5  : 'May',
                   6  : 'Jun',
                   7  : 'Jul',
                   8  : 'Aug',
                   9  : 'Sep',
                   10 : 'Oct',
                   11 : 'Nov',
                   12 : 'Dec',
                   13 : 'Annual'
                  }
    
    df = pd.DataFrame(all_values)
    df.dropna(how = 'any',inplace = True)
    df.rename( columns = fields_dict, inplace = True)
    df['City'] = key         
    df.set_index(['City', 'Measure'], inplace = True)
    
    return df    


def extract_climate_data (climate_table, key, all_headers):
    
    # print_start('extract_climate_data')
    
    all_values = []
    
    for record in climate_table.find_all('tr')[2:-1]: # Extract each record of the table
        
        # print('=====================================')
        # print(record)
        # Get header and the unit I should choose
        values, selected_units, all_headers = get_headers(record, all_headers, key)
        
        # Get all the values in each record
        values = get_column_values(record, values, selected_units)
        
        # Put all the values for the city in the same list of list
        all_values.append(values)
        
        city_climate_df = data_to_dataframe(all_values, key)
        
        values = []
    
    return record, city_climate_df, all_headers
  
    

def export_data (all_headers, cities_climate):
    
    # Extract all headers table
    with open('{}\\all_headers.csv'.format(csvs_folder), 'w', encoding="utf-8") as f:
        for key in all_headers.keys():
            f.write("\"{0}\"\t{1}\t\"{2}\"\n".format(key,all_headers[key][0], all_headers[key][1]))
            # f.write("\"{0}\",{1},\"{2}\"\n".format(key,all_headers[key][0], all_headers[key][1]))
    print('All headers exported to CSV\n')
    
    # Extract the climate table
    cities_climate.to_csv('{}\cities_climate.csv'.format(csvs_folder), encoding = 'utf-8')
    print('Cities climate exported to CSV\n')
    
    
def extract_all_climate_data ():
    
    cities_without_page = []
    cities_with_errors = []
    cities_without_table = []
    all_headers = {}
    
    cities = import_cities (wiki_cities_100k_url)
    num_cities = len(cities.keys())
    
    start_time = datetime.datetime.now()
    print_start('Exporting climate data for cities', start_time)
    
    
    # cities_sample = dict(itertools.islice(cities.items(), 0, 4))
    # cities_sample = {key: cities[key] for key in cities.keys() 
    #                                & {  'Abakan'}} 
    #key = 'İstanbul'
    #cities_sample = cities[key]
    
    i = 0
    # Loop through the dictionary entries and retrieve the Wikipedia climate webpage for that city
    for key in cities.keys():
        i +=1
        
        
        
        start_time_all = datetime.datetime.now()
        print_start(key, start_time_all)
        
        print('City number {0}/{1}'.format(i, num_cities))
        
        # Extract the link for the city climate webpage
        link = cities[key][1] + '#Climate'
        print('{}\n'.format(link))
        
        
        # Get the webpage as text
        try:
            webpage_climate = requests.get(link).text
        except:
            cities_with_errors.append(key)
            print("City page doesn't exist\n")
        
        cities_without_page = check_if_page_exists (webpage_climate, cities_without_page, key)
        
        # Read the webpage with Beautiful Soup so we can work with it
        soup = bs(webpage_climate,'lxml')
    
        # Extract the whole table from the webpage
        climate_table = extract_table(soup, cities_without_table, key)
        
        # Extract climate data for each city
        if climate_table is None:
            continue
        else:
            try:
                record, city_climate_df, all_headers = extract_climate_data (climate_table, key, all_headers)
                if i == 1:
                    cities_climate = city_climate_df.copy(deep = True)
                else:
                    cities_climate = cities_climate.append(city_climate_df)#, verify_integrity = True)
                print(city_climate_df)
            except:
                cities_with_errors.append(key)
                print("This city threw and error\n")
                
        print_time(start_time_all)
    
    
    print_last(start_time)
    
    return cities_climate, cities_without_page, cities_with_errors, cities_without_table, all_headers, cities



def import_and_reformat_climate_table ():
    
    def add_ranks (climate):
    
        # Add ascending and descending rank to each category
        climate['rnk_asc'] = climate.loc[climate['Month'] != 'Annual']\
            .groupby(['City', 'Measure'])['Value'].rank(method = 'first', ascending=True)
        climate['rnk_desc'] = climate.loc[climate['Month'] != 'Annual']\
            .groupby(['City', 'Measure'])['Value'].rank(method = 'first', ascending=False).fillna(99)
        
        climate['rnk_asc'] = climate['rnk_asc'].fillna(99)
        climate['rnk_desc'] = climate['rnk_desc'].fillna(99)
        
        return climate

    # Import climate data
    cities_climate = pd.read_csv('{}\cities_climate.csv'.format(csvs_folder), encoding = 'utf-8')
    
    # Create DF with month_id
    fields_dict = {'Jan'    : 1,
                   'Feb'    : 2,
                   'Mar'    : 3,
                   'Apr'    : 4,
                   'May'    : 5,
                   'Jun'    : 6,
                   'Jul'    : 7,
                   'Aug'    : 8,
                   'Sep'    : 9,
                   'Oct'    : 10,
                   'Nov'    : 11,
                   'Dec'    : 12,
                   'Annual' : 13
                  }
    fields_names = pd.DataFrame.from_dict(fields_dict, orient = 'index', columns = ['Month_id'])
            
    
    # Unpivot the climate table
    climate_melted = pd.melt(cities_climate,
                             id_vars = ['City', 'Measure'],
                             var_name = 'Month',
                             value_name = 'Value')
    
    # Merge with month_id table
    climate = climate_melted.merge(fields_names, left_on='Month', right_index = True)
    
    # Change column order and sort values
    climate = climate[['City', 'Measure', 'Month', 'Month_id', 'Value']]
    climate.sort_values(['City', 'Measure', 'Month_id'], inplace = True)
    
    
    climate = add_ranks (climate)
    
    # Create a dataframe with the name of the citirs only
    cities_list = climate['City'].drop_duplicates().to_frame().reset_index(drop = True)
                        
    return climate, cities_list



def flag_conditions (cities_climate, cities_list):
    for key, value in conditions.items():
        print(key)
        print(value)
        
        
        if value[0] == 'Annual':
            l = [99]
        elif value[0] in ['Top 3']:
            l = [10, 11, 12]
        elif value[0] in ['Bottom 3']:
            l = [1, 2, 3]
        
        
        # Select cities with this measurement and calculate the average for the selected months/annual
        selected_condition = cities_climate.loc[(cities_climate['Measure'] == value[1]) & (cities_climate['rnk_asc'].isin(l))]\
                                           .groupby(['City', 'Measure'])['Value']\
                                           .mean()\
                                           .to_frame()
                                            
        # Add column with the difference
        selected_condition['{} Dif'.format(key)] = selected_condition['Value'] - statistics.mean(value[2])
        
        # Rename value column
        selected_condition.rename(columns={'Value': key}, inplace = True)
        
        cities_list = cities_list.merge(selected_condition, how = 'left', on = 'City')
    
        # Flag the cities that match the criteria
        cities_list['{} Match'.format(key)] = np.where(
            cities_list['{}'.format(key)].isnull(), pd.NA, np.where(\
            cities_list['{}'.format(key)].between(value[2][0], value[2][1]), True, False))
        
    return cities_list



def print_start(function_name, start_time):
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("Function {} starting".format(function_name.upper()))
    print('{:%Y-%m-%d %H:%M:%S}'.format(start_time))
    print("...")


def print_time(start_time):
    time_used_seconds = (datetime.datetime.now() - start_time).seconds
    time_used_seconds = time_used_seconds + (datetime.datetime.now() - start_time).microseconds / 1000000
    # print("...")
    print("--- {:.3f} seconds".format(time_used_seconds))
    print("---------------------------------------------------")


def print_last(start_time):
    time_used_seconds = (datetime.datetime.now() - start_time).seconds
    time_used_seconds = time_used_seconds + (datetime.datetime.now() - start_time).microseconds / 1000000
    # print("...")
    print("End of script")
    print("--- {:.3f} seconds ---".format(time_used_seconds))
    print("--- {:.3f} minutes ---".format(time_used_seconds / 60))
    print('{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
    print("===================================================")

# def print_start(txt):
#     #print('---------------------')
# #    print('Running: {}'.format(txt.upper()))
#     pass