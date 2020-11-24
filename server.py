#source venv/bin/active
#python server.py

from flask import Flask
from database import Database
from product import Product
import views

def create_app():
    app = Flask(__name__)
    app.add_url_rule("/", view_func= views.home_page)
    app.add_url_rule("/ads", view_func= views.ads_page)
    app.add_url_rule("/ads/<int:product_key>", view_func=views.product_page)

    db = Database()
    db.add_product(Product("Dining Table", price=5000))
    db.add_product(Product("Wassily Chair", price=2500))
    db.add_product(Product("Vintage Chanel Bag",price=1500))
    app.config["db"] = db
    
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8080, debug=True)