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
from database import *


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
        return render_template(
            "index.html", server_name=config.server_name, recaptcha=recaptcha.get_code()
        )
    if request.method == "POST":
        if recaptcha.verify():
            old = request.form.get("old")
            new = request.form.get("new")
            if (
                fullmatch("[a-zA-Z0-9_-]+", new)
                and db.session.query(URLs).filter_by(new=new).first() is None
            ):
                new_url = URLs(
                    insert_time=datetime.datetime.now(),
                    username="test-username",  # TODO edit username
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
                    "Bad characters or the new url has been occupied", category="alert"
                )
                return redirect(url_for("index"))

        flash("Please click 'I am not a robot'", category="alert")
        return redirect(url_for("index"))


@app.route("/login", methods=["GET", "POST"])
def login_page():  # TODO
    if not current_user.is_active:
        if request.method == "GET":
            return render_template("login.html")
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            return "test"


# not read again
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

'''
@app.route("/test", methods=["GET", "POST"])
def test_page():
    test_url = db.session.query(URLs).filter_by(new="aaaa").first()
    print(test_url)
    return str(test_url)
'''

@app.errorhandler(404)
def redirect_page(e):
    to_url = db.session.query(URLs).filter_by(new=request.path[1:]).first()
    if to_url is None:
        return redirect(url_for("index"))
    return redirect(to_url.old)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
