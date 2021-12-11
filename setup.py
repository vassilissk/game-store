from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
database = os.path.join(app.root_path, 'service', 'database.db')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + database
app.debug = True
# db = SQLAlchemy(app)
from views.views import *

app.secret_key = 'the random string'

if __name__ == "__main__":
    app.run()
