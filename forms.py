from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, SelectField
from wtforms.validators import InputRequired, EqualTo, ValidationError, Email, Length
from flask import current_app

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])

class PostForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
    category = SelectField(u'Categories',validate_choice=False)
    color = SelectField(u'Color',validate_choice=False)
    picture = FileField('Image', validators=[InputRequired(),FileAllowed(['jpg', 'png'])])
    tag1 = StringField('Tag 1')
    tag2 = StringField('Tag 2')
    submit = SubmitField('Publish')

class SearchForm(FlaskForm):
    choices = [('Color', 'Color'),
               ('Situation', 'Situation'),
               ('Category', 'Category')]
    select = SelectField('Search for product:', choices=choices)
    search = StringField('')

    

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[InputRequired()])
    email = StringField('Email',
                        validators=[InputRequired(), Email()])
    phone = StringField('Phone')
    password = PasswordField("Password", validators=[InputRequired()])
    picture = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Update')

    
    


