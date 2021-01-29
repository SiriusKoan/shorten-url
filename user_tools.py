import sqlite3 as sql
from hashlib import sha256
from app import db, Users
    
def login_auth(username, password):
    hash_password = sha256(bytes(password.encode("utf-8"))).hexdigest()
    user = db.session.query(Users).filter_by(username=username).first()
    print(user)
    if user:
        return hash_password == user.password
    return False
