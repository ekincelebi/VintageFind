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

    ### USER QUERIES

    #okey
    def read_user(self, id):
        #retrive user from id
        connection = dbapi2.connect(dsn)
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE (id = %(id)s)"
        cursor.execute(query, {'id' : id})
        user = cursor.fetchone()
        temp = User(username=user[1], password=user[2], email=user[3], phone=user[4], profile_pic=user[5])
        temp.profile_pic = user[5]
        temp.key = user[0]
        return temp
    
    #okey
    def get_user_id(self,username):
        connection = dbapi2.connect(dsn)
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE (username = %(username)s)"
        cursor.execute(query, {'username' : username})
        user = cursor.fetchone()
        if user is not None:
            return user[0]
        else:
            pass

    #okey
    def add_user(self,user):
        connection = dbapi2.connect(dsn)
        cursor = connection.cursor()
        query = "INSERT INTO users (username, password, email, phone_number, profile_pic ) VALUES (%s, %s, %s, %s, %s)"
        #takes "" for the phone number should change 
        cursor.execute(query, (user.username, user.password, user.email, "", "default.jpg",))
        connection.commit()

    ##gerek var mı bilmiyorum
    def is_email_taken(self,email):
        connection = dbapi2.connect(dsn)
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE (email = %(email)s)"
        cursor.execute(query, {'email' : email})
        user = cursor.fetchone()
        return user

    def update_user(self,user, id):
        #takes userr object as param
        connection = dbapi2.connect(dsn)
        cursor = connection.cursor()
        query ="""UPDATE users SET 
                    username = %s,
                    password = %s, 
                    email = %s,
                    phone_number = %s,
                    profile_pic = %s
                    WHERE (id = %s)"""
        cursor.execute(query, (user.username, user.password, user.email, user.phone, user.profile_pic, id))
        #user.key calısmayabilir
        connection.commit()


    
    def delete_user(self,username):
        connection = dbapi2.connect(dsn)
        cursor = connection.cursor()
        query = "DELETE FROM users WHERE (username = %(username)s)"
        cursor.execute(query, {'username' : username})
        connection.commit()






    

    

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
    #buna gerek kalmadı
    def add_item(self,item):
        connection = dbapi2.connect(dsn)
        cursor = connection.cursor()
        query = "INSERT INTO items (category_id,name,description) VALUES (%s, %s, %s)"
        db = current_app.config["db"]
        cat_id = db.get_category_id(item.category) ####im not sure
        cursor.execute(query, (cat_id, item.title, item.description,))
        connection.commit()

    def add_item_image(self,item,file_name):
        ####let us consider only jpg files available
        connection = dbapi2.connect(dsn)
        cursor = connection.cursor()
        query = "INSERT INTO items (category_id,name,description,image,color,situation) VALUES (%s, %s, %s, %s, %s, %s)"
        db = current_app.config["db"]
        cat_id = db.get_category_id(item.category) 
        data = (cat_id, item.title, item.description, file_name, item.color, item.situation)
        cursor.execute(query, data )
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
    
    def delete_item(self, id):
        connection = dbapi2.connect(dsn)
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE (id = %(id)s)"
        cursor.execute(query, {'id' : id})
        connection.commit()

        

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






            







