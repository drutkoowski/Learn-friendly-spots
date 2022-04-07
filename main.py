import requests
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from dbmodels import Cafe, User
from forms import Login, SignUp, NewSpot
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


@app.route("/delete/<int:cafe_id>")
def delete_cafe(cafe_id):
    # post_to_delete = Cafe.query.get(cafe_id)
    # db.session.delete(post_to_delete)
    # db.session.commit()
    return redirect(url_for('home'))



@app.route("/", methods=["GET", "POST"])
def home():
    cafes = db.session.query(Cafe).all()
    if request.method == "POST":
        city_to_search = request.form.get('city-search')
        return render_template('index.html', cafes=cafes, city_to_search=city_to_search)
    return render_template("index.html", cafes=cafes)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = Login()
    if request.method == "POST" and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                msg = flash(f'Nice to see you again {user.name}!', category="info")
                login_user(user)
                return redirect(url_for('home', flash=msg))
        if not user or not check_password_hash(user.password, password):
            flash('Account with these credentials can not be found.', category="warning")
            return render_template("login.html", form=form)

    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def signup():
    form = SignUp()

    if request.method == "POST" and form.validate_on_submit():

        name = form.name.data
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        is_name = User.query.filter_by(name=name).first()
        if user or is_name:
            flash(f'User with these credentials already exists!', category="info")
            return render_template("register.html", form=form)
        else:
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
            flash(f'Welcome on board {name}!', category="info")
            return redirect(url_for('home'))

    return render_template("register.html", form=form)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    user = current_user
    flash(f'{user.name} Logged out successfully!', category="info")
    logout_user()
    return redirect(url_for('home'))


@app.route("/add-spot", methods=["GET", "POST"])
def add_spot():
    form = NewSpot()
    formlogin = Login()
    if request.method == "POST" and form.validate_on_submit():
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

        google_maps_url = data["search_metadata"]["google_maps_url"]
        img_url = form.img_url.data
        location = form.location.data
        seats = form.seats.data
        has_toilet = form.has_toilet.data
        has_wifi = form.has_wifi.data
        has_sockets = form.has_sockets.data
        can_take_calls = form.can_take_calls.data
        coffee_price = str(form.coffee_price.data)
        try:
            title = data["local_results"][0]["title"]
            rating = data["local_results"][0]["rating"]
            price = data["local_results"][0]["price"]
            address = data["local_results"][0]["address"]
            phone = data["local_results"][0]["phone"]

        except KeyError:
            try:
                title = data["place_results"]["title"]
                rating = data["place_results"]["rating"]
                address = data["place_results"]["address"]
                phone = data["place_results"]["phone"]
                price = data["place_results"]["price"]
            except:
                flash('We could not add your Cafe to our database, please refine the invocation!', category="warning")
                return render_template("add.html", form=form)

        cafe = Cafe(name=title, map_url=google_maps_url, img_url=img_url, location=location, seats=seats,
                    has_toilet=has_toilet, has_wifi=has_wifi, has_sockets=has_sockets, can_take_calls=can_take_calls,
                    rating=rating, address=address, phone=phone, price=price, coffee_price=coffee_price)
        if cafe:
            db.session.add(cafe)
            db.session.commit()
        flash('Cafe added successfully!', category="info")
        return redirect(url_for('home'))

    if current_user.is_authenticated:
        return render_template("add.html", form=form)
    elif not current_user.is_authenticated:
        flash('You need to sign in to add a new spot!', category="info")
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
