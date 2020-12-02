from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, length, Email, EqualTo, ValidationError
from app.models import User


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), length(min=5, max=20)])
    confirm = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Register')

    # check the database
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose another one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already taken. Please choose another one')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), length(min=5, max=20)])
    remember = BooleanField('Remember')
    submit = SubmitField('Sign in')


class ManagerForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), length(min=5, max=20)])
    submit = SubmitField('check')




class CarForm(FlaskForm):
    car_type = StringField('car_type', validators=[DataRequired(), length(min=1, max=255)])
    car_level = StringField('car_level', validators=[DataRequired(), length(min=1, max=100)])
    price = IntegerField('price', validators= [DataRequired()])
    submit = SubmitField('add in')

class EditForm(FlaskForm):
    car_type = StringField('car_type', validators=[DataRequired(), length(min=1, max=255)])
    car_level = StringField('car_level', validators=[DataRequired(), length(min=1, max=100)])
    price = IntegerField('price', validators=[DataRequired()])
    availability = StringField('availability', validators=[DataRequired(), length(min=1, max=10)])

    submit = SubmitField('update ')




