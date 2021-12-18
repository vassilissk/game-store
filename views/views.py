# from cv2 import cv
from service.crud_operations import *
import sqlite3
from setup import app
from models.models import *
from service.forms import SomeForm

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, current_user, \
    login_required, login_user, logout_user

login_manager = LoginManager(app)
login_manager.login_view = '/index#login'


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


print('Hello World ssss')


@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')


@app.route('/index', methods=["POST", "GET"])
@app.route('/', methods=["POST", "GET"])
def index():
    res = flask.make_response()
    res.set_cookie("remember_token", "", expires=0)
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

    return render_template("homepage.html", list_of_games=list_of_games, len=len(list_of_games),
                           form=form, in_or_out=in_or_out, logged=logged, show_profile=show_profile)


@app.route('/cart')
def cart():
    form = SomeForm()
    return render_template("cart.html", form=form)


@app.route('/game/<name>')
def game(name):
    form = SomeForm()
    current_game = Game.query.filter(Game.name == name).first()
    in_or_out, logged, show_profile = show_log_in_out()

    return render_template("game.html", game=current_game, form=form,
                           in_or_out=in_or_out, logged=logged, show_profile=show_profile)


@app.route('/test', methods=["POST", "GET"])
def test():
    form = SomeForm()

    if request.method == 'POST':
        print('hello')
        image = request.files['img']
        avatar = image.read()
        user = User.query.filter_by(username=current_user.username).first()

        user.avatar = sqlite3.Binary(avatar)
        db.session.commit()
    return render_template("test.html", form=form)


@app.route('/userava')
@login_required
def userava():
    img = current_user.avatar
    if not img:
        return url_for('static', filename='default.png')
    return img


@app.route('/index#logout', methods=["POST", "GET"])
@login_required
def logout():
    print("helloooooooooooooooooo")
    logout_user()
    flash("You have been logged out.")
    return redirect("/index")


@app.route('/profile', methods=["POST", "GET"])
@login_required
def profile():
    form = SomeForm()
    if request.method == 'POST':

        image = request.files['img']
        password = request.form['profile_password']
        confirm_password = request.form['profile_confirm_password']
        print(bool(password), bool(confirm_password))
        avatar = image.read()
        user = User.query.filter_by(username=current_user.username).first()
        if password and password == confirm_password:

            user.password = generate_password_hash(request.form['profile_password'])
        elif password:
            flash("passwords must match")
        if avatar:
            user.avatar = sqlite3.Binary(avatar)
        user.username = request.form['username']
        user.email = request.form['email']
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        db.session.commit()
    in_or_out, logged, show_profile = show_log_in_out()
    return render_template("profile.html", form=form,
                           in_or_out=in_or_out, logged=logged, show_profile=show_profile)


def show_log_in_out():
    if current_user.is_authenticated:
        inorout = "fa fa-sign-out"
        logged = "logout"
        show_profile = ""
    else:
        inorout = "fa fa-sign-in"
        logged = "login"
        show_profile = "none"
    return inorout, logged, show_profile
