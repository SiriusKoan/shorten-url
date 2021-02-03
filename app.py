from flask import Flask, render_template, request, redirect, url_for, abort, flash
from flask_cors import CORS
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
from user_tools import login_auth, register
from url_tools import add_url, get_urls_by
from database import db, URLs, Users


app = Flask(__name__)
app.config.from_object(config.Config)
CORS(app)
recaptcha = ReCaptcha(app)
login_manager = LoginManager(app)
db.init_app(app)

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
        return render_template("index.html", server_name=config.server_name)
    if request.method == "POST":
        if recaptcha.verify():
            old = request.form.get("old")
            new = request.form.get("new")
            username = (
                "anonymous" if current_user.is_anonymous else current_user.get_id()
            )
            from_ip = request.remote_addr
            if add_url(old, new, username, from_ip):
                new_url = config.server_name + new
                flash(
                    'New url: <a href="%s" target="_blank">%s</a>' % (new_url, new_url),
                    category="success",
                )
                return redirect(url_for("index"))
            else:
                flash(
                    "Bad characters or the new url has been occupied.",
                    category="alert",
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
            username = request.form["username"]
            password = request.form["password"]
            if login_auth(username, password):
                user = User()
                user.id = username
                login_user(user)
                flash("Login as %s!" % username, category="success")
                return redirect(url_for("index"))
            else:
                flash("Login failed.", category="alert")
                return redirect(url_for("login_page"))
    else:
        flash("You have logined. Redirect to home page.", category="info")
        return redirect(url_for("index"))


@app.route("/logout", methods=["GET"])
def logout_page():
    # TODO notice
    if current_user.is_active:
        logout_user()
        flash("Logout.", category="info")
        return redirect(url_for("index"))
    else:
        flash("You have not logined.", category="info")
        return redirect(url_for("login_page"))


@app.route("/register", methods=["GET", "POST"])
def register_page():
    if not current_user.is_active:
        if request.method == "GET":
            return render_template("register.html")
        if request.method == "POST":
            if recaptcha.verify():
                username = request.form["username"]
                password = request.form["password"]
                email = request.form["email"]
                if register(username, password, email):
                    flash(
                        "Register successfully! You can login now.",
                        category="success",
                    )
                    return redirect(url_for("login_page"))
                else:
                    flash(
                        "Bad characters or the username has been occupied.",
                        category="alert",
                    )
                    return redirect(url_for("index"))

            else:
                flash("Please click 'I am not a robot.'", category="alert")
                return redirect(url_for("register_page"))
    else:
        flash("You have logined. Redirect to home page.", category="info")
        return redirect(url_for("index"))


@app.route("/api", methods=["POST"])
def api():
    payload = request.get_json()
    old = payload["old"]
    new = payload["new"]
    api_key = payload["api_key"]

    user = Users.query.filter_by(api_key=api_key).first()
    if user is None:
        abort(401)
    else:
        if add_url(old, new, user.username, request.remote_addr):
            return ""
        else:
            abort(400)


@app.route("/dashboard", methods=["GET"])
@login_required
def dashboard_page():
    username = current_user.get_id()
    user = Users.query.filter_by(username=username).first()
    profile = {"username": username, "email": user.email, "api_key": user.api_key}
    urls = get_urls_by(username)
    return render_template("dashboard.html", profile=profile, urls=urls)
    


@app.errorhandler(404)
def redirect_page(e):
    to_url = URLs.query.filter_by(new=request.path[1:]).first()
    if to_url:
        return redirect(to_url.old)
    return redirect(url_for("index"))  # TODO customize 404 page


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
