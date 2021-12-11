import os
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from setup import app
import uuid

database = os.path.join(app.root_path, 'service', 'database.db')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + database
print(database)

from models.models import User, Game

# db = SQLAlchemy(app)


# class User(db.Model):
#     __tablename__ = "User"
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#
#     image = db.Column(db.BLOB)
#
#     def __repr__(self):
#         return '<User %r>' % self.username





#db.create_all()


def convert_to_binary_data(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobdata = file.read()
    return blobdata


# binary = convert_to_binary_data('D:\Python\\final-internal-project\static\game-img\Red Dead Redemption 2.jpg')
# me = User(username='admin',email= 'adminwq@example.com')
# db.session.add(me)
# db.session.commit()


# user = User.query.all()
# print(user[0].username)
# file = user[0].image
# def blob_to_jpg(file):
#    with open('D:\Python\\final-internal-project\static\profile-img\\author-image3.jpg', "wb") as fh:
#        fh.write(file)
# blob_to_jpg(file)

# binary = convert_to_binary_data(os.path.join(app.root_path, 'static\\game-img', 'Red Dead Redemption 2.jpg'))
# game = Game(name='Red Dead Redemption 2', price=157.0, genre='Strategy', image=binary)
# db.session.add(game)
# db.session.commit()

def show_games():
    list_of_games = Game.query.all()