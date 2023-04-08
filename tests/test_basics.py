import unittest
from flask import current_app,url_for
from app import create_app, db
import run


class BasicsTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

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
        
    
 