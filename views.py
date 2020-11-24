from datetime import datetime
from flask import Flask, render_template, current_app,abort
from product import Product
from database import Database

def home_page():
    today = datetime.today()
    day_name = today.strftime("%A")
    return render_template("home.html", day=day_name)

def ads_page():
    db = current_app.config["db"]
    products = db.get_products()
    return render_template("ads.html", products=sorted(products))

def product_page(product_key):
    db = current_app.config["db"]
    product = db.get_product(product_key)
    if product is None:
        abort(404)
    return render_template("product.html", product=product)