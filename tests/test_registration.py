import unittest

from sqlalchemy import and_

from controllers.registration import RegistrationController
from models.user import User
from session import Session


class RegistrationTest(unittest.TestCase):
    def setUp(self):
        self.session = Session()
        self.session.query(User).delete()
        self.email = 'user@localhost.com'
        self.controller = RegistrationController(self.session)
        self.token = self.controller.register(self.email, 'qwerty')

    def test_registration(self):
        self.assertEqual(self.session.query(User).filter(and_(User.email == self.email, User.confirmed_at == None)).count(), 1)

    def test_confirmation(self):
        self.controller.confirm(self.email, self.token)
        self.assertEqual(self.session.query(User).filter(and_(User.email == self.email, User.confirmed_at != None)).count(), 1)

