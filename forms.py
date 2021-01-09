from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, SelectField
from wtforms.validators import InputRequired, EqualTo, ValidationError, Email
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
    submit = SubmitField('Publish')
    picture = FileField('Image', validators=[InputRequired(),FileAllowed(['jpg', 'png'])])
    #image will come later

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[InputRequired()])
    email = StringField('Email',
                        validators=[InputRequired(), Email()])
    
    phone = StringField('Phone')

    password = PasswordField("Password", validators=[InputRequired()])

    picture = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png'])])


    
    submit = SubmitField('Update')

    
    


