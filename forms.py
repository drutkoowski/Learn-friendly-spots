from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, DateField
from wtforms.validators import DataRequired, URL, NumberRange, Email


class Login(FlaskForm):
    email = StringField("Email: ", validators=[DataRequired(), Email()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    submit = SubmitField("Submit Login")


class SignUp(FlaskForm):
    email = StringField("Email: ", validators=[DataRequired(), Email()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    name = StringField("Name: ", validators=[DataRequired()])
    submit = SubmitField("Submit Sign Up")
