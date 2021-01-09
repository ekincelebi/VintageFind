import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
    'DROP TABLE IF EXISTS public.categories CASCADE',
    'DROP TABLE IF EXISTS public.items CASCADE',
    'DROP TABLE IF EXISTS public.posts CASCADE',
    'DROP TABLE IF EXISTS public.users CASCADE',
    
    '''CREATE TABLE users (
        id serial PRIMARY KEY,
        username varchar(32) NOT NULL UNIQUE,
        password varchar(200) NOT NULL,
        email varchar(254) NOT NULL UNIQUE,
        phone_number varchar(11) NOT NULL );
    ''',
    '''CREATE TABLE categories (
        id serial PRIMARY KEY,
        category_name varchar(32) NOT NULL UNIQUE );
    ''',
    '''CREATE TABLE items (
        id serial PRIMARY KEY,
        category_id serial NOT NULL,
        name varchar(32) NOT NULL,
        description varchar(500) NOT NULL,
        image varchar(120) NOT NULL DEFAULT 'default.jpg',
        CONSTRAINT CONSTRAINT1 FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE );
    ''',
    '''CREATE TABLE posts (
        id serial PRIMARY KEY,
        user_id serial NOT NULL,
        item_id serial NOT NULL,
        post_date date  NOT NULL,
        CONSTRAINT CONSTRAINT1 FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
        CONSTRAINT CONSTRAINT2 FOREIGN KEY (item_id) REFERENCES items (id) ON DELETE CASCADE);
    ''',
]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)