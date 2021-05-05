from unittest import TestCase

from flask import *
from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True


db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):

    def setUp(self):
        User.query.delete()

        user = User(first_name='John', last_name="Smith", img_url='https://i.ytimg.com/vi/7qDws-LCptk/hqdefault.jpg')
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        db.session.rollback()
    
    def test_all_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('John', html)
            self.assertIn('Smith', html)

    def test_new_user(self):
        with app.test_client() as client:
            resp = client.get("/users/new-user")

            self.assertEqual(resp.status_code, 200)

    def test_add_user(self):
        with app.test_client() as client: 
            resp = client.post('/users/new-user', data={
                'first-name':'Steve', 
                'last-name':'Jobs', 
                'img-url':'https://i.ytimg.com/vi/7qDws-LCptk/hqdefault.jpg', 
                'user-form' : ''
            })
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)

            resp = client.post('/users/new-user', data={
                'first-name':'Anna', 
                'last-name':'Squirrel', 
                'img-url':'https://i.ytimg.com/vi/7qDws-LCptk/hqdefault.jpg', 
                'user-form' : ''
            }, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Anna', html)
            self.assertIn('Squirrel', html)
            self.assertIn('https://i.ytimg.com/vi/7qDws-LCptk/hqdefault.jpg', html)

    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.get('/users/1/delete')
            self.assertEqual(resp.status_code, 302)
    
    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.get('/users/5/delete', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('John Smith', html)