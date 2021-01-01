#source venv/bin/active
#source /Users/ios/Documents/GitHub/VintageFind/venv/bin/activate
#python server.py

from flask import Flask
from flask_login import LoginManager

from database import Database
from product import Product
from user import get_user

import views

#lm = LoginManager()


@lm.user_loader
def load_user(user_id):
    return get_user(user_id)

def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")
    app.add_url_rule("/", view_func= views.home_page, methods=["GET"])
    app.add_url_rule("/<int:product_key>", view_func=views.product_page_home)

    app.add_url_rule(
        "/login", view_func=views.login_page, methods=["GET", "POST"]
    )
    app.add_url_rule("/logout", view_func=views.logout_page)
    
    app.add_url_rule("/ads", view_func= views.ads_page, methods=["GET", "POST"])
    app.add_url_rule("/ads/<int:product_key>", view_func=views.product_page)
    app.add_url_rule(
        "/ads/<int:product_key>/edit",
        view_func= views.product_edit_page,
        methods=["GET", "POST"],
    )
    app.add_url_rule("/new-product", view_func=views.product_add_page, methods=["GET", "POST"])

    lm.init_app(app)
    lm.login_view = "login_page"

    db = Database()
    app.config["db"] = db
    
    return app


if __name__ == "__main__":
    app = create_app()
    port = app.config.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port)