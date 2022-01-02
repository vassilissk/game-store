# import threading, schedule, time
import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, session
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
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

# from models.models import Game,User,db
# admin.add_view(ModelView(User,db.session))
# admin.add_view(ModelView(Game,db.session))
app.secret_key = 'the random string'

count = 0


def sensor():
    global count
    """ Function for test purposes. """
    count += 1

    print("Scheduler is alive!", count, datetime.datetime.now())


sched = BackgroundScheduler(daemon=True)
sched.add_job(sensor, 'interval', weeks=1)
sched.start()

if __name__ == "__main__":
    app.run(debug=True)
