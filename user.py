from flask_login import UserMixin
from flask import current_app


class User(UserMixin):
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.active = True

    def get_id(self):
        return self.username

    @property
    def is_active(self):
        return self.active


def get_user(user_name):
    db = current_app.config["db"]
    user = db.get_user_info(user_name)
    if user is None:
        pass
    else:
        return User(user_name , user[2], user[3])