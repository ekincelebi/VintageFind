#source venv/bin/active
#python server.py

from flask import Flask
from database import Database
from product import Product
import views

def create_app():
    app = Flask(__name__)
    app.add_url_rule("/", view_func= views.home_page)
    app.add_url_rule("/ads", view_func= views.ads_page, methods=["GET", "POST"])
    app.add_url_rule("/ads/<int:product_key>", view_func=views.product_page)
    app.add_url_rule(
        "/ads/<int:product_key>/edit",
        view_func= views.product_edit_page,
        methods=["GET", "POST"],
    )
    app.add_url_rule("/new-product", view_func=views.product_add_page, methods=["GET", "POST"])

    db = Database()
    app.config["db"] = db
    
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080, debug=True)