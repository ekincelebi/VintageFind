from flask_login import LoginManager
from datetime import datetime
from flask import Flask
import views
from user import get_user
import os
from database import Database
#from database import Database


lm = LoginManager()

@lm.user_loader
def load_user(user_id):
    return get_user(user_id)

def create_app():
    app = Flask(__name__)
    #app.config.from_object("settings")
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

    app.add_url_rule("/", view_func=views.home_page)
    app.add_url_rule("/login", view_func=views.login_page, methods=["GET", "POST"])
    app.add_url_rule("/register", view_func=views.register_page, methods=['GET', 'POST'])
    app.add_url_rule("/logout", view_func=views.logout_page)
    app.add_url_rule("/post/create", view_func=views.publish_page , methods=["GET", "POST"])
    app.add_url_rule("/post/<int:post_id>/update", view_func=views.post_update , methods=["GET", "POST"])
    app.add_url_rule("/ads", view_func=views.ads_page , methods=["GET", "POST"])
    app.add_url_rule("/account", view_func=views.account , methods=["GET", "POST"])
    app.add_url_rule("/ads/<int:category_id>", view_func=views.ads2_page , methods=["GET", "POST"])

    
    lm.init_app(app)
    lm.login_view = "login_page"

    db = Database()
    app.config["db"] = db


    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080, debug=True)