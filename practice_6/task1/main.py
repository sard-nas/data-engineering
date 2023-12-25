import pandas as pd
import os
import json
from bson.json_util import dumps, loads
import numpy as np

def get_memory_stat(dataset, filename):
    memory_stat = dataset.memory_usage(deep=True)
    total_memory = memory_stat.sum()
    column_stat = []
    for key in dataset.dtypes.keys():
        column_stat.append({
            'name': key,
            'memory_abs': int(memory_stat[key] // 1024),
            'memory_per': round(memory_stat[key] / total_memory * 100, 3),
            'data_type': dataset.dtypes[key]
        })
    column_stat.sort(key=lambda x: x['memory_abs'], reverse = True)
    column_stat.append({'total_memory_usage': total_memory // 1024})
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(json.dumps(column_stat,  default=str))

def convert_to_categorial_values(dataframe):
    result = pd.DataFrame()
    dataset_obj = dataframe.select_dtypes(include=['object']).copy()
    for column in dataset_obj.columns:
        count_unique = len(dataset_obj[column].unique())
        total_count = len(dataset_obj[column])
        if count_unique / total_count < 0.5:
            result.loc[:, column] = dataset_obj[column].astype('category')
        else:
            result.loc[:, column] = dataset_obj[column]
    return result

def downcast_int(dataframe):
    dataset_int = dataframe.select_dtypes(include=['int']).copy()
    downcasted_int = dataset_int.apply(pd.to_numeric, downcast = 'unsigned')
    return downcasted_int

def downcast_float(dataframe):
    dataset_float = dataframe.select_dtypes(include=['float']).copy()
    downcasted_float = dataset_float.apply(pd.to_numeric, downcast = 'float')
    return downcasted_float

def optimize_dataset(dataset):
    converted_obj = convert_to_categorial_values(dataset)
    opt_int = downcast_int(dataset)
    opt_float = downcast_float(dataset)
    result = dataset.copy()
    result[converted_obj.columns] = converted_obj
    result[opt_int.columns] = opt_int
    result[opt_float.columns] = opt_float
    return result

filename = "../data/game_logs.csv"
filesize = os.path.getsize(filename)
print(f'File size on disk = {filesize // 1024} KB')

dataset = pd.read_csv(filename)
os.makedirs('./results', exist_ok=True)
get_memory_stat(dataset, 'results/memory_stat.json')
optimized_dataset = optimize_dataset(dataset)
get_memory_stat(optimized_dataset, 'results/memory_stat_optimized.json')

column_types = {}
use_columns = ['date', 'number_of_game', 'day_of_week',
               'v_league', 'day_night', 'length_minutes',
               'v_hits', 'v_doubles', 'attendance', 'v_errors']
              
for key in use_columns:
    column_types[key] = optimized_dataset.dtypes[key]

with open('dtypes.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(column_types,  default=str))

has_header = True
for chunck in pd.read_csv(filename,
                          usecols=lambda x: x in use_columns,
                          dtype=column_types,
                          chunksize=1000000):
    chunck.to_csv('dataframe.csv', mode='a', header=has_header)
    has_header = False