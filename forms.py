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
    name = StringField("Name: ", validators=[DataRequired()])
    submit = SubmitField("Submit Sign Up")


class NewSpot(FlaskForm):
    name = StringField("Name of the spot: ", validators=[DataRequired()])
    location = StringField("City: ", validators=[DataRequired()])
    img_url = StringField("Img url: ", validators=[DataRequired(), URL()])
    has_sockets = BooleanField('Has sockets?', validators=[DataRequired()])
    has_toilet = BooleanField('Has toilet?', validators=[DataRequired()])
    has_wifi = BooleanField('Has wifi?', validators=[DataRequired()])
    can_take_calls = BooleanField('Can take calls?', validators=[DataRequired()])
    seats = StringField('Number of seats: ', validators=[DataRequired()])
    coffee_price = FloatField("Coffee price: ", validators=[DataRequired()])
    submit = SubmitField("Submit Sign Up")
