import csv
import sqlite3
import json

def parse_file(filename: str) -> list:
    with open(filename, encoding='utf-8') as file:
        result = json.load(file)
    return result

def create_table(db):
    cursor = db.cursor()
    cursor.execute("""CREATE TABLE comment (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                name          TEXT    REFERENCES building (name),
                rating        REAL,
                convenience   INT,
                security      INT,
                functionality INT,
                comment       TEXT)
                """)
    db.commit()

def insert_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""INSERT INTO comment (name, rating, convenience, security, functionality, comment)
                       VALUES (:name, :rating, :convenience, :security, :functionality, :comment)""", 
                       data)
    db.commit()

def count_of_comments(db):
    cursor = db.cursor()
    cursor.execute(""" SELECT name, street, city,
                        (SELECT COUNT(*) FROM comment WHERE comment.name=building.name) AS count_of_comments
                   FROM building
                    """)
    result = [dict(row) for row in cursor.fetchall()]
    db.commit()
    with open('count_of_comments.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(result, ensure_ascii=False))

def average_rating(db):
    cursor = db.cursor()
    cursor.execute(""" SELECT name, street, city,
                        (SELECT ROUND(AVG(rating),2) FROM comment WHERE comment.name=building.name) AS average_rating
                   FROM building
                   ORDER BY average_rating DESC
                    """)
    result = [dict(row) for row in cursor.fetchall()]
    db.commit()
    with open('average_rating.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(result, ensure_ascii=False))

def rating_stat(db, name):
    cursor = db.cursor()
    cursor.execute(""" SELECT name, street, city,
                        (SELECT MIN(rating) FROM comment WHERE comment.name=building.name) AS min_rating,
                        (SELECT MAX(rating) FROM comment WHERE comment.name=building.name) AS max_rating,
                        (SELECT ROUND(AVG(rating),2) FROM comment WHERE comment.name=building.name) AS average_rating
                   FROM building
                   WHERE name = ?""", [name])
    result = [dict(row) for row in cursor.fetchall()]
    db.commit()
    with open('rating_stat.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(result, ensure_ascii=False))


data = parse_file('task_2_var_74_subitem.json')
connection = sqlite3.connect('task2.db')
connection.row_factory = sqlite3.Row
#create_table(connection)
#insert_data(connection, data)
count_of_comments(connection)
average_rating(connection)
rating_stat(connection, 'Гараж 100')