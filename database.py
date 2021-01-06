import psycopg2 as dbapi2
import os
from item import Item
from user import User
from flask import current_app
from datetime import date

dsn = """user='postgres' password='docker' host='localhost' port=5432 dbname='postgres'"""
#dsn = os.getenv('DATABASE_URL')

#import models
class Database:
    def __init__(self):
        self.categories = {}

    ###############################user
    def get_username_from_id(self, id):
        connection = dbapi2.connect(dsn)
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE (id = %(id)s)"
        cursor.execute(query, {'id' : id})
        user = cursor.fetchone()[1]
        return user
    
    def get_user_info(self, username):
        connection = dbapi2.connect(dsn)
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE (username = %(username)s)"
        cursor.execute(query, {'username' : username})
        user = cursor.fetchone()
        return user

    def get_user_id(self,username):
        connection = dbapi2.connect(dsn)
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE (username = %(username)s)"
        cursor.execute(query, {'username' : username})
        id = cursor.fetchone()[0]
        return id
    
    def add_user(self,user):
        connection = dbapi2.connect(dsn)
        cursor = connection.cursor()
        query = "INSERT INTO users (username, password, email, phone_number) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (user.username, user.password, user.email, "",))
        connection.commit()

    def is_email_taken(self,email):
        connection = dbapi2.connect(dsn)
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE (email = %(email)s)"
        cursor.execute(query, {'email' : email})
        user = cursor.fetchone()
        return user

    ################category
    def add_category(self,category_name):
        connection = dbapi2.connect(dsn)
        cursor = connection.cursor()
        query = "INSERT INTO categories category_name VALUES (%s)"
        cursor.execute(query, {'category_name' : category_name})
        connection.commit()
    
    def get_category_names(self):
        connection = dbapi2.connect(dsn)
        cursor = connection.cursor()
        query = "select category_name from categories"
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    
    def get_category(self,id):
        connection = dbapi2.connect(dsn)
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE (id = %(id)s)"
        query = "select category_name from categories where (id = %(id)s)"
        cursor.execute(query, {'id' : id})
        rows = cursor.fetchone()
        return rows
    
    def get_category_id(self,category_name):
        connection = dbapi2.connect(dsn)
        cursor = connection.cursor()
        query = "SELECT * FROM categories WHERE (category_name = %(category_name)s)"
        cursor.execute(query, {'category_name' : category_name})
        id = cursor.fetchone()[0]
        return id

    ###############item 
    def add_item(self,item):
        connection = dbapi2.connect(dsn)
        cursor = connection.cursor()
        query = "INSERT INTO items (category_id,name,description) VALUES (%s, %s, %s)"
        db = current_app.config["db"]
        cat_id = db.get_category_id(item.category) ####im not sure
        cursor.execute(query, (cat_id, item.title, item.description,))
        connection.commit()
    
    def get_item_id(self,name):
        connection = dbapi2.connect(dsn)
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE (name = %(name)s)"
        cursor.execute(query, {'name' : name})
        id = cursor.fetchone()[0]
        return id
    
    def get_item_info(self,id):
        connection = dbapi2.connect(dsn)
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE (id = %(id)s)"
        cursor.execute(query, {'id' : id})
        info = cursor.fetchone()
        return info

    def update_item(self, id, name, description, category_id):
        connection = dbapi2.connect(dsn)
        cursor = connection.cursor()
        query ="""UPDATE items SET 
                    name = %s,
                    description = %s, 
                    category_id = %s
                    WHERE (id = %s)"""
        cursor.execute(query, (name, description,category_id, id))
        connection.commit()
    
    def get_items_from_category_name(self, category_name):
        connection = dbapi2.connect(dsn)
        cursor = connection.cursor()
        db = current_app.config["db"]
        category_id = db.get_category_id(category_name)
        query = "SELECT * FROM items WHERE (category_id = %(category_id)s)"
        cursor.execute(query, {'category_id' : category_id})
        rows = cursor.fetchall()
        return rows
        

    ###############posts

    def create_post(self, username, item_name):
        connection = dbapi2.connect(dsn)
        cursor = connection.cursor()
        
        today = date.today()
        today = today.strftime("%d/%m/%Y")
        
        db = current_app.config["db"]
        user_id = db.get_user_id(username)
        item_id = db.get_item_id(item_name)
        
        query = "INSERT INTO posts (user_id, item_id, post_date) VALUES (%s, %s, %s)"
        cursor.execute(query, (user_id, item_id, today,))
        connection.commit()
    
    def get_all_posts(self):
        connection = dbapi2.connect(dsn)
        cursor = connection.cursor()
        query = "SELECT * FROM posts"
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    
    def get_post(self,id):
        connection = dbapi2.connect(dsn)
        cursor = connection.cursor()
        query = "SELECT * FROM posts WHERE (id = %(id)s)"
        cursor.execute(query, {'id' : id})
        post = cursor.fetchone()
        return post

    def bring_users_post(self, username):
        connection = dbapi2.connect(dsn)
        cursor = connection.cursor()
        db = current_app.config["db"]
        user_id = db.get_user_id(username)
        query = "SELECT * FROM posts WHERE (user_id = %(user_id)s)"
        cursor.execute(query, {'user_id' : user_id})
        rows = cursor.fetchall()
        return rows

    def bring_items_post(self, item_id):
        connection = dbapi2.connect(dsn)
        cursor = connection.cursor()
        query = "SELECT * FROM posts WHERE (item_id = %(item_id)s)"
        cursor.execute(query, {'item_id' : item_id})
        rows = cursor.fetchone()
        return rows




    

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






            







