import unittest
import datetime

from models.user import User, Permission
from session import Session


class PermissionsTest(unittest.TestCase):
    def setUp(self):
        self.session = Session()
        self.session.query(User).delete()
        self.user = User('user@localhost.com', 'qwerty')
        self.user.confirmed_at = datetime.datetime.now()
        self.user.perms = [Permission(self.user, 'foo'), Permission(self.user, 'bar'),]
        self.session.add(self.user)
        self.session.commit()

    def test_has_perm(self):
        self.assert_(self.user.has_perm('foo'))

    def test_has_no_perm(self):
        self.failIf(self.user.has_perm(''))

    def test_add_perm(self):
        self.user.add_perm('baz')
        self.session.commit()
        self.assert_(self.user.has_perm('baz'))

    def test_remove_perm(self):
        self.user.add_perm('baf')
        self.session.commit()
        self.assert_(self.user.has_perm('baf'))
        self.user.remove_perm('baf')
        self.session.commit()
        self.failIf(self.user.has_perm('baf'))
