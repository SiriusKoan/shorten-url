from hashlib import sha256
from database import db, Users
from re import fullmatch
from random import sample


def login_auth(username, password):
    hash_password = sha256(bytes(password.encode("utf-8"))).hexdigest()
    user = Users.query.filter_by(username=username).first()
    if user:
        return hash_password == user.password
    return False


def register(username, password, email):
    if (
        fullmatch("[a-zA-Z0-9_-]+", username)
        and Users.query.filter_by(username=username).first() is None
    ):
        new_user = Users(
            username=username,
            password=sha256(bytes(password.encode("utf-8"))).hexdigest(),
            email=email,
            verify_code=None,
            api_key=generate_api_key(username),
        )
        db.session.add(new_user)
        db.session.commit()
        return True
    else:
        return False


def generate_api_key(username):
    ingredient = sha256(bytes(username.encode("utf-8"))).hexdigest()
    ingredient = sample(ingredient, 40)[:20]
    ingredient = sample(ingredient, 1)[0].join(ingredient)
    return ingredient

    
    