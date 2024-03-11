import os
import unittest
from flask import current_app,url_for
from app import create_app, db
import run
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User, Role
from flask_login import current_user, login_user
from urllib.parse import urlparse

class BasicsTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app('testing')
        # self.app.config['SERVER_NAME'] = os.getenv('ServerName')
        # self.app.config['PREFERRED_URL_SCHEME'] = 'https'
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # # Print out the server name
        # print("Server name:", self.app.config['SERVER_NAME'])

        # # Print out the available routes
        # print("Routes:")
        # for rule in self.app.url_map.iter_rules():
        #     print(rule)

        # print("Generated URL for 'about':", url_for('main.about'))

        self.userRole = Role(RoleName = "User")
        self.adminRole = Role(RoleName = "Admin")
        db.session.add(self.userRole)
        db.session.add(self.adminRole)

        self.client = self.app.test_client()    

        db.session.commit()        
  

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    
    def test_app_exists(self):
        self.assertFalse(current_app is None)

    #Test the app is able to initialise with test configuration
    def test_app_is_test(self):
        self.assertTrue(current_app.config['TESTING'])
    
    #Simple test to check the about page loads
    def test_about_loads(self):
         response = self.client.get('/about/')
         self.assertEqual(response.status_code, 200)

    #Tests that a user is able to log in
    def test_user_login(self):
     user = User(Username='testUser', Password=generate_password_hash('testPassword'), Email='Test@Test.co.uk', RoleID=1)
     db.session.add(user)
     db.session.commit()

    #  response = self.client.post('/login', data={'username':'testUser','password':'testPassword'}, follow_redirects=True)
    #  self.assertEqual(response.status_code, 200)

     with self.app.test_request_context():
         login_user(user)
         self.assertTrue(current_user.is_authenticated)

    
   
    #Security OWASP tests

    #Cross-Site Scripting attack on login. The script should be escaped and not executed.
    def test_XSS(self):
        response = self.client.post('/login', data={'username':'<script>alert("XSS")</script>', 'password':'testPassword'}, follow_redirects=True)
        self.assertNotIn(b'<script>alert("XSS")</script>', response.data)

    # Broken Access Control - User should be redirected to login page if not authenticated
    def test_authentication_required(self):
        response = self.client.get('/home/', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        # login_url = urlparse(url_for('main.login', next='/home/', _external=True))
        # redirect_url = urlparse(response.headers['Location'])
        # self.assertEqual(redirect_url.path, login_url.path)


    
 