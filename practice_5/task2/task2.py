from pymongo import MongoClient
from bson.json_util import dumps, loads

def read_data(filename):
    with open(filename, encoding='utf-8') as file:
        text = file.read()
    data = []
    for elem in text.split('====='):
        item = {}
        for row in elem.strip().split('\n'):
            if (row):
                key, value = row.split('::')[0], row.split('::')[1]
                if key in ['job', 'city']:
                    item[key] = value
                else:
                    item[key] = int(value)
        if item:
            data.append(item)   
    return data

def insert_data(collection, data):
    collection.insert_many(data)

def get_salary_stat(collection):
    query = [{
            '$group': {
                '_id': 'salary stats',
                'max_salary': {'$max': '$salary'},
                'min_salary': {'$min': '$salary'},
                'average_salary': {'$avg': '$salary'}
            }
        }]
    cursor = collection.aggregate(query)
    result = list(cursor)
    with open('salary_stat.json', 'w', encoding='utf-8') as file:
        file.write(dumps(result, ensure_ascii=False))

def jobs_freq(collection):
    query = [{
            '$group': {
                '_id': '$job',
                'count': {'$sum': 1}
                }
            },
            {'$sort': {'count': -1}}]
    cursor = collection.aggregate(query)
    result = list(cursor)
    with open('jobs_frequency.json', 'w', encoding='utf-8') as file:
        file.write(dumps(result, ensure_ascii=False))

def get_stat_by_column(collection, column_name, param):
    query = [{
            '$group': {
                '_id': f'${column_name}',
                f'max_{param}': {'$max': f'${param}'},
                f'min_{param}': {'$min': f'${param}'},
                f'average_{param}': {'$avg': f'${param}'}
            }
        }]
    cursor = collection.aggregate(query)
    result = list(cursor)
    with open(f'{param}_stat_by_{column_name}.json', 'w', encoding='utf-8') as file:
        file.write(dumps(result, ensure_ascii=False))

def get_max_salary_by_min_age(collection):
    query = [{
                '$group': {
                    '_id': '$age',
                    'max_salary': {'$max': '$salary'}
                }
            },
            {
                '$group': {
                    '_id': 'max salary by min age',
                    'min_age': {'$min': '$_id'},
                    'max_salary': {'$max': '$max_salary'}
                }
            }]
    
    cursor = collection.aggregate(query)
    result = list(cursor)
    with open('max_salary_by_min_age.json', 'w', encoding='utf-8') as file:
        file.write(dumps(result, ensure_ascii=False))


def get_min_salary_by_max_age(collection):
    query = [{
                '$group': {
                    '_id': '$age',
                    'min_salary': {'$min': '$salary'}
                }
            },
            {
                '$group': {
                    '_id': 'min salary by max age',
                    'max_age': {'$max': '$_id'},
                    'min_salary': {'$min': '$min_salary'}
                }
            }]
    
    cursor = collection.aggregate(query)
    result = list(cursor)
    with open('min_salary_by_max_age.json', 'w', encoding='utf-8') as file:
        file.write(dumps(result, ensure_ascii=False))

def filter_query_1(collection):
    query = [
        {
            '$match': {
                'salary': {'$gt': 50000}
            }
        },
        {
            '$group': {
                '_id': '$city',
                'max_age': {'$max': '$age'},
                'min_age': {'$min': '$age'},
                'average_age': {'$avg': '$age'}
            }
        },
        {'$sort': {'average_age': -1}}
    ]
    cursor = collection.aggregate(query)
    result = list(cursor)
    with open('filter_query_1.json', 'w', encoding='utf-8') as file:
        file.write(dumps(result, ensure_ascii=False))

def filter_query_2(collection):
    query = [
        {
            '$match': {
                'city': {'$in': ['Хельсинки', 'Рига', 'Таллин', 'Прага']},
                'job': {'$in': ['Бухгалтер', 'Строитель', 'Водитель', 'Инженер']},
                '$or': [{'age': {'$gt': 18, '$lt': 25}},
                        {'age': {'$gt': 50, '$lt': 65}}]
            }
        },
        {
            '$group': {
                '_id': 'result',
                'max_salary': {'$max': '$salary'},
                'min_salary': {'$min': '$salary'},
                'average_salary': {'$avg': '$salary'}
            }
        }
    ]
    cursor = collection.aggregate(query)
    result = list(cursor)
    with open('filter_query_2.json', 'w', encoding='utf-8') as file:
        file.write(dumps(result, ensure_ascii=False))

def filter_query_3(collection):
    query = [
        {
            '$match': {
                'age': {'$lt': 30}
            }
        },
        {
            '$group': {
                '_id': '$job',
                'max_salary': {'$max': '$salary'},
                'min_salary': {'$min': '$salary'},
                'average_salary': {'$avg': '$salary'}
            }
        },
        {'$sort': {'average_salary': -1}}
    ]
    cursor = collection.aggregate(query)
    result = list(cursor)
    with open('filter_query_3.json', 'w', encoding='utf-8') as file:
        file.write(dumps(result, ensure_ascii=False))

client = MongoClient()
db = client['practice5']

data = read_data('task_2_item.text')
insert_data(db.employee, data)
collection = db.employee

get_salary_stat(collection)
jobs_freq(collection)

get_stat_by_column(collection, 'city', 'salary')
get_stat_by_column(collection, 'job', 'salary')

get_stat_by_column(collection, 'city', 'age')
get_stat_by_column(collection, 'job', 'age')

get_max_salary_by_min_age(collection)
get_min_salary_by_max_age(collection)

filter_query_1(collection)
filter_query_2(collection)
filter_query_3(collection)
