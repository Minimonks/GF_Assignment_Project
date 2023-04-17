import unittest
from flask import current_app,url_for
from app import create_app, db
import run
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User, Role
from flask_login import current_user, login_user

class BasicsTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

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

    #Tests that a user is able to log in - however doesnt test the page itself... tried doing this to no avail
    def test_user_login(self):
     user = User(Username='testUser', Password=generate_password_hash('testPassword'), Email='Test@Test.co.uk', RoleID=1)
     db.session.add(user)
     db.session.commit()

     with self.app.test_request_context():
         login_user(user)
         self.assertTrue(current_user.is_authenticated)

   
    
 