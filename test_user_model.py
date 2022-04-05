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

        u1 = User.signup("test1", "email1@email.com", "location", "password")
        uid1 = 1111
        u1.id = uid1

        u2 = User.signup("test2", "email2@email.com", "location", "password")
        uid2 = 2222
        u2.id = uid2

        db.session.commit()

        u1 = User.query.get(uid1)
        u2 = User.query.get(uid2)

        self.u1 = u1
        self.uid1 = uid1

        self.u2 = u2
        self.uid2 = uid2

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res


    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            id=1818,
            username="testuser",
            email="test@test.com",
            location="location",
            password="HASHED_PASSWORD" 
            )

        db.session.add(u)
        db.session.commit()

        # User should have no posts
        self.assertEqual(len(u.posts), 0)

    
    # Signup Tests
    #
    ####
    def test_valid_signup(self):
        u_test = User.signup("testtesttest", "testtest@test.com", "location", "password")
        uid = 99999
        u_test.id = uid
        db.session.commit()

        u_test = User.query.get(uid)
        self.assertIsNotNone(u_test)
        self.assertEqual(u_test.username, "testtesttest")
        self.assertEqual(u_test.email, "testtest@test.com")
        self.assertEqual(u_test.location, "location")
        self.assertNotEqual(u_test.password, "password")

        invalid = User.signup(None, "test@test.com", "location", "password")
        uid = 123456789
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_invalid_email_signup(self):
        invalid = User.signup("testtest", None, "location", "password")
        uid = 123789
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()
    
    def test_invalid_password_signup(self):
        with self.assertRaises(ValueError) as context:
            User.signup("testtest", "email@email.com", "location", None)
        
        with self.assertRaises(ValueError) as context:
            User.signup("testtest", "email@email.com", "location", "")