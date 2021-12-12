import sqlite3, os
from datetime import datetime

import flask
from flask import render_template, url_for, request, redirect, session,flash
from setup import app
from models.models import *
from test import SomeForm
from werkzeug.security import generate_password_hash, check_password_hash

print('Hello World ssss')


@app.route('/', methods=["POST", "GET"])
@app.route('/index', methods=["POST", "GET"])
def index():
    form = SomeForm()

    genres = ['strategy', 'adventure', 'action', 'survival', 'rpg', 'rpg']
    selected_genres=dict()
    if request.method == 'POST':

        list_of_games = []

        # searching by game name--------------------------------
        if 'search' in request.form:
            search_request = request.form.get('search', False)
            print(search_request)
            games = Game.query.all()
            for game in games:
                if search_request.lower() in game.name.lower():
                    list_of_games.append(game)
            return render_template("homepage.html", list_of_games=list_of_games, len=len(list_of_games),
                                   form=form)

        if any([genre in request.form for genre in genres]):
            flash('You were successfully logged in')
            for genre in genres:
                selected_genres[genre] = request.form.get(genre, False)
            for genre in selected_genres:
                if selected_genres[genre]:
                    genre_games = Game.query.filter(Game.genre == genre)
                    for game in genre_games:
                        list_of_games.append(game)
            return render_template("homepage.html", list_of_games=list_of_games, len=len(list_of_games),
                                               form=form)

            print(genre)
            print(selected_genres)
            print(list_of_games)

        if 'login_user_name' in request.form:
            # print(request.form['login_user_name'])
            # print(request.form['login_password'])
            # print(request.form['remember_me'])
            # print(request.form['login_submit'])
            pass

        if 'username' in request.form:
            user = request.form['username']
            email = request.form['email']
            users = User.query.all()
            user_list = [user.username for user in users]
            email_list = [user.email for user in users]
            # print(email in email_list)
            # print(email_list)
            # print(user_list)
            # print(User.query.filter(User.email == request.form['email'])[0].email)
            if user in user_list:
                print(f"User {user} already exists")
                flash(f"User {user} already exists")
                return flask.redirect("/index#register")

            elif email in email_list:
                flash(f"e-mail {email} already exists")
                return flask.redirect("/index#register")

            # if request.form['password'] == request.form['confirm_password']
            hash = generate_password_hash(request.form['password'])

            user = User(username=request.form['username'], first_name=request.form['first_name'],
                        last_name=request.form['last_name'],password=hash,
                        email=request.form['email'])
            db.session.add(user)
            db.session.commit()
    list_of_games = Game.query.all()
    return render_template("homepage.html", list_of_games=list_of_games, len=len(list_of_games),
                           form=form)


@app.route('/cart')
def cart():
    # a=5
    # session['a']=3
    # print(url_for('cart'))
    # print(session, app.config)
    # me = Game(name='Grand Theft Auto V', price=199.3, genre='strategy',image='Grand Theft Auto V.jpg')
    # db.session.add(me)
    # db.session.commit()
    return render_template("cart.html")


@app.route('/game/<game_id>')
def game(game_id):
    game = Game.query.filter(Game.id == game_id)[0]

    return render_template("game.html", game=game)



@app.route('/test', methods=["POST", "GET"])
def test():
    form = SomeForm()
    print(request.values)
    if request.method == 'POST':
        print('hello')
    #     a = request.form.get('strategy', False)
    #     print(bool(a))
    return render_template("test.html", form=form)
