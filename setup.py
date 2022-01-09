# import threading, schedule, time
# import datetime
# from service.crud_operations import *
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, session
from datetime import timedelta
# from flask_sqlalchemy import SQLAlchemy
# from flask_admin import Admin
# from flask_admin.contrib.sqla import ModelView
import os

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
database = os.path.join(app.root_path, 'service', 'database.db')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + database
app.config["REMEMBER_COOKIE_DURATION"] = timedelta(weeks=1)
# app.config [ "UPLOAD_FOLDER"] = os.path.join(app.root_path, 'static', 'profile-img')

# db = SQLAlchemy(app)
# admin = Admin(app)
from views.views import *

from models.models import Game, User, db

# admin.add_view(ModelView(User,db.session))
# admin.add_view(ModelView(Game,db.session))
app.secret_key = 'the random string'


def background_deleting():
    games = Game.query.filter(Game.hidden == 1)
    for game in games:
        if datetime.datetime.now() > game.hidden_date + datetime.timedelta(weeks=13):
            db.session.delete(game)
    db.session.commit()


def test_func():
    print("Hello")


schedule = BackgroundScheduler(daemon=True)
# sched.add_job(background_deleting, 'interval', weeks=1)
schedule.add_job(test_func, 'cron', week='1-53')
schedule.start()

if __name__ == "__main__":
    app.run(debug=True)
