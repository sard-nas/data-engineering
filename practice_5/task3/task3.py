from pymongo import MongoClient
from bson.json_util import dumps, loads
import json

def read_data(filename):
    with open(filename, encoding='utf-8') as file:
        result = json.load(file)
    return result

def insert_data(collection, data):
    collection.insert_many(data)

def delete_by_salary(collection):
    query = {
        '$or': [
            {'salary': {'$lt': 25000}},
            {'salary': {'$gt': 175000}}
        ]
    }
    result = collection.delete_many(query)
    print("Count of deleted documents (delete by salary): ", result.deleted_count)

def update_age(collection):
    update = {'$inc': {'age': 1}}
    result = collection.update_many({}, update)
    print("Count of modified documents (update age): ", result.modified_count)

def update_salary_by_job(collection):
    filter = {
        'job': {'$in': ['Врач', 'Учитель', 'Программист', 'Психолог']}
    }
    update = {'$mul': {'salary': 1.05}}
    result = collection.update_many(filter, update)
    print("Count of modified documents (update salary by job): ", result.modified_count)

def update_salary_by_city(collection):
    filter = {
        'city': {'$in': ['Астана', 'Барселона', 'Таллин', 'Бишкек']}
    }
    update = {'$mul': {'salary': 1.07}}
    result = collection.update_many(filter, update)
    print("Count of modified documents (update salary by city): ", result.modified_count)

def update_salary(collection):
    filter = {
        'city': {'$in': ['Хельсинки', 'Москва', 'Рига', 'Тбилиси']},
        'job': {'$in': ['Врач', 'Учитель', 'Программист']},
        '$or': [
            {'age': {'$gt': 18}},
            {'age': {'$lt': 50}}
        ]
    }
    update = {'$mul': {'salary': 1.1}}
    result = collection.update_many(filter, update)
    print("Count of modified documents (update salary by complex predicate): ", result.modified_count)

def delete_by_age(collection):
    query = {
        'job': 'Менеджер',
        '$or': [
            {'age': {'$lt': 20}},
            {'age': {'$gt': 60}}
        ]
    }
    result = collection.delete_many(query)
    print("Count of deleted documents (delete by age): ", result.deleted_count)

client = MongoClient()
db = client['practice5']

data = read_data('task_3_item.json')
insert_data(db.employee, data)
collection = db.employee

delete_by_salary(collection)
update_age(collection)
update_salary_by_job(collection)
update_salary_by_city(collection)
update_salary(collection)
delete_by_age(collection)