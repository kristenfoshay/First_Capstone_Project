import os
from flask import Flask, render_template, request, flash, redirect, session, g, abort
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from forms import UserAddForm, LoginForm
from models import db, connect_db, User, Post, Neighbourhood, Board

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("://", "ql://", 1) or  'postgresql:///ranger'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ranger'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = "it's a secret"
toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

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
    """Route to Home for logged in user or generic if not logged in. Render template for posts owned by logged in user."""
    if g.user:
        user = g.user
        posts = user.posts

        return render_template('home.html', posts=posts)

    else:
        return render_template('home-anon.html')

@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup."""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    form = UserAddForm()
    
    """Form submit"""
    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                email=form.email.data,
                location=form.location.data,
                password=form.password.data,
                
            )
            db.session.commit()

            """If Username taken, flash messsage"""
        except IntegrityError as e:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        """If no error, login user and redirect to home"""
        do_login(user)

        return redirect("/")

        """render form for signup"""
    else:
        return render_template('users/signup.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()
    """Form submit"""
    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        """If successful user authentication, flash message"""
        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        """If not, flash message"""

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)

@app.route('/logout')
def logout(): 
    """Handle user logout."""
    do_logout()
    flash(f"Goodbye!", "success")
    return redirect("/login")

@app.route('/region')
def region():
    """If user logged in, route to select GTA region."""
    if g.user:
        return render_template('region/region.html')
        """Otherwise redirect to home."""
    else:
        return redirect("/")


@app.route('/eastend')
def eastend():
    """If user logged in, route to select neighbourhood."""
    if g.user:
        return render_template('region/east-end.html')
        """Otherwise redirect to home."""
    else:
        return redirect("/")

@app.route('/leslieville')
def leslieville():
    """If user logged in, route to form for Leslieville."""
    if g.user:
        neighbourhood = Neighbourhood.query.get(1)
        return render_template('east-end-regions/neighbourhood.html', neighbourhood=neighbourhood)
        """Otherwise redirect to home."""
    else:
        return redirect("/")

@app.route("/map_data", methods=["GET", "POST"])
def post_map_data():
    """If user logged in, on form submit, commit data to database and render template presenting posted data."""
    if g.user:
        if request.method == "POST":

            lat=request.form['lat']
            long=request.form['long']
            neighbourhood=request.form['neighbourhood']
            board=request.form['board-id']
            text=request.form['text-input']
            title=request.form['title']
            url=request.form['imageurl']
            user=g.user.id

            post = Post(user_id=user, board_id=board, neighbourhood_id=neighbourhood, text=text, lat=lat, long=long, title=title, image_url=url)
            db.session.add(post)
            db.session.commit()

            type = Board.query.get(board)
        

        return render_template("/posts/post_data.html", type=type, title=title, lat=lat, long=long, neighbourhood=neighbourhood, text=text, board=board, user=user, url=url)
        """Otherwise redirect to home."""
    else:
        return redirect("/")

@app.route('/neighbourhoods/<int:neighbourhood_id>/read_posts')
def read_posts(neighbourhood_id):
    """If user logged in, render template to present all posts for selected neighbourhood."""
    if g.user:
        ngh = Neighbourhood.query.get_or_404(neighbourhood_id)
        posts = ngh.posts

        return render_template("/posts/read_posts.html", posts=posts)
        """Otherwise redirect to home."""
    else:
        return redirect("/")

@app.route('/posts/<int:post_id>')
def individual_post(post_id):
    """If user logged in, render template for selected post."""
    if g.user:
        post = Post.query.get_or_404(post_id)
        lat = post.lat
        long = post.long

        return render_template("/posts/read_individual_post.html", post=post, lat=lat, long=long)
        """Otherwise redirect to home."""
    else:
        return redirect("/")
    
@app.route('/myposts/<int:post_id>')
def my_post(post_id):
    "If user logged in, render template for selected post owned by user."
    if g.user:
        post = Post.query.get_or_404(post_id)
        lat = post.lat
        long = post.long

        return render_template("/posts/read_my_post.html", post=post, lat=lat, long=long)
        """Otherwise redirect to home."""
    else:
        return redirect("/")

@app.route('/posts/<int:post_id>/delete')
def post_destroy(post_id):
        """Handle post deletion."""
        pst = Post.query.get_or_404(post_id)

        db.session.delete(pst)
        db.session.commit()

        return redirect("/")
 





    

    

    