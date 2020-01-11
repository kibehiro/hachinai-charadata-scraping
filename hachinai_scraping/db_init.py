import json

from hachinai_scraping import make_db


def create_table(cur):
    cur.execute(open('schema.sql', 'r').read())


def insert_dummy_data(cur):
    with open('../json/dummy_data.json', encoding='utf-8') as f:
        dummy_data = json.load(f)

    for data in dummy_data:
        make_db.make_db(data, cur)
