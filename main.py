import requests
from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from dbmodels import Cafe, User
from forms import Login, SignUp,NewSpot
from flask_bootstrap import Bootstrap


app = Flask(__name__)
##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "saj21#12da!s321@das*(aas$as6"
db = SQLAlchemy(app)
Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)

API_KEY = "2d079ddff24b3df03e4b409dd70a097699c115333909fa0789acd47be42822bd"
API_ENDPOINT = "https://serpapi.com/search.json"
query = ""




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/", methods=["GET", "POST"])
def home():
    cafes = db.session.query(Cafe).all()
    if request.method == "POST":
        city_to_search = request.form.get('city-search')
        return render_template('index.html', cafes=cafes, city_to_search=city_to_search)
    return render_template("index.html", cafes=cafes)

@app.route("/login", methods=["GET","POST"])
def login():
    form = Login()
    if request.method == "POST":
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('home'))
        if not user:
            return render_template("register.html", form=form)

    return render_template("login.html", form=form)

@app.route("/register", methods=["GET","POST"])
def signup():
    form = SignUp()

    if request.method == "POST" and form.validate_on_submit():

        name = form.name.data
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user:
            return render_template("register.html", form=form)
        else:
            print("elo")
            hash_and_salted_password = generate_password_hash(
                password,
                method='pbkdf2:sha256',
                salt_length=8
            )
            new_user = User(
                email=email,
                name=name,
                password=hash_and_salted_password,
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('home'))

    return render_template("register.html", form=form)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/add-spot", methods=["GET","POST"])
@login_required
def add_spot():
    form = NewSpot()
    if request.method == "POST":
        nameofspot = form.name.data
        city = form.name.data
        query = f"{nameofspot} {city}"
        params = {
            "engine": "google_maps",
            "q": query,
            "api_key": API_KEY,
        }

        response = requests.get(API_ENDPOINT, params=params)
        data = response.json()
        title = data["local_results"][0]["title"]
        google_maps_url = data["search_metadata"]["google_maps_url"]
        img_url = form.img_url.data
        location = form.location.data
        seats = form.seats.data
        has_toilet = form.has_toilet.data
        has_wifi = form.has_wifi.data
        has_sockets = form.has_sockets.data
        can_take_calls = form.can_take_calls.data
        rating = data["local_results"][0]["rating"]
        address = data["local_results"][0]["address"]
        phone = data["local_results"][0]["phone"]
        price = data["local_results"][0]["price"]



        cafe = Cafe(name=title,map_url=google_maps_url,img_url=img_url,location=location,seats=seats,
                    has_toilet=has_toilet,has_wifi=has_wifi,has_sockets=has_sockets,can_take_calls=can_take_calls,
                    rating=rating,address=address,phone=phone,price=price)
        db.session.add(cafe)
        db.session.commit()
        return redirect(url_for('home'))

    if current_user.is_authenticated:
        return render_template("add.html", form=form)
    elif not current_user.is_authenticated:
        return "<h1> you can not add spot, log in </h1>"


if __name__ == '__main__':
    app.run(debug=True)
