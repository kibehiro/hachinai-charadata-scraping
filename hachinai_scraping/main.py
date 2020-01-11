from hachinai_scraping import settings
from hachinai_scraping.init_db import create_table
from hachinai_scraping.make_db import make_db


def main():
    create_table()
    make_db()


if __name__ == '__main__':
    DATABASE_URL = settings.DATABASE_URL
    main()
