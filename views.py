from passlib.hash import pbkdf2_sha256 as hasher
from datetime import datetime
from forms import LoginForm, RegistrationForm, PostForm, UpdateAccountForm
from flask_wtf import FlaskForm
from user import User, get_user
from item import Item
from post import Post

from flask_login import LoginManager, login_user, login_required, logout_user, current_user   
from flask import abort, current_app, render_template, request, redirect, url_for, flash

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

        db.create_post(current_user.username,form.title.data)
        #flash('Your post has been created!', 'success')
        return redirect(url_for('home_page'))
    return render_template("publish.html", form=form)

@login_required
def ads_page():
    db = current_app.config["db"]
    post_list = db.get_all_posts()
    #user_id,item_id,date
    posts = []
    for item in post_list:
        #user,item,date
        #user = db.get_username_from_id(item[1])
        user = db.get_username_from_id(item[1])
        item_name = db.get_item_info(item[2])[2]
        item_description = db.get_item_info(item[2])[3]
        item_category_id = db.get_item_info(item[2])[1]
        tempItem = Item(title=item_name,description=item_description,category=item_category_id)
        date = item[3]
        temp = Post(tempItem,user,date)
        posts.append(temp)
    return render_template('ads.html', posts=posts)
####################################################
@login_required
def ads2_page(category_id):
    db = current_app.config["db"]
    post_list = db.get_all_posts()
    #user_id,item_id,date
    posts = []
    for item in post_list:
        #user,item,date
        #user = db.get_username_from_id(item[1])
        user = db.get_username_from_id(item[1])
        item_name = db.get_item_info(item[2])[2]
        item_description = db.get_item_info(item[2])[3]
        item_category_id = db.get_item_info(item[2])[1]
        tempItem = Item(title=item_name,description=item_description,category=item_category_id)
        date = item[3]
        temp = Post(tempItem,user,date)
        if item_category_id == category_id:
            posts.append(temp)
    return render_template('ads.html', posts=posts)

def post_update(post_id):
    form = PostForm()
    db = current_app.config["db"]
    post = db.get_post(post_id)
    item_id = post[2]
    categories = [ x[0] for x in db.get_category_names()]
    form.category.choices = categories
    if form.validate_on_submit():
        cat_id = db.get_category_id(form.category.data)
        db.update_item(item_id, form.title.data, form.description.data, cat_id)
        return redirect(url_for('post_update', post_id=post_id))
    elif request.method == 'GET':
        item_cat_id = db.get_item_info(item_id)[1]
        item_category = db.get_category(item_cat_id)
        item_name = db.get_item_info(item_id)[2]
        item_description = db.get_item_info(item_id)[3]
        form.title.data = item_name
        form.description.data = item_description
        form.category.data = item_category
    return render_template('another.html', title='Update Post', form=form, post=post)

@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        #update yapmıyor suan icin
        current_user.username = form.username.data
        current_user.email = form.email.data
        #db.session.commit()
        flash('Your account has been update!', 'success')
        return redirect(url_for('account'))
    #######yukarısı update kısmı
    db = current_app.config["db"]
    post_list = db.bring_users_post(current_user.username)
    posts = []
    for item in post_list:
        #user,item,date
        #user = db.get_username_from_id(item[1])
        user = current_user.username
        item_name = db.get_item_info(item[2])[2]
        item_description = db.get_item_info(item[2])[3]
        tempItem = Item(title=item_name,description=item_description,category="")
        date = item[3]
        temp = Post(tempItem,user,date)
        temp.key = item[0] #init key
        posts.append(temp)

    return render_template('account.html', posts=posts, form=form)






def logout_page():
    logout_user()
    #flash("You have logged out.")
    return redirect(url_for("home_page"))

#############employee################

