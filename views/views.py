import sqlite3, os
from datetime import datetime
from flask import render_template, url_for, request, redirect, session
from setup import app
from models.models import *
from test import SomeForm
from urllib.parse import urlparse

print('Hello World ssss')


@app.route('/', methods=["POST", "GET"])
@app.route('/index', methods=["POST", "GET"])
def index():
    form = SomeForm()
    genres = ['strategy', 'adventure', 'action', 'survival', 'rpg', 'rpg']
    selected_genres=dict()
    if request.method == 'POST':
        list_of_games = []
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
    if request.method == 'POST':
        print('hello')
        a = request.form.get('strategy', False)
        print(bool(a))
    return render_template("test.html", form=form)
