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

    location = db.Column(
        db.Text, 
        nullable=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    posts = db.relationship('Post', backref='users')

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

    @classmethod
    def signup(cls, username, email, location, password, ):
        """Sign up user.
        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            location=location,
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

    posts = db.relationship('Post', backref='board')

    
class Neighbourhood(db.Model):

    __tablename__ = 'neighbourhood'
    
    id = db .Column(
        db.Integer,
        primary_key=True,
    )

    name = db.Column(
        db.String,
        nullable=True,
        unique=True,
    )

    posts = db.relationship('Post', backref='neighbourhood')

    def __repr__(self):
        return f'<Neighbourhood: {self.name}>'


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

    neighbourhood_id = db .Column(
        db.Integer,
        db.ForeignKey('neighbourhood.id', ondelete='CASCADE'),
        nullable=False,
    )

    title = db.Column(
        db.String,
        nullable=False,
    )

    text = db.Column(
        db.String,
        nullable=False,
    )

    lat = db.Column(
        db.Float,
        nullable=True,
    )

    long = db.Column(
        db.Float,
        nullable=True,
    )

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow(),
    )

    image_url = db.Column(
        db.Text,
        nullable=True
    )

    def __repr__(self):
        return f'<Post: {self.timestamp} {self.title}>'

## at the end

def connect_db(app):

    db.app = app
    db.init_app(app)