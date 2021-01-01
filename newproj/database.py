import psycopg2 as dbapi2
import os
from item import Item
from user import User
from flask import current_app

dsn = """user='postgres' password='docker' host='localhost' port=5432 dbname='postgres'"""
#dsn = os.getenv('DATABASE_URL')

#import models
class Database:
    def __init__(self):
        self.categories = {}

    
    def get_user_info(self, username):
        connection = dbapi2.connect(dsn)
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE (username = %(username)s)"
        cursor.execute(query, {'username' : username})
        user = cursor.fetchone()
        return user
    
    def add_user(self,user):
        connection = dbapi2.connect(dsn)
        cursor = connection.cursor()
        query = "INSERT INTO users (username, password, email, phone_number) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (user.username, user.password, user.email, "",))
        connection.commit()

    def add_category(self,category_name):
        connection = dbapi2.connect(dsn)
        cursor = connection.cursor()
        query = "INSERT INTO categories category_name VALUES (%s)"
        cursor.execute(query, {'category_name' : category_name})
        connection.commit()
    
    def is_email_taken(self,email):
        connection = dbapi2.connect(dsn)
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE (email = %(email)s)"
        cursor.execute(query, {'email' : email})
        user = cursor.fetchone()
        return user
    
    def get_category_names(self):
        connection = dbapi2.connect(dsn)
        cursor = connection.cursor()
        query = "select category_name from categories"
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    
    
    def get_category_id(self,category_name):
        connection = dbapi2.connect(dsn)
        cursor = connection.cursor()
        query = "SELECT * FROM categories WHERE (category_name = %(category_name)s)"
        cursor.execute(query, {'category_name' : category_name})
        id = cursor.fetchone()[0]
        return id

    def add_item(self,item):
        connection = dbapi2.connect(dsn)
        cursor = connection.cursor()
        query = "INSERT INTO items (category_id,name,description) VALUES (%s, %s, %s)"
        db = current_app.config["db"]
        cat_id = db.get_category_id(item.category) ####im not sure
        cursor.execute(query, (cat_id, item.title, item.description,))
        connection.commit()

    

    #INSERT INTO items (category_id,name,description) VALUES ((SELECT id from categories  WHERE category_name='furniture'), 'wassily chair', 'cool chair');


        

#dsn = """user='postgres' password='docker' host='localhost' port=5432 dbname='postgres'"""
"""def add_category(category_name):
    connection = dbapi2.connect(dsn)
    cursor = connection.cursor()
    query = "INSERT INTO categories (category_name) VALUES (%s)"
    cursor.execute(query,(category_name,))
    connection.commit()

def read_categories():
    connection = dbapi2.connect(dsn)
    cursor = connection.cursor()
    query = "select id, category_name from categories"
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows

def is_username_exist(username):
    connection = dbapi2.connect(dsn)
    cursor = connection.cursor()
    query = "SELECT ID FROM users WHERE (USERNAME = %(username)s)"
    cursor.execute(query, {'username' : username})
    if cursor.fetchone() is None:
        print("no user")
        return False
    else:
        print("user exist")
        return True

def get_user(email):
    connection = dbapi2.connect(dsn)
    cursor = connection.cursor()
    query = "SELECT * FROM users WHERE (email = %(email)s)"
    cursor.execute(query, {'email' : email})
    user = cursor.fetchone()
    return user
def get_password_from_username(username):
    connection = dbapi2.connect(dsn)
    cursor = connection.cursor()
    query = "SELECT * FROM users WHERE (username = %(username)s)"
    cursor.execute(query, {'username' : username})
    password = cursor.fetchone()[2]
    return password

def is_email_exist(email):
    connection = dbapi2.connect(dsn)
    cursor = connection.cursor()
    query = "SELECT ID FROM users WHERE (EMAIL= %(email)s)"
    cursor.execute(query, {'email' : email})
    if cursor.fetchone() is None:
        print("e mail adress does not exist")
        return False
    else:
        print("e mail adress exist")
        return True

#umarım dogrudur
def get_user_from_email(email):
    connection = dbapi2.connect(dsn)
    cursor = connection.cursor()
    query = "SELECT PASSWORD FROM users WHERE (EMAIL= %(email)s)"
    cursor.execute(query, {'email' : email})
    user = cursor.fetchone()[0]
    return user

def add_user(user):
    connection = dbapi2.connect(dsn)
    cursor = connection.cursor()
    query = "INSERT INTO users (username, password, email, phone_number) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (user.username, user.password, user.email, user.phonenumber,))
    connection.commit()"""






            







