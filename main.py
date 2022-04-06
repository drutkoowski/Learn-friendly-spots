from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from dbmodels import Cafe, User
from forms import Login, SignUp
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


@app.route("/logout", methods=["GET","POST"])
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/add-spot", methods=["GET","POST"])
def add_spot():
    if current_user.is_authenticated:
        return "<h1> you can add spot </h1>"
    elif not current_user.is_authenticated:
        return "<h1> you can not add spot, log in </h1>"


if __name__ == '__main__':
    app.run(debug=True)
