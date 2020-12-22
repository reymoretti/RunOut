from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from flask import session


class Customer(db.Model, UserMixin):
    __tablename__='Customer'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    name = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return "Customer(%r, %r, %r)" % (self.username, self.email, self.image_file)

class Foodseller(db.Model, UserMixin):
    __tablename__ = 'Foodseller'
    id = db.Column(db.Integer, primary_key=True)
    foodsellerName = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    city = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(20), nullable=False)
    phone_number = db.Column(db.Integer, unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return "Foodseller(%r, %r, %r, %r)" % (self.foodsellerName, self.image_file, self.city, self.address)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return "Post(%r, %r)" % (self.title, self.date_posted)


@login_manager.user_loader
def load_user(user_id):
    if session['type'] == 'customer':
        return Customer.query.get(int(user_id))
    elif session['type'] == 'foodseller':
        return Foodseller.query.get(int(user_id))
    else:
        return None




