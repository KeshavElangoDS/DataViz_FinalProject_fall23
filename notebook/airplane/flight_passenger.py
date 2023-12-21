"""
flight_passenger.py
"""
import os
import pandas as pd
import pathlib



col = ['Year', 'Month', 'DOMESTIC', 'INTERNATIONAL', 'TOTAL']
airports_of_interest = [
    'Dallas/Fort', 'Oakland Int', 'Sacramento', 'Kansas City', 'John F',
    'Philadelphia Int', 'Boise', 'John Wayne', 'Hartsfield', 'Seattle'
]
air_fare_columns = ['Year', 'Quarter', 'Current_US_Avg', 'Infl_Adj_US_Avg', 'Current_City_Avg', 'Infl_Adj_City_Avg']
col_order = ['Year', 'Month', 'Quarter', 'City', 
             'Domestic Passengers', 'International Passengers', 'Total Passengers', 
             'Domestic Flights', 'International Flights', 'Total Flights']


def process_data(file_path):
    data = pd.read_csv(file_path)
    mask_1 = data['Year'] > 2002
    mask_2 = data['Month'] != 'TOTAL'
    data = data[mask_1 & mask_2][:-1].reset_index(drop=True)
    data['Month'] = data['Month'].astype(int)
    data['Quarter'] = data['Month'].apply(lambda x: (x - 1) // 3 + 1)
    data[col[2:]] = data[col[2:]].replace(',', '', regex=True).astype(int)
    data['City'] = data['City'].astype(str)
    suffix = ' Passengers' if 'passengers' in file_path else ' Flights'
    renamed_col = {key: (f'{key}{suffix}').title() for key in col[2:]}
    data.rename(columns=renamed_col, inplace=True)
    return data
    

def merge_datasets(data_p, data_f, columns):
    merged_data = pd.merge(data_p, data_f, on=columns)
    if len(columns) == 2:
        return merged_data
    return merged_data[col_order]

def df_to_csv(dataframe, file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
    dataframe.to_csv(file_path, index=False)

def df_to_csv(dataframe, file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
    dataframe.to_csv(file_path, index=False)


def get_airports_info():
    """
    Get all airports information we are interested in.
    """
    data_file= pathlib.Path('data/airports_code@public.csv')
    airports_info = pd.read_csv(data_file, delimiter=';', header=0)
    mask = airports_info['Airport Name'].str.contains('|'.join(airports_of_interest), case=False)
    selected_airports = airports_info[mask].drop([3776, 3980]).reset_index(drop=True)
    selected_airports = selected_airports.drop(columns=['World Area Code', 'Country Name', 'Country Code'], inplace=False)
    selected_airports['City Name'] = selected_airports['City Name'].str.split(',').str[0]
    extracted_data_file = pathlib.Path('data/airports_information.csv')
    df_to_csv(selected_airports, extracted_data_file)
    return selected_airports