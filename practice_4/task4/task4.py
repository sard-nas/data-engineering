import sqlite3
import json
from update_methods import *

def parse_textfile(filename: str) -> list:
    with open(filename, encoding='utf-8') as file:
        text = file.read()
    data = []
    for elem in text.split('====='):
        item = {}
        for row in elem.strip().split('\n'):
            if row:
                key, value = row.split('::')[0], row.split('::')[1]
                item[key] = value
        if item.keys():
            item['price'] = float(item['price'])
            item['quantity'] = int(item['quantity'])
            item['views'] = int(item['views'])
            item['updates'] = 0
            if 'category' not in item.keys():
                item['category'] = '-'
            data.append(item)   
    return data

def parse_json(filename: str) -> list:
    with open(filename, encoding='utf-8') as file:
        result = json.load(file)
    return result

def create_table(db):
    cursor = db.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS product (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    name        TEXT (256),
                    price       INTEGER,
                    quantity    REAL,
                    category    TEXT,
                    fromCity    TEXT,
                    isAvailable TEXT,
                    views       INTEGER,
                    updates     INTEGER)""")
    db.commit()

def insert_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""INSERT INTO product (name, price, quantity, category, fromCity, isAvailable, views, updates)
                       VALUES (:name, :price, :quantity, :category, :fromCity, :isAvailable, :views, :updates)""", 
                       data)
    db.commit()

def update_data(db, updates):
    methods = {'quantity_add': quantity_update, 
               'quantity_sub': quantity_update, 
               'price_abs': price_abs, 
               'remove': remove_product, 
               'available': update_available, 
               'price_percent': price_percent}
    for update in updates:
        methods[update['method']](db, update['name'], update['param'])


def select_top_by_updates(db, limit=10):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM product ORDER BY updates DESC LIMIT ?", [limit])
    result = [dict(row) for row in cursor.fetchall()]
    db.commit()
    with open('top_updated.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(result, ensure_ascii=False))

def get_price_stat(db):
    cursor = db.cursor()
    cursor.execute("""SELECT
                        category,
                        ROUND(SUM(price),2) AS sum_price,
                        ROUND(MAX(price),2) AS max_price,
                        ROUND(MIN(price),2) AS min_price,
                        ROUND(AVG(price), 4) as average_price,
                        COUNT(*) AS  product_count
                        FROM product
                        GROUP BY category""")
    result = [dict(row) for row in cursor.fetchall()]
    with open('price_stat.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(result))
    db.commit()

def get_quantity_stat(db):
    cursor = db.cursor()
    cursor.execute("""SELECT
                        category,
                        SUM(quantity) AS sum_quantity,
                        MAX(quantity) AS max_quantity,
                        MIN(quantity) AS min_quantity,
                        ROUND(AVG(quantity), 2) as average_quantity
                        FROM product
                        GROUP BY category""")
    result = [dict(row) for row in cursor.fetchall()]
    with open('quantity_stat.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(result))
    db.commit()

def available_products(db):
    cursor = db.cursor()
    cursor.execute("""SELECT *
                        FROM product
                        WHERE isAvailable = 'True'
                        ORDER BY price""")
    result = [dict(row) for row in cursor.fetchall()]
    with open('available_products.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(result, ensure_ascii=False))
    db.commit()

data = parse_textfile('task_4_var_74_product_data.text')
updates = parse_json('task_4_var_74_update_data.json')

connection = sqlite3.Connection('task4.db')
connection.row_factory = sqlite3.Row
#create_table(connection)

#insert_data(connection, data)

update_data(connection, updates)

select_top_by_updates(connection)
get_price_stat(connection)
get_quantity_stat(connection)
available_products(connection)