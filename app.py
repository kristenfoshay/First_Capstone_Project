from flask import Flask, render_template, request, flash, redirect, session, g, abort
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

toolbar = DebugToolbarExtension(app)

@app.route('/')
def homepage():

    return render_template('home-anon.html')