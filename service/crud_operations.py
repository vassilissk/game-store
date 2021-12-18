import flask
from flask import render_template, url_for, request, redirect, flash
from setup import app
from service.forms import SomeForm
from flask_login import login_user
from models.models import *

database = os.path.join(app.root_path, 'service', 'database.db')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + database
print(database)

from models.models import User, Game


def show_log_in_out():
    if current_user.is_authenticated:
        inorout = "fa fa-sign-out"
        logged = "logout"
        show_profile = "flex"
    else:
        inorout = "fa fa-sign-in"
        logged = "login"
        show_profile = "none"
    return inorout, logged, show_profile


def for_index():
    form = SomeForm()

    genres = ['strategy', 'adventure', 'action', 'survival', 'rpg', 'rpg']
    selected_genres = dict()
    if request.method == 'POST':

        list_of_games = []

        # searching by game name--------------------------------
        if 'search' in request.form:
            search_request = request.form.get('search', False)

            games = Game.query.all()
            for game in games:
                if search_request.lower() in game.name.lower():
                    list_of_games.append(game)
            in_or_out, logged, show_profile = show_log_in_out()
            return render_template("homepage.html", list_of_games=list_of_games, len=len(list_of_games),
                                   form=form, in_or_out=in_or_out, logged=logged, show_profile=show_profile)

            # -----------------sort by genres ---------------

        if any([genre in request.form for genre in genres]):
            flash('You were successfully logged in')
            for genre in genres:
                selected_genres[genre] = request.form.get(genre, False)
            for genre in selected_genres:
                if selected_genres[genre]:
                    genre_games = Game.query.filter(Game.genre == genre)
                    for game in genre_games:
                        list_of_games.append(game)
            in_or_out, logged, show_profile = show_log_in_out()
            return render_template("homepage.html", list_of_games=list_of_games, len=len(list_of_games),
                                   form=form, in_or_out=in_or_out, logged=logged, show_profile=show_profile)

            # ----------- login ---------------

        if 'login_user_name' in request.form:

            username = request.form.get('login_user_name')
            password = request.form.get('login_password')
            remember_me = request.form.get('remember_me')

            log_user = db.session.query(User).filter(User.username == username).first()

            if log_user and check_password_hash(log_user.password, password):
                login_user(log_user, remember=remember_me)
                return redirect(url_for('index'))

            flash("Invalid username/password", 'error')
            return redirect('/index#login')

            # ------------------------registration------------------------

        if 'username' in request.form:
            user = request.form['username']
            email = request.form['email']
            users = User.query.all()
            user_list = [user.username for user in users]
            email_list = [user.email for user in users]

            if user in user_list:

                flash(f"User {user} already exists")
                return flask.redirect("/index#register")

            elif email in email_list:
                flash(f"e-mail {email} already exists")
                return flask.redirect("/index#register")

            # if request.form['password'] == request.form['confirm_password']
            hash = generate_password_hash(request.form['password'])

            user = User(username=request.form['username'], first_name=request.form['first_name'],
                        last_name=request.form['last_name'], password=hash,
                        email=request.form['email'])
            db.session.add(user)
            db.session.commit()
            flash(f"User {user.username} is registered")
            return flask.redirect("/index#login")

    list_of_games = Game.query.all()
    in_or_out, logged, show_profile = show_log_in_out()

    return list_of_games, len(list_of_games), form, in_or_out, logged, show_profile




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


