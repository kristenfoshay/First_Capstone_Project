import os
import requests
from unittest import TestCase

from flask import Flask
from csv import DictReader
from models import db, connect_db, Neighbourhood, Board, User, Post

 
os.environ['DATABASE_URL'] = 'postgresql:///ranger'

from app import app, CURR_USER_KEY

class PostViewTestCase(TestCase):

    def setUp(self):

        db.drop_all()
        connect_db(app)
        db.create_all()

        with open('generator/board.csv') as board:
            db.session.bulk_insert_mappings(Board, DictReader(board))

        with open('generator/neighbourhood.csv') as neighbourhood:
            db.session.bulk_insert_mappings(Neighbourhood, DictReader(neighbourhood))

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    location="Toronto",
                                    password="testuser")
        self.testuser_id = 8989
        self.testuser.id = self.testuser_id

        db.session.commit()

    def test_add_post(self):
        """Can user add a post?"""

        # Since we need to change the session to mimic logging in,
        # we need to use the changing-session trick:

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            # Now, that session setting is saved, so we can have
            # the rest of ours test
            dt={"user_id": self.testuser.id, "board_id": 2, "title": "test title", "neighbourhood_id": 1, "text": "Hello"}

            resp = c.post('/map_data', data=dt)

            print("this is it", resp)
            # Make sure it redirects
            self.assertEqual(resp.status, 302)

            pst = Post.query.one()
            self.assertEqual(pst.text, "Hello")
    
    def test_post_delete(self):

        m = Post(
            id=1234,
            user_id=self.testuser_id,
            board_id=1,
            neighbourhood_id=1, 
            title="a test title",
            text="a test message",
            
        )
        db.session.add(m)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.get("/posts/1234/delete", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)

            m = Post.query.get(1234)
            self.assertIsNone(m)