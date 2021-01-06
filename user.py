from flask_login import UserMixin
from flask import current_app


class User(UserMixin):
    def __init__(self, username, password, email, phone):
        self.key = ""
        self.username = username
        self.password = password
        self.phone = phone 
        self.email = email
        self.active = True


    def get_id(self):
        return self.username

    @property
    def is_active(self):
        return self.active


def get_user(user_name):
    db = current_app.config["db"]

    user_id = db.get_user_id(user_name)
    
    if user_id is None:
        pass
    else:
        user = db.read_user(user_id)
        return User(user.username,user.password,user.email,user.phone)

