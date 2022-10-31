from os import environ

import databases

DB_NAME = environ.get('DB_NAME', 'foton_db')
DB_USER = environ.get('DB_USER', 'foton_user')
DB_PASS = environ.get('DB_PASS', 'qwerty123')
DB_HOST = environ.get('DB_HOST', 'localhost')

SQLALCHEMY_DATABASE_URL = f'postgres://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}'

database = databases.Database(url=SQLALCHEMY_DATABASE_URL)
