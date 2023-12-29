import os
from optimization import *

filename = "data/vacancies_2020.csv"
filesize = os.path.getsize(filename)
print(f'File size on disk = {filesize // (1024 ** 2)} MB')

dataset = pd.read_csv(filename)
os.makedirs('results/task4', exist_ok=True)
get_memory_stat(dataset, 'results/task4/memory_stat.json')
optimized_dataset = optimize_dataset(dataset)
get_memory_stat(optimized_dataset, 'results/task4/memory_stat_optimized.json')

column_types = {}
use_columns = ['employer_id', 'salary_from', 'salary_to',
               'type_name', 'accept_incomplete_resumes', 'prof_classes_found',
               'test_required', 'schedule_name', 'experience_name', 'address_city', 'employer_industries']

for key in use_columns:
    column_types[key] = optimized_dataset.dtypes[key]

with open('results/task4/dtypes.json', 'w', encoding='utf-8') as file:
    file.write(json.dumps(column_types,  default=str))

has_header = True
for chunck in pd.read_csv(filename,
                          usecols=lambda x: x in use_columns,
                          dtype=column_types,
                          chunksize=1000000):
    chunck.to_csv('results/task4/dataframe.csv', mode='a', header=has_header)
    has_header = False