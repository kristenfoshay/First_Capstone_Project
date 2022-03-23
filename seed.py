from flask import Flask
from csv import DictReader
from models import db, connect_db, Neighbourhood, Board 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ranger'

connect_db(app)
db.create_all()

with open('generator/board.csv') as board:
    db.session.bulk_insert_mappings(Board, DictReader(board))

with open('generator/neighbourhood.csv') as neighbourhood:
    db.session.bulk_insert_mappings(Neighbourhood, DictReader(neighbourhood))

db.session.commit()
