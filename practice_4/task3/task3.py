import msgpack
import json
import sqlite3

def parse_json(filename: str) -> list:
    with open(filename, encoding='utf-8') as file:
        result = json.load(file)
    for row in result:
        row.pop('explicit')
        row.pop('popularity')
        row.pop('danceability')
    return result

def parse_msgpack(filename: str) -> list:
    with open(filename, "rb") as file:
        byte_data = file.read()
    data = msgpack.unpackb(byte_data)
    for row in data:
        row.pop('mode')
        row.pop('speechiness')
        row.pop('acousticness')
        row.pop('instrumentalness')
    return data

def create_table(db):
    cursor = db.cursor()
    cursor.execute("""CREATE TABLE music (
                    id          INTEGER    PRIMARY KEY AUTOINCREMENT,
                    artist      TEXT (256),
                    song        TEXT (256),
                    duration_ms INTEGER,
                    year        INTEGER,
                    tempo       REAL,
                    genre       TEXT (256) )""")
    db.commit()

def insert_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""INSERT INTO music (artist, song, duration_ms, year, tempo, genre)
                       VALUES (:artist, :song, :duration_ms, :year, :tempo, :genre)""", 
                       data)
    db.commit()

def sort_by_year(db, limit):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM music ORDER BY year DESC LIMIT ?", [limit])
    result = [dict(row) for row in cursor.fetchall()]
    db.commit()
    with open('sorted_by_year.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(result, ensure_ascii=False))

def get_tempo_stat(db):
    cursor = db.cursor()
    cursor.execute("""SELECT
                        ROUND(SUM(tempo),2) as sum,
                        ROUND(MAX(tempo),2) as max,
                        ROUND(MIN(tempo),2) as min,
                        ROUND(AVG(tempo), 4) as average
                        FROM music""")
    result = dict(cursor.fetchone())
    with open('tempo_stat.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(result))
    db.commit()

def get_artist_freq(db):
    cursor = db.cursor()
    cursor.execute("""SELECT
                        artist, COUNT(*) as frequency
                        FROM music
                        GROUP BY artist
                        ORDER BY frequency DESC""")
    result = [dict(row) for row in cursor.fetchall()]
    with open('artist_frequency.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(result, ensure_ascii=False))
    db.commit()

def filter_by_genre(db, limit):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM music WHERE genre LIKE '%rock%' ORDER BY year DESC LIMIT ?", [limit])
    result = [dict(row) for  row in cursor.fetchall()]
    db.commit()
    with open('filtered_by_genre.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(result, ensure_ascii=False))

data = parse_json('task_3_var_74_part_1.json') + parse_msgpack('task_3_var_74_part_2.msgpack')
connection = sqlite3.connect('task3.db')
connection.row_factory = sqlite3.Row
#create_table(connection)
#insert_data(connection, data)
sort_by_year(connection, 84)
get_tempo_stat(connection)
get_artist_freq(connection)
filter_by_genre(connection, 89)