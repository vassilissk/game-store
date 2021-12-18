import datetime
import os

from flask_sqlalchemy import SQLAlchemy
from setup import app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin,current_user

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


# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(80), nullable=False)
#     body = db.Column(db.Text, nullable=False)
#     pub_date = db.Column(db.DateTime, nullable=False,
#                          default=datetime.datetime.utcnow())
#
#     category_id = db.Column(db.Integer,
#                             nullable=False)

#
# def __repr__(self):
#     return '<Post %r>' % self.title


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    # image = db.Column(db.BLOB)
    price = db.Column(db.Float)
    genre = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Game %r>' % self.name

# me = User(username='admin', email='adminwq@example.com')
# db.session.add(me)
# db.session.commit()
