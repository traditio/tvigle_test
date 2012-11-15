import unittest
import datetime

from controllers.authentication import AuthenticationController
from controllers.registration import RegistrationController
from models.user import User
from session import Session


class AuthorizationTest(unittest.TestCase):
    def setUp(self):
        self.session = Session()
        self.session.query(User).delete()
        self.email = 'user@localhost.com'
        reg_controller = RegistrationController(self.session)
        self.password = 'qwerty'
        token = reg_controller.register(self.email, self.password)
        reg_controller.confirm(self.email, token)
        self.controller = AuthenticationController(self.session)

    def test_login_attempts(self):
        self.controller.authenticate(self.email, self.password)
        user = self.session.query(User).first()
        with self.assertRaises(self.controller.UserBlocked):
            for _ in xrange(User.LOGIN_ATTEMPTS + 1):
                self.controller.authenticate(self.email, '')
        user = self.session.query(User).first()
        self.assertGreater(user.blocked_to, datetime.datetime.now())

    def test_authentication(self):
        self.controller.authenticate(self.email, self.password)
        user = self.session.query(User).first()
        self.assert_(self.controller.authenticate(self.email, self.password))
