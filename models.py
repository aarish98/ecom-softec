from datetime import datetime
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):

    __tablename__ = "users"

    id = db.Column('user_id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(60), index=True, unique=True)
    password = db.Column('password', db.String(50))
    email = db.Column('email', db.String(50), unique=True, index=True)
    registered_on = db.Column('registered_on', db.DateTime)

    def __init__(self, name, password, email):
        self.name = name
        self.set_password(password)
        self.email = email
        self.registered_on = datetime.utcnow()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % self.username

class Item(db.Model):
    __tablename__ = "Items"

    id = db.Column('item_id', db.Integer, primary_key=True)
    name = db.Column('item_name', db.String(60))
    color = db.Column('color', db.String(60))

