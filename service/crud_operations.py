import flask
from flask import render_template, url_for, request, redirect, flash
from setup import app
from service.forms import SomeForm
from flask_login import login_user
# from models.models import *











# def convert_to_binary_data(filename):
#     # Convert digital data to binary format
#     with open(filename, 'rb') as file:
#         blobdata = file.read()
#     return blobdata


# binary = convert_to_binary_data('D:\Python\\final-internal-project\static\game-img\Red Dead Redemption 2.jpg')
# me = User(username='admin',email= 'adminwq@example.com')
# db.session.add(me)
# db.session.commit()


# user = User.query.all()
# print(user[0].username)
# file = user[0].image

# def blob_to_jpg(file):
#     with open('D:\Python\\final-internal-project\static\profile-img\\author-image3.jpg', "wb") as fh:
#         fh.write(file)


# blob_to_jpg(file)

# binary = convert_to_binary_data(os.path.join(app.root_path, 'static\\game-img', 'Red Dead Redemption 2.jpg'))
# game = Game(name='Red Dead Redemption 2', price=157.0, genre='Strategy', image=binary)
# db.session.add(game)
# db.session.commit()


