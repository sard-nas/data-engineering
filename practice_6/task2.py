import os
from optimization import *

filename = "data/CIS_Automotive_Kaggle_Sample.csv"
filesize = os.path.getsize(filename)
print(f'File size on disk = {filesize // (1024 ** 2)} MB')

use_columns = ['firstSeen', 'lastSeen', 'askPrice',
               'vf_FuelTypePrimary', 'vf_FuelTypeSecondary', 'mileage', 
               'isNew', 'color', 'brandName', 'modelName','vf_ActiveSafetySysNote']

df = pd.DataFrame()
for chunk in pd.read_csv(filename, chunksize=100000, usecols=use_columns, low_memory=False):
    df = pd.concat([df, chunk])

os.makedirs('results/task2', exist_ok=True)
get_memory_stat(df, 'results/task2/memory_stat.json')
optimized_dataset = optimize_dataset(df)
get_memory_stat(optimized_dataset, 'results/task2/memory_stat_optimized.json')

column_types = {}              
for key in use_columns:
    column_types[key] = optimized_dataset.dtypes[key]

with open('results/task2/dtypes.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(column_types,  default=str))

has_header = True
for chunck in pd.read_csv(filename,
                          usecols=lambda x: x in use_columns,
                          dtype=column_types,
                          chunksize=1000000):
    chunck.to_csv('results/task2/dataframe.csv', mode='a', header=has_header)
    has_header = False
