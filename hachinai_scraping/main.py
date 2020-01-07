import psycopg2
from psycopg2.extras import DictCursor

from hachinai_scraping import db_init, settings, make_db


def main():
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            db_init.create_table(cur)
            conn.commit()

            make_db.make_db(cur, conn)
            conn.commit()


if __name__ == '__main__':
    DATABASE_URL = settings.DATABASE_URL
    main()
