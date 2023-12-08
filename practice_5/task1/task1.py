from pymongo import MongoClient
import csv
from bson.json_util import dumps, loads

def read_data(filename):
    with open(filename,  encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        rows = [row for row in reader]
        result = []
        for row in rows[1:]:
            item = dict(zip(rows[0], row))
            for key in item.keys():
                if key in ['salary', 'id', 'year', 'age']:
                    item[key] = int(item[key])
            result.append(item)
    return result

def insert_data(collection, data):
    collection.insert_many(data)

def select_top_salary(collection):
    cursor = collection.find({}, limit=10).sort({'salary': -1})
    result = list(cursor)
    with open('top_salaries.json', 'w', encoding='utf-8') as file:
        file.write(dumps(result, ensure_ascii=False))
        
def select_by_age(collection):
    cursor = collection.find({'age': {'$lt': 30}}, limit=15).sort({'salary': -1})
    result = list(cursor)
    with open('selected_by_age.json', 'w', encoding='utf-8') as file:
        file.write(dumps(result, ensure_ascii=False))
    
def filter_query(collection):
    cursor = collection.find({
        'city': 'Санкт-Петербург', 
        'job': {'$in': ['Продавец', 'Инженер', 'Психолог']}
        }, limit=10).sort({'age': 1})
    
    result = list(cursor)
    with open('filtered.json', 'w', encoding='utf-8') as file:
        file.write(dumps(result, ensure_ascii=False))

def count_query(connection):
    result = collection.count_documents({
        'age': {'$gt': 18, '$lt': 45},
        'year': {'$in': [2019, 2020, 2021, 2022]},
        '$or': [{'salary': {'$gt': 50000, '$lte': 75000}},
               {'salary': {'$gt': 125000, '$lt': 150000}}]
    })
    with open('count.json', 'w', encoding='utf-8') as file:
        file.write(dumps(result, ensure_ascii=False))

client = MongoClient()
db = client['practice5']

data = read_data('task_1_item.csv')
insert_data(db.employee, data)
collection = db.employee

select_top_salary(collection)
select_by_age(collection)
filter_query(collection)
count_query(collection)