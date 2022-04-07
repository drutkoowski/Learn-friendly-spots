from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, DateField, BooleanField, FloatField
from wtforms.validators import DataRequired, URL, NumberRange, Email


class Login(FlaskForm):
    email = StringField("Email: ", validators=[DataRequired(), Email()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    submit = SubmitField("Submit Login")


class SignUp(FlaskForm):
    email = StringField("Email: ", validators=[DataRequired(), Email()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    name = StringField("Username: ", validators=[DataRequired()])
    submit = SubmitField("Submit Sign Up")


class NewSpot(FlaskForm):
    name = StringField("Name of the spot: ", validators=[DataRequired()])
    location = StringField("City: ", validators=[DataRequired()])
    img_url = StringField("Img url: ", validators=[DataRequired(), URL()])
    has_sockets = BooleanField('Has sockets?')
    has_toilet = BooleanField('Has toilet?')
    has_wifi = BooleanField('Has wifi?')
    can_take_calls = BooleanField('Can take calls?')
    seats = StringField('Number of seats: ', validators=[DataRequired()])
    coffee_price = FloatField("Coffee price: ", validators=[DataRequired()])
    submit = SubmitField("Submit Sign Up")
