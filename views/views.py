import time
import bdb
import copy

import requests.cookies
import datetime
from service.crud_operations import *
import sqlite3
from setup import app, session
from models.models import *
from service.forms import SomeForm

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, current_user, \
    login_required, login_user, logout_user

login_manager = LoginManager(app)
login_manager.login_view = '/index#login'

# import flagpy as fp
# import phonenumbers
# from phonenumbers import timezone, carrier, geocoder


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


print('Hello World ssss')


@app.route('/index', methods=["POST", "GET"])
@app.route('/', methods=["POST", "GET"])
def index():
    if not 'cart' in session:
        session['cart'] = {}

    res = flask.make_response()
    res.set_cookie("remember_token", "", expires=0)
    form = SomeForm()

    genres = ['strategy', 'adventure', 'action', 'survival', 'rpg']
    selected_genres = dict()
    if current_user.is_authenticated and\
            current_user.role == 'Manager' :
        manager_display = "flex"
        admin_display = "none"
        games = Game.query.all()
    elif current_user.is_authenticated and\
            current_user.role == 'Admin' :
        manager_display = "flex"
        admin_display = "flex"
    else:
        manager_display = "none"
        admin_display = "none"
        games = Game.query.filter_by(hidden=0)
    list_of_games = []
    if request.method == 'POST':

        # searching by game name--------------------------------
        if 'search' in request.form:
            search_request = request.form.get('search')
            # print('Hello', search_request == True)
            games = Game.query.all()

            for game in games:
                if search_request.lower() in game.name.lower():
                    list_of_games.append(game)

            list_of_games = [list_of_games[i:i + 3] for i in range(0, len(list_of_games), 3)]

            if not bool(search_request):
                list_of_games = [game for game in games if game.hidden == 0]
                list_of_games = [list_of_games[i:i + 3] for i in range(0, len(list_of_games), 3)]

            in_or_out, logged, show_profile = show_log_in_out()
            hidden_games = [game for game in Game.query.all() if game.hidden > 0]

            return render_template("homepage.html", list_of_games=list_of_games, length=len(list_of_games),
                                   form=form, in_or_out=in_or_out, logged=logged, hidden_games=hidden_games,
                                   admin_display=admin_display, show_profile=show_profile)

            # -----------------sort by genres ---------------

        if any([genre in request.form for genre in genres]):


            for genre in genres:
                selected_genres[genre] = request.form.get(genre, False)

            for genre in selected_genres:
                if selected_genres[genre]:
                    for game in games:
                        if genre in game.genre.lower().split() and game.hidden == 0:
                            list_of_games.append(game)

            list_of_games = [list_of_games[i:i + 3] for i in range(0, len(list_of_games), 3)]
            in_or_out, logged, show_profile = show_log_in_out()
            hidden_games = [game for game in Game.query.all() if game.hidden > 0]
            return render_template("homepage.html", list_of_games=list_of_games, length=len(list_of_games),
                                   form=form, in_or_out=in_or_out, logged=logged, hidden_games=hidden_games,
                                   manager_display=manager_display, show_profile=show_profile,
                                   admin_display=admin_display)

            # ----------- login ---------------

        if 'login_user_name' in request.form:

            username = request.form.get('login_user_name')
            password = request.form.get('login_password')
            remember_me = request.form.get('remember_me')

            log_user = db.session.query(User).filter(User.username == username).first()

            if log_user and check_password_hash(log_user.password, password):
                login_user(log_user, remember=remember_me)
                session['cart'].clear()
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


            hash = generate_password_hash(request.form['password'])

            user = User(username=request.form['username'], first_name=request.form['first_name'],
                        last_name=request.form['last_name'], password=hash, email=request.form['email'])
            db.session.add(user)
            db.session.commit()
            flash(f"User {user.username} is registered")
            return flask.redirect("/index#login")

    hidden_games = [game for game in Game.query.all() if game.hidden > 0]

    list_of_games = [game for game in Game.query.all() if game.hidden == 0]
    list_of_games = [list_of_games[i:i + 3] for i in range(0, len(list_of_games), 3)]
    print(hidden_games)
    in_or_out, logged, show_profile = show_log_in_out()

    cart_games_amount = sum(session['cart'].values()) if len(session['cart']) else ''

    return render_template("homepage.html", list_of_games=list_of_games, length=len(list_of_games),
                           manager_display=manager_display, hidden_games=hidden_games,
                           form=form, in_or_out=in_or_out, logged=logged, show_profile=show_profile,
                           cart_games_amount=cart_games_amount, admin_display=admin_display)


@app.route('/cart', methods=["POST", "GET"])
def cart():
    form = SomeForm()
    game_in_cart_list = []


    for item in session['cart']:
        game_in_cart = Game.query.filter(Game.name == item).first()
        game_in_cart_list.append(game_in_cart)
    cart_games_amount = sum(session['cart'].values()) if \
        len(session['cart']) and sum(session['cart'].values()) else ''
    in_or_out, logged, show_profile = show_log_in_out()
    total = sum(
        [Game.query.filter(Game.name == item).first().price * session['cart'][item] for item in session['cart']])

    return render_template("cart.html", form=form, game_in_cart_list=game_in_cart_list,
                           cart_games_amount=cart_games_amount, in_or_out=in_or_out,
                           logged=logged, show_profile=show_profile, total=total)


@app.route('/cart_plus_minus/<name>', methods=["POST", "GET"])
def cart_plus_minus(name):
    if request.method == "POST":
        if "cart_add" in request.form:
            session['cart'][name] += 1
        elif "cart_sub" in request.form:
            session['cart'][name] -= 1
        if session['cart'][name] < 1:
            session['cart'][name] = 1
        session.modified = True
    return redirect("/cart")


@app.route('/delitem/<name>')
def delitem(name):

    session['cart'].pop(name)
    session.modified = True

    return redirect("/cart")


@app.route('/game/<name>', methods=["POST", "GET"])
def game(name):
    form = SomeForm()
    if current_user.is_authenticated and current_user.role in ['Admin', 'Manager']:
        user_comments = Comment.query.filter(Game.name == name)
    elif current_user.is_authenticated:
        user_comments = Comment.query.filter(Game.name == name).filter(Comment.user_id == current_user.id)
    else:
        user_comments = []

    if request.method == 'POST':
        if current_user.is_authenticated:
            author_name = f"{current_user.first_name} {current_user.last_name}"
            user_id = current_user.id
        else:
            author_name = "User"
            user_id = 1
        comment = Comment(comment=request.form['comment'],
                          game_id=Game.query.filter(Game.name == name).first().id,
                          author_name=author_name,
                          user_id=user_id,
                          time_left=datetime.datetime.today().strftime("%H:%M:%S %b %d %Y"))
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('game', name=name))

    current_game = Game.query.filter(Game.name == name).first()
    comments = Comment.query.filter(Comment.game_id == current_game.id)

    in_or_out, logged, show_profile = show_log_in_out()

    return render_template("game.html", game=current_game, form=form,
                           in_or_out=in_or_out, logged=logged, show_profile=show_profile,
                           comments=comments, user_comments=user_comments)


@app.route('/add_game', methods=["POST", "GET"])
@login_required
def add_game():
    form = SomeForm()

    if request.method == 'POST':
        image = request.files['upload_game_image']
        name = request.form['add_game_name']
        description = request.form['add_game_description']
        game_image = image.read()
        price = request.form['game_price']
        genre = request.form['game_genre']
        game = Game(name=name, description=description, avatar=game_image,
                    price=price, genre=genre)
        db.session.add(game)
        db.session.commit()
        return redirect('/index')
    in_or_out, logged, show_profile = show_log_in_out()
    return render_template('add_game.html', form=form,
                           in_or_out=in_or_out, logged=logged, show_profile=show_profile)


@app.route('/edit_game/<name>', methods=["POST", "GET"])
@login_required
def edit_game(name):
    form = SomeForm()

    if request.method == 'POST':
        game = Game.query.filter_by(name=name).first()
        image = request.files['upload_game_image']
        game.name = request.form['add_game_name']
        game.description = request.form['add_game_description']
        if image:
            game.avatar = image.read()

        game.price = request.form['game_price']
        game.genre = request.form['game_genre']

        db.session.commit()
        return redirect('/index')
    in_or_out, logged, show_profile = show_log_in_out()
    game = Game.query.filter_by(name=name).first()
    return render_template('edit_game.html', form=form, game=game,
                           in_or_out=in_or_out, logged=logged, show_profile=show_profile)


@app.route('/hide_game/<name>', methods=["POST", "GET"])
@login_required
def hide_game(name):
    form = SomeForm()

    game = Game.query.filter_by(name=name).first()
    game.hidden = 1
    game.hidden_date = datetime.datetime.now()
    db.session.commit()
    # game = Game.query.filter_by(name=name).first()
    # print('game',game.hidden)
    return redirect(url_for('index', game=game))


@app.route('/restore_game/<name>', methods=["POST", "GET"])
@login_required
def restore_game(name):

    game = Game.query.filter_by(name=name).first()
    game.hidden = 0
    game.hidden_date = None
    db.session.commit()

    return redirect(url_for('index', game=game))


@app.route('/test', methods=["POST", "GET"])
def test():
    form = SomeForm()

    if request.method == 'POST':

        image = request.files['img']
        avatar = image.read()
        user = User.query.filter_by(username=current_user.username).first()

        user.avatar = sqlite3.Binary(avatar)
        db.session.commit()
    return render_template("test.html", form=form)


@app.route('/userava')
@login_required
def userava():
    if current_user.avatar:
        # print(current_user.avatar)
        img = current_user.avatar

        return img
    else:
        return redirect(url_for('static', filename='default.png'))



@app.route('/game_image/<name>')
def game_image(name):
    img = Game.query.filter_by(name=name).first().avatar
    if img:
        return img
    else:
        return Game.query.filter_by(name='default').first().avatar


@app.route('/comment_ava/<comment_id>')
def comment_ava(comment_id):

    comment = Comment.query.filter_by(id=comment_id).first()
    user = User.query.filter_by(id=comment.user_id).first()

    if user.avatar:

        img = user.avatar

        return img
    else:
        return redirect(url_for('static', filename='default.png'))


@app.route('/index#logout', methods=["POST", "GET"])
@login_required
def logout():
    print("helloooooooooooooooooo")
    logout_user()
    session['cart'].clear()
    flash("You have been logged out.")
    return redirect("/index")


@app.route('/profile', methods=["POST", "GET"])
@login_required
def profile():
    form = SomeForm()

    if request.method == 'POST':

        image = request.files['upload']
        password = request.form['profile_password']
        confirm_password = request.form['profile_confirm_password']
        # print(bool(password), bool(confirm_password))
        avatar = image.read()
        # print('reading avatar')
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
        flask.redirect('profile')
    cart_games_amount = sum(session['cart'].values()) if \
        len(session['cart']) and sum(session['cart'].values()) else ''
    in_or_out, logged, show_profile = show_log_in_out()
    return render_template("profile.html", form=form, cart_games_amount=cart_games_amount,
                           in_or_out=in_or_out, logged=logged, show_profile=show_profile)


@app.route('/success', methods=["POST", "GET"])
def success(name):
    return redirect('/game/<name>')





@app.route('/reply/<name>/<parent_id>', methods=["POST", "GET"])
def reply(name, parent_id):
    res = []
    if current_user.is_authenticated:
        author_name = f"{current_user.first_name} {current_user.last_name}"
        user_id = current_user.id
    else:
        author_name = "User"
        user_id = 1
    parent_comment = Comment.query.filter(Comment.id == parent_id).first()
    current_comment = Comment(comment=request.form['comment'],
                              game_id=Game.query.filter(Game.name == name).first().id,
                              author_name=author_name,
                              user_id=user_id,
                              parent_id=parent_id,
                              number_of_parents=parent_comment.number_of_parents + 1,
                              time_left=datetime.datetime.today().strftime("%H:%M:%S %b %d %Y"))


    rest_comments = Comment.query.filter(Comment.id > parent_comment.id)

    for comment in rest_comments:
        res.append(comment)
    res1 = copy.deepcopy(res)
    for comment in rest_comments:
        db.session.delete(comment)
    db.session.commit()
    db.session.add(current_comment)
    #
    print('res=', res)
    for comment in res1:
        com = Comment(comment=comment.comment,
                      game_id=comment.game_id,
                      author_name=comment.author_name,
                      user_id=comment.user_id,
                      parent_id=comment.parent_id,
                      number_of_parents=comment.number_of_parents,
                      time_left=datetime.datetime.today().strftime("%H:%M:%S %b %d %Y"))
        print('time',datetime.datetime.today().strftime("%H:%M:%S %b %d %Y"))
        db.session.add(com)
    db.session.commit()
    return redirect(url_for('game', name=name))


@app.route('/edit_comment/<name>/<comment_id>', methods=["POST", "GET"])
def edit_comment(name, comment_id):
    current_comment = Comment.query.filter(Comment.id == comment_id).first()
    current_comment.comment = request.form['comment']
    db.session.commit()
    return redirect(url_for('game', name=name))

@app.route('/delete_comment/<name>/<comment_id>')
def delete_comment(name, comment_id):
    current_comment = Comment.query.filter(Comment.id == comment_id).first()
    current_comment.comment = "the comment was deleted by author"
    if current_user.role in ['Admin', 'Manager']:
        db.session.delete(current_comment)
    db.session.commit()

    return redirect(url_for('game', name=name))


@app.route('/add_to_cart/<path:name>', methods=["POST", "GET"])
def add_to_cart(name):
    # if request.method == 'POST':
    if name in session['cart']:
        session['cart'][name] += 1

    else:
        session['cart'][name] = 1
    session.modified = True
    # print(session)
    return redirect('/index' + '#' + name.replace(' ', ''))


@app.route('/confirm_order', methods=["POST", "GET"])
def confirm_order():
    form = SomeForm()
    # ukr = fp.get_flag_img('Ukraine')
    display_method = "block"
    if request.method == "POST":
        # print(request.form)
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        payment_type = request.form['payment_type']
        comment = request.form['add_game_description']
        date_of_order = datetime.datetime.today().strftime("%H:%M:%S %b %d %Y")
        # print(date_of_order)
        customer = Customer(first_name=first_name, last_name=last_name, email=email,
                            phone=phone, payment_type=payment_type, comment=comment, date_of_order=date_of_order)
        db.session.add(customer)
        for item in session['cart']:
            game = item
            price = Game.query.filter(Game.name == game).first().price
            amount = session['cart'][item]
            user_id = customer.id
            total = price * amount
            order = Order(game=game, price=price, amount=amount, user_id=user_id, total=total)
            db.session.add(order)
        db.session.commit()
        flash("Your order has been accepted")
        session['cart'].clear()
        display_method = "none"

    cart_games_amount = sum(session['cart'].values()) if \
        len(session['cart']) and sum(session['cart'].values()) else ''
    in_or_out, logged, show_profile = show_log_in_out()
    return render_template('confirm_order.html', form=form, cart_games_amount=cart_games_amount,
                           in_or_out=in_or_out, logged=logged, show_profile=show_profile,
                           display_method=display_method)


@app.route('/customers_list')
def customers_list():
    form = SomeForm()
    customers_list = [customer for customer in Customer.query.all()]
    # print(customers_list)
    cart_games_amount = sum(session['cart'].values()) if \
        len(session['cart']) and sum(session['cart'].values()) else ''
    in_or_out, logged, show_profile = show_log_in_out()
    return render_template('customers_list.html', form=form, customers_list=customers_list,
                           cart_games_amount=cart_games_amount,
                           in_or_out=in_or_out, logged=logged, show_profile=show_profile)


@app.route('/order/<customer_id>')
def order(customer_id):
    form = SomeForm()
    # print(customer_id)
    # cart_games_amount = sum(session['cart'].values()) if \
    #     len(session['cart']) and sum(session['cart'].values()) else ''

    customer = Customer.query.filter_by(id=customer_id).first()
    order = Order.query.filter_by(user_id=customer_id)
    total = sum([item.total for item in order])
    # print(total)

    in_or_out, logged, show_profile = show_log_in_out()
    return render_template('order.html', form=form, in_or_out=in_or_out, customer=customer, order=order,
                           logged=logged, show_profile=show_profile, total=total)


@app.route('/close_order/<customer_id>')
def close_order(customer_id):
    # print(customer_id)
    customer = Customer.query.filter_by(id=customer_id).first()
    orders = Order.query.filter_by(user_id=customer_id)
    for order in orders:
        db.session.delete(order)
    db.session.delete(customer)
    db.session.commit()
    return redirect('/customers_list')


@app.route('/users_list')
@login_required
def users_list():
    form = SomeForm()
    users = User.query.filter(User.id > 1)

    in_or_out, logged, show_profile = show_log_in_out()
    return render_template('users_list.html', form=form, in_or_out=in_or_out,
                           logged=logged, show_profile=show_profile, users=users)


@app.route('/change_role/<user_id>', methods=["POST", "GET"])
@login_required
def change_role(user_id):
    if request.method == "POST":
        user = User.query.filter(User.id == user_id).first()
        print(user.first_name)
        role = request.form['roles']
        user.role = role
        print(role)
        db.session.commit()
        return redirect('/users_list')


# @app.route('/country')
# def country():
#     ukr = fp.get_flag_img('Ukraine')
#     return ukr


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
