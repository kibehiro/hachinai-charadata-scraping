import psycopg2
from psycopg2.extras import DictCursor

from src import db_init
from src import settings

DATABASE_URL = settings.DATABASE_URL

# print(DATABASE_URL)

with psycopg2.connect(DATABASE_URL) as conn:
    with conn.cursor(cursor_factory=DictCursor) as cur:

        db_init.create_table(cur)
        conn.commit()

        db_init.insert_dummy_data(cur)
        conn.commit()
