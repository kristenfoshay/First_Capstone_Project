from datetime import datetime
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

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

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

    @classmethod
    def authenticate(cls, username, password):
  

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


class Board(db.Model):
   
    __tablename__ = 'board'

    id = db .Column(
        db.Integer,
        primary_key=True,
    )

    name = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

##class Area(db.Model):

    ## __tablename__ = 'area'
    
##id = db .Column(
        ##db.Integer,
       ## primary_key=True,
    ##)

##name = db.Column(
        ##db.Text,
       ## nullable=False,
        ##unique=True,
   ## )

class Post(db.Model):

    __tablename__ = 'post'
    
    id = db .Column(
        db.Integer,
        primary_key=True,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )

    board_id = db .Column(
        db.Integer,
        db.ForeignKey('board.id', ondelete='CASCADE'),
        nullable=False,
    )

    lat = db.Column(
        db.Integer,
        nullable=False,
        unique=True,
    )

    long = db.Column(
        db.Integer,
        nullable=False,
        unique=True,
    )

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow(),
    )

## at the end

def connect_db(app):

    db.app = app
    db.init_app(app)