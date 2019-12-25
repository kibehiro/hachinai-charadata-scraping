import psycopg2
from psycopg2.extras import DictCursor

from src import db_init
from src import settings
from src import make_db

DATABASE_URL = settings.DATABASE_URL

with psycopg2.connect(DATABASE_URL) as conn:
    with conn.cursor(cursor_factory=DictCursor) as cur:

        db_init.create_table(cur)
        conn.commit()

        make_db.make_db(cur)
        conn.commit()
