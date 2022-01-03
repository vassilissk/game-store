import datetime
import os

import flask
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

from setup import app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, current_user

login_manager = LoginManager(app)

db = SQLAlchemy(app)


# from models.models import db
# db.create_all()
@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(80), unique=True, nullable=False)
    last_name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    avatar = db.Column(db.BLOB)

    def __repr__(self):
        return '<User %r>' % self.username


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(600), nullable=False)
    parent_id = db.Column(db.Integer, default=0)
    pub_date = db.Column(db.DateTime, nullable=False,
                         default=datetime.datetime.utcnow())
    children_id = db.Column(db.String(600), default=None)
    game_id = db.Column(db.Integer, nullable=False)
    author_name = db.Column(db.String(60), default=None, )
    user_id = db.Column(db.Integer, default=0)
    number_of_parents = db.Column(db.Integer, default=0)
    time_left = db.Column(db.String, nullable=False)


def __repr__(self):
    return '<Comment %r>' % self.id


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    avatar = db.Column(db.BLOB)
    price = db.Column(db.Float)
    genre = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(600))
    hidden = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Game %r>' % self.name


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    payment_type = db.Column(db.String(20), nullable=False)
    comment = db.Column(db.String(600), nullable=True)
    date_of_order = db.Column(db.String, nullable=False)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    amount = db.Column(db.Integer)
    total = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, ForeignKey(Customer.id))

# me = User(username='admin', email='adminwq@example.com')
# db.session.add(me)
# db.session.commit()
