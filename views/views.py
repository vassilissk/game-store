from datetime import datetime
from flask import render_template, url_for, request, redirect
from setup import app

print('Hello World ssss')


@app.route('/')
def index():
    return render_template("base.html")

@app.route('/cart')
def cart():
    return render_template("cart.html")
