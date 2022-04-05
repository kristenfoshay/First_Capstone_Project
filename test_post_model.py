import os
from unittest import TestCase
from sqlalchemy import exc
from flask import Flask
from csv import DictReader
from models import db, connect_db, Neighbourhood, Board, User, Post

os.environ['DATABASE_URL'] = 'postgresql:///ranger'

from app import app

db.create_all()

class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        connect_db(app)
        db.create_all()

        with open('generator/board.csv') as board:
            db.session.bulk_insert_mappings(Board, DictReader(board))

        with open('generator/neighbourhood.csv') as neighbourhood:
            db.session.bulk_insert_mappings(Neighbourhood, DictReader(neighbourhood))

        self.uid = 94566
        u = User.signup("testing", "testing@test.com", "Toronto", "password")
        u.id = self.uid
        db.session.commit()

        self.u = User.query.get(self.uid)

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_message_model(self):
        """Does basic model work?"""
        
        m = Post(
            id=2121,
            user_id=self.uid,
            board_id=1,
            neighbourhood_id=1,
            title="testing_title",
            text="a post",
        )

        db.session.add(m)
        db.session.commit()

        # User should have 1 post
        self.assertEqual(len(self.u.posts), 1)
        self.assertEqual(self.u.posts[0].text, "a post")
