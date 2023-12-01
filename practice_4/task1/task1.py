import csv
import sqlite3
import json

def parse_file(filename: str) -> list:
    with open(filename,  encoding='utf-8', newline='\n') as file:
        reader = csv.reader(file, delimiter=';')
        rows = [row for row in reader]
        result = []
        for row in rows[1:]:
            item = dict(zip(rows[0], row))
            for key in item.keys():
                if key in ['id', 'floors', 'year', 'zipcode', 'prob_price']:
                    item[key] = int(item[key])
            result.append(item)
    return result

def insert_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""INSERT INTO building (name, street, city, zipcode, floors, year, parking, prob_price, views)
                       VALUES (:name, :street, :city, :zipcode, :floors, :year, :parking, :prob_price, :views)""", 
                       data)
    db.commit()

def select_top_views(db, limit):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM building ORDER BY views DESC LIMIT ?", [limit])
    result = [dict(row) for row in cursor.fetchall()]
    db.commit()
    with open('sorted_by_views.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(result, ensure_ascii=False))

def get_prices_stat(db):
    cursor = db.cursor()
    cursor.execute("""SELECT
                        SUM(prob_price) AS sum,
                        MAX(prob_price) AS max,
                        MIN(prob_price) AS min,
                        ROUND(AVG(prob_price), 2)  AS average
                        FROM building""")
    result = dict(cursor.fetchone())
    with open('prices_stat.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(result))
    db.commit()

def get_city_freq(db):
    cursor = db.cursor()
    cursor.execute("""SELECT
                        city, COUNT(*) as frequency
                        FROM building
                        GROUP BY city
                        ORDER BY frequency DESC""")
    result = [dict(row) for row in cursor.fetchall()]
    with open('city_frequency.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(result, ensure_ascii=False))
    db.commit()

def filter_by_floors(db, min_floors, limit):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM building WHERE floors > ? ORDER BY prob_price LIMIT ?", [min_floors, limit])
    result = [dict(row) for  row in cursor.fetchall()]
    db.commit()
    with open('filtered_by_floors.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(result, ensure_ascii=False))
                 
data = parse_file('task_1_var_74_item.csv')
connection = sqlite3.connect('task1.db')
connection.row_factory = sqlite3.Row
#insert_data(connection, data)
select_top_views(connection, 84)
get_prices_stat(connection)
get_city_freq(connection)
filter_by_floors(connection, 8, 84)