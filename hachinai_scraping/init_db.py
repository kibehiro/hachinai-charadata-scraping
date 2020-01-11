import json
from argparse import ArgumentParser

import psycopg2

from hachinai_scraping import make_db, settings


def arg_parse():
    arg_parser = ArgumentParser()
    arg_parser.add_argument('-dd', '--insertDummyData', type=bool,
                            default=False,
                            help='ダミーデータを追加します')
    return arg_parser.parse_args()


def create_table():
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(open('schema.sql', 'r').read())


def insert_dummy_data():
    with open('../json/dummy_data.json', encoding='utf-8') as f:
        dummy_data = json.load(f)

    for data in dummy_data:
        make_db.insert_data(data)


if __name__ == '__main__':
    DATABASE_URL = settings.DATABASE_URL
    args = arg_parse()
    create_table()
    if args.insertDummyData:
        insert_dummy_data()
