import psycopg2
import requests
from bs4 import BeautifulSoup
from psycopg2.errors import InFailedSqlTransaction

from config import PG_USER, PG_PASS

connection = psycopg2.connect(dbname='tele', user=PG_USER, password=PG_PASS)
cur = connection.cursor()


def __create_table_cities():
    cur.execute("""
                 CREATE TABLE IF NOT EXISTS cities
                (   
                    city_id int GENERATED ALWAYS AS IDENTITY (start with 1) NOT NULL,
                    eng_city varchar(60),
                    rus_city varchar(60),
                    PRIMARY KEY (city_id)
                )
                """)

    connection.commit()


def __create_index():
    cur.execute("""CREATE INDEX IF NOT EXISTS cities_index
                    ON cities (eng_city, rus_city)
                """)


def insert_city(eng_city, rus_city):
    cur.execute("""
                INSERT INTO cities (eng_city, rus_city) VALUES (%s, %s)
                """, (eng_city, rus_city))
    connection.commit()


def select_city(rus_city):
    try:
        cur.execute("""SELECT eng_city  FROM cities WHERE rus_city = %s""",
                    (rus_city,))
        connection.commit()
        fetch = cur.fetchone()
        return fetch[1] if fetch is not None else None
    except InFailedSqlTransaction:
        connection.rollback()


__create_table_cities()
__create_index()

if select_city('санкт-петербург') is None:
    response = requests.get(url='https://www.afisha.ru/')
    all_cities = BeautifulSoup(response.content, 'html.parser').find('ul', class_='city-switcher__list')
    for city_name in all_cities.find_all('a', {'class': 'city-switcher__item-link'}, href=True):
        insert_city(eng_city=city_name['href'].strip('/'), rus_city=city_name.get_text().lower())
