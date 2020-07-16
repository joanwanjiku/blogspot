import unittest
from app.models import User

class TestUser(unittest.TestCase):

    def setUp(self):
        self.user = User(password = 'foobar')

    def test_no_access_password(self):
        with self.assertRaises(AttributeError):
            self.user.password

    def test_password_setter(self):
        self.assertTrue(self.user.hash_password is not None)

    def test_password_verification(self):
        self.assertTrue(self.user.verify_password('foobar'))
