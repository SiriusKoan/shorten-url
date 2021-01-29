from flask import Flask, render_template, request, redirect, url_for, abort, flash
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    current_user,
    login_required,
    logout_user,
)
from flask_recaptcha import ReCaptcha
from re import fullmatch
import config
import datetime
from user_tools import *


app = Flask(__name__)
app.config.update(
    dict(
        DEBUG=True,
        SECRET_KEY="4v6945t2mj7terntv48tvnqn4otaei",
        ENV="development",
        RECAPTCHA_ENABLED=True,
        RECAPTCHA_SITE_KEY=config.recaptcha_public_key,
        RECAPTCHA_SECRET_KEY=config.recaptcha_private_key,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_DATABASE_URI="sqlite:///data.db",
    )
)

CORS(app)
recaptcha = ReCaptcha(app)
login_manager = LoginManager(app)
db = SQLAlchemy(app)


# SQLAlchemy
class Users(db.Model):
    __tablename__ = "users"
    ID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    verify_code = db.Column(db.Text, unique=True, nullable=True)
    api_key = db.Column(db.Text, unique=True, nullable=False)

    def __init__(self, username, password, email, verify_code, api_key):
        self.username = username
        self.password = password
        self.email = email
        self.verify_code = verify_code
        self.api_key = api_key


class URLs(db.Model):
    __tablename__ = "urls"
    ID = db.Column(db.Integer, primary_key=True)
    insert_time = db.Column(db.DateTime, nullable=False)
    from_ip = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, nullable=False)
    old = db.Column(db.Text, nullable=False)
    new = db.Column(db.Text, unique=True, nullable=False)

    def __init__(self, insert_time, from_ip, username, old, new):
        self.insert_time = insert_time
        self.from_ip = from_ip
        self.username = username
        self.old = old
        self.new = new


# Exception
class UsernameNotExists(Exception):
    def __init__(self):
        self.category = "error"
        self.message = 'No this user...<br>You can <a href="/register">register</a> it or check your username and login again.'

    def __str__(self):
        return self.category + "+" + self.message


class WrongPassword(Exception):
    def __init__(self):
        self.category = "error"
        self.message = "Authenticate failed..."

    def __str__(self):
        return self.category + "+" + self.message


# User
class User(UserMixin):
    # define basic user
    pass


@login_manager.user_loader
def user_loader(username):
    user = User()
    user.id = username  # use username as user id
    return user


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        """
        db.drop_all()
        db.create_all()

        u = Users(username='a', api_key='a')
        db.session.add(u)
        db.session.commit()
        p = URLs(insert_time=datetime.datetime.now(), from_ip='127.0.0.1', username='user', old='https://google.com', new='meow')
        db.session.add(p)
        db.session.commit()
        """
        return render_template("index.html", server_name=config.server_name)
    if request.method == "POST":
        print(current_user)
        if recaptcha.verify():
            old = request.form.get("old")
            new = request.form.get("new")
            if (
                fullmatch("[a-zA-Z0-9_-]+", new)
                and db.session.query(URLs).filter_by(new=new).first() is None
            ):
                new_url = URLs(
                    insert_time=datetime.datetime.now(),
                    username= "anonymous"
                    if current_user.is_anonymous
                    else current_user.get_id(),
                    from_ip=request.remote_addr,
                    old=old,
                    new=new,
                )
                db.session.add(new_url)
                db.session.commit()

                new_url = config.server_name + new
                flash(
                    'New url: <a href="%s" target="_blank">%s</a>' % (new_url, new_url),
                    category="success",
                )
                return redirect(url_for("index"))
            else:
                flash(
                    "Bad characters or the new url has been occupied.", category="alert"
                )
                return redirect(url_for("index"))

        flash("Please click 'I am not a robot.'", category="alert")
        return redirect(url_for("index"))


@app.route("/login", methods=["GET", "POST"])
def login_page():
    if not current_user.is_active:
        if request.method == "GET":
            return render_template("login.html")
        if request.method == "POST":
            if recaptcha.verify():
                username = request.form["username"]
                password = request.form["password"]
                if login_auth(username, password):
                    user = User()
                    user.id = username
                    login_user(user)
                    flash("Login as %s!" % username, category="success")
                    return redirect(url_for("index"))
                flash("Login failed.", category="alert")
                return redirect(url_for("login_page"))
            else:
                flash("Please click 'I am not a robot.'", category="alert")
                return redirect(url_for("index"))
    else:
        flash("You have logined. Redirect to home page.", category="info")
        return redirect(url_for("index"))


@app.route("/logout", methods=["GET"])
@login_required
def logout_page():
    logout_user()
    flash("Logout.", category="info")
    return redirect(url_for("index"))

# TODO
@app.route("/register", methods=["GET", "POST"])
def register_page():
    pass


# TODO
@app.route("/api", methods=["POST"])
def api():
    try:
        payload = request.get_json()
        old_url = payload["old_url"]
        new_url = payload["new_url"]
        key = payload["key"]
        username = get_username(key)
        save(
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            username,
            request.remote_addr,
            old_url,
            new_url,
        )
        return "%s => %s" % (old_url, new_url)
    except:
        return "Error", 400


@app.route("/user/<username>")
def profile_page(username):
    if current_user.is_active:
        # TODO show profile
        pass
        return "meow"
    else:
        flash("You have not logined. Login to view the profile.", category="alert")
        return redirect(url_for("login_page"))

# TODO
@app.route("/dashboard", methods=["GET"])
def dashboard_page():
    pass


"""
@app.route("/test", methods=["GET", "POST"])
def test_page():
    test_url = db.session.query(URLs).filter_by(new="aaaa").first()
    print(test_url)
    return str(test_url)
"""


@app.errorhandler(404)
def redirect_page(e):
    to_url = db.session.query(URLs).filter_by(new=request.path[1:]).first()
    if to_url:
        return redirect(to_url.old)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
