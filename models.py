from datetime import datetime
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Users(db.Model):
    __tablename__ = "Users"

    id = db.Column('user_id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(60), index=True, unique=True)
    password = db.Column('password', db.String(50))
    email = db.Column('email', db.String(50), unique=True, index=True)
    registered_on = db.Column('registered_on', db.DateTime)
    products_created = db.relationship('Products',backref='Users', lazy='dynamic')

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


class Products(db.Model):
    __tablename__ = "Products"

    id = db.Column('product_id', db.Integer, primary_key=True)
    name = db.Column('product_name', db.String(60))
    color = db.Column('product_color', db.String(60))
    size = db.Column('product_size', db.String)
    description = db.Column('product_description', db.String)
    original_quantity = db.Column('original_quantity', db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey('Categories.category_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'))

    def __init__(self, name, color, size, original_quantity, description):
        self.name = name
        self.color = color
        self.size = size
        self.description = description
        self.original_quantity = original_quantity


class Categories(db.Model):
    __tablename__ = "Categories"

    id = db.Column('category_id', db.Integer, primary_key=True)
    name = db.Column('category_name', db.String(40))
    products = db.relationship('Products', backref='Categories', lazy='dynamic')

    def __init__(self, name):
        self.name = name
