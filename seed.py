from csv import DictReader
from app import db
from models import Board, Neighbourhood


db.drop_all()
db.create_all()

with open('generator/board.csv') as board:
    db.session.bulk_insert_mappings(Board, DictReader(board))

with open('generator/neighbourhood.csv') as neighbourhood:
    db.session.bulk_insert_mappings(Neighbourhood, DictReader(neighbourhood))


db.session.commit()
