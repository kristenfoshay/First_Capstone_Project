from flask import Flask, render_template, request, flash, redirect, session, g, abort
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from forms import UserAddForm, LoginForm
from models import db, connect_db, User

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ranger'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = "it's a secret"
toolbar = DebugToolbarExtension(app)

connect_db(app)

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id

def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/')
def homepage():

    if g.user:
       ## following_ids = [f.id for f in g.user.following] + [g.user.id]

       ## messages = (Message
               ##     .query
               ##     .filter(Message.user_id.in_(following_ids))
              ##      .order_by(Message.timestamp.desc())
              ##      .limit(100)
              ##      .all())
       ## liked_msg_ids = [msg.id for msg in g.user.likes]      
      ##  not_followed_yet = (Message
                 ##   .query
                ##    .order_by(Message.timestamp.desc())
                ##    .limit(100)
                ##    .all())

        return render_template('home.html')

    else:
        return render_template('home-anon.html')

@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    form = UserAddForm()
    

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                email=form.email.data,
                location=form.location.data,
                image_url=form.image_url.data or User.image_url.default.arg,
                password=form.password.data,
                
            )
            db.session.commit()

        except IntegrityError as e:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('users/signup.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)

@app.route('/logout')
def logout(): 

    do_logout()
    flash(f"Goodbye!", "success")
    return redirect("/login")

@app.route('/eastend')
def eastend():
    return render_template('region/east-end.html')

@app.route('/leslieville')
def leslieville():
    return render_template('region/leslieville.html')