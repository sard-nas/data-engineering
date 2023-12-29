import pandas as pd
import json
from bson.json_util import dumps, loads

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