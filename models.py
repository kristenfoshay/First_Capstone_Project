from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    image_url = db.Column(
        db.Text,
        default="/static/images/default-pic.png",
    )

    location = db.Column(
        db.Text, 
        nullable=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    @classmethod
    def signup(cls, username, email, location, image_url, password, ):
        """Sign up user.
        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            location=location,
            image_url=image_url,
            password=hashed_pwd,
            
        )

        db.session.add(user)
        return user

## at the end

def connect_db(app):

    db.app = app
    db.init_app(app)