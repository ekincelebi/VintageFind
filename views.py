from datetime import datetime
from flask import Flask, render_template, current_app,abort,request,redirect, url_for
from product import Product
from database import Database

def home_page():
    today = datetime.today()
    day_name = today.strftime("%A")
    return render_template("home.html", day=day_name)

def ads_page():
    db = current_app.config["db"]
    if request.method == "GET":
        products = db.get_products()
        return render_template("ads.html", products=sorted(products))
    else:
        form_product_keys = request.form.getlist("product_keys")
        for form_product_key in form_product_keys:
            db.delete_product(int(form_product_key))
        return redirect(url_for("ads_page"))

def product_page(product_key):
    db = current_app.config["db"]
    product = db.get_product(product_key)
    if product is None:
        abort(404)
    return render_template("product.html", product=product)

def product_add_page():
    if request.method == "GET":
        values = {"name": "", "situation": "", "description": ""}
        #return render_template("product_edit.html", min_price=0, max_year=10000, values=values)
        return render_template("product_edit.html",values=values)
    else:
        name = request.form["name"]
        situation = request.form["situation"]
        description = request.form["description"]
        product = Product(name, situation=situation, description=description)
        db = current_app.config["db"]
        product_key = db.add_product(product)
        return redirect(url_for("product_page", product_key=product_key))



def product_edit_page(product_key):
    if request.method == "GET":
        db = current_app.config["db"]
        product = db.get_product(product_key)
        if product is None:
            abort(404)
        values = {"name": product.name, "situation": product.situation, "description": product.description}
        return render_template(
            "product_edit.html",
            values=values,
        )
    else:
        '''valid = validate_product_form(request.form)
        if not valid:
            return render_template(
                "product_edit.html",
                min_price=0, max_year=10000,
                values=request.form,)'''
        form_name = request.form["name"]
        form_situation = request.form["situation"]
        form_description = request.form["description"]
        #product = Product(form_name,  price=int(form_price ) if form_price  else None)
        product = Product(form_name, situation=form_situation, description=str(form_description) if form_description  else None)
        db = current_app.config["db"]
        db.update_product(product_key,product)
        return redirect(url_for("product_page",product_key=product_key))

    
'''
    def validate_product_form(form):
    form.data = {}
    form.errors = {}
    

    form_name = form.get("name", "").strip()
    if len(form_name) == 0:
        form.errors["name"] = "Name area can not be blank."
    else:
        form.data["name"] = form_name

    form_price = form.get("price")
    if not form_price:
        form.data["price"] = None
    elif not form_year.isdigit():
        form.errors["Price"] = "Price must consist of digits only."
    else:
        price = int(form_price)
        if (price < 0) or (price > 10000):
            form.errors["Price"] = "Price is out of range."
        else:
            form.data["price"] = price

    return len(form.errors) == 0
    '''