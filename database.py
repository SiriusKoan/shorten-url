from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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