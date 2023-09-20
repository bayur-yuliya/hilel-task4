import sqlite3
import random

from faker import Faker
from flask import Flask

app = Flask(__name__)
fake = Faker()


def db_creator():
    connect = sqlite3.connect("task4.db")
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS customers
            (ID INTEGER PRIMARY KEY AUTOINCREMENT, 
            first_name VARCHAR (20) NOT NULL, 
            last_name VARCHAR (20) NOT NULL, 
            email TEXT)
            """)

    cursor.execute("""CREATE TABLE IF NOT EXISTS tracks
            (ID INTEGER PRIMARY KEY AUTOINCREMENT, 
            artist VARCHAR (50), 
            length_in_seconds INT, 
            release_date DATE)
            """)

    connect.commit()
    connect.close()


def data_creator():
    connect = sqlite3.connect("task4.db")
    cur = connect.cursor()

    data_customers = []
    data_tracks = []

    for el in range(100):
        seconds = random.randint(60, 300)

        data_customers.append((el+1, fake.first_name(), fake.last_name(), fake.email()))
        data_tracks.append((el+1, fake.name(), seconds, fake.date()))

    cur.executemany('INSERT OR IGNORE INTO customers VALUES (?, ?, ?, ?)', data_customers)
    cur.executemany("INSERT OR IGNORE INTO tracks VALUES (?, ?, ?, ?)", data_tracks)

    connect.commit()
    connect.close()


@app.route('/names/')
def names():
    new_connect = sqlite3.connect("task4.db")
    new_cur = new_connect.cursor()
    res_query_first_name = new_cur.execute("SELECT COUNT(DISTINCT first_name) FROM customers ")
    unique_names = res_query_first_name.fetchall()

    return f'Кількість унікальних імен клієнтів -  {unique_names[0][0]}'


@app.route('/tracks/')
def tracks():
    new_connect = sqlite3.connect("task4.db")
    new_cursor = new_connect.cursor()
    res_query_count_tracks = new_cursor.execute("SELECT COUNT(*) FROM tracks ")
    count_tracks = res_query_count_tracks.fetchall()

    return f'Кількість записів в таблиці треків: {count_tracks[0][0]}'


@app.route('/tracks-sec/')
def tracks_sec():
    new_connect = sqlite3.connect('task4.db')
    new_cursor = new_connect.cursor()
    res_query_tracks = new_cursor.execute('SELECT ID, length_in_seconds FROM tracks')
    all_tracks_info = ''
    tracks_info = res_query_tracks.fetchall()

    for id_track, length_track in tracks_info:
        all_tracks_info += " Номер трека: " + str(id_track) + ', довжина треку: ' + str(length_track) + ' секунд; <br>'

    return f'Всі треки і  з таблиці треків: <br> {all_tracks_info}'


if __name__ == '__main__':
    db_creator()
    data_creator()
    app.run(debug=True)
