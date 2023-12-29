import os
from optimization import *

# Link to download dataset: https://catalog.data.gov/dataset/crime-data-from-2020-to-present

filename = "data/Crime_Data_from_2020_to_Present.csv"
filesize = os.path.getsize(filename)
print(f'File size on disk = {filesize // (1024 ** 2)} MB')

dataset = pd.read_csv(filename)
os.makedirs('results/task6', exist_ok=True)
get_memory_stat(dataset, 'results/task6/memory_stat.json')
optimized_dataset = optimize_dataset(dataset)
get_memory_stat(optimized_dataset, 'results/task6/memory_stat_optimized.json')


column_types = {}
use_columns = ['AREA', 'AREA NAME', 'Status', 'Status Desc', 
               'Vict Age', 'Vict Sex', 'Vict Descent',
               'Rpt Dist No', 'Cross Street', 'Weapon Used Cd', 'Weapon Desc']
              
for key in use_columns:
    column_types[key] = optimized_dataset.dtypes[key]

with open('results/task6/dtypes.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(column_types,  default=str))

has_header = True
for chunck in pd.read_csv(filename,
                          usecols=lambda x: x in use_columns,
                          dtype=column_types,
                          chunksize=1000000):
    chunck.to_csv('results/task6/dataframe.csv', mode='a', header=has_header)
    has_header = False


