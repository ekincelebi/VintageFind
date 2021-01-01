from passlib.hash import pbkdf2_sha256 as hasher
from datetime import datetime
from forms import LoginForm, RegistrationForm, PostForm
from flask_wtf import FlaskForm 
from user import User, get_user
from item import Item

from flask_login import LoginManager, login_user, login_required, logout_user, current_user   
from flask import abort, current_app, render_template, request, redirect, url_for

def home_page():
    today = datetime.today()
    day_name = today.strftime("%A")
    return render_template("home.html", day=day_name)

##############logging##################
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        temp = get_user(username)
        if temp is not None:
            #realpassword = temp.password
            user = User(username, temp.password,temp.email)
            password = form.password.data
            if password == temp.password: ##burayı sonra hashli yaparsın
                login_user(user)
                #flash("You have logged in.")
                next_page = request.args.get("next", url_for("home_page"))
                return redirect(next_page)

            else:
                return ("Wrong Password")
        else:
            return ("User can not be found")
    return render_template("login.html", form=form)

def register_page():
    form = RegistrationForm()
    if form.validate_on_submit():
        password = form.password.data
        username = form.username.data
        email = form.email.data
        temp = get_user(username)
        db = current_app.config["db"]
        email_check = db.is_email_taken(email)
        if temp is not None or email_check is not None:
            return ("Please check your username and password!")
        else:
            user = User(username,password,email)
            db.add_user(user)
            return redirect(url_for('login_page'))
    return render_template('register.html', form=form)

@login_required
def publish_page():
    form = PostForm()

    db = current_app.config["db"]
    categories = [ x[0] for x in db.get_category_names()]
    
    form.category.choices = categories
    if form.validate_on_submit():
        cat = form.category.data
        newItem = Item(title=form.title.data,description=form.description.data,category=cat)
        #add item 
        db = current_app.config["db"]
        db.add_item(newItem)
        #flash('Your post has been created!', 'success')
        return redirect(url_for('home_page'))
    return render_template("publish.html", form=form)





def logout_page():
    logout_user()
    #flash("You have logged out.")
    return redirect(url_for("home_page"))

#############employee################

