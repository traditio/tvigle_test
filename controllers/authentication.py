import datetime

from sqlalchemy import and_

from controllers.base import Controller
from models.user import User


class AuthenticationController(Controller):
    class UserBlocked(BaseException):
        pass

    def authenticate(self, email, password):
        user = self.session.query(User).filter(and_(User.email == email, User.confirmed_at != None)).first()
        if user.login_attempts > User.LOGIN_ATTEMPTS:
            raise self.UserBlocked
        self.authenticated = user.authenticate(password)
        if not self.authenticated:
            self.set_user_login_attempts(user, user.login_attempts + 1)
            if user.blocked_to:
                raise self.UserBlocked(user.blocked_to)
        if user.login_attempts > 0 and self.authenticated:
            self.set_user_login_attempts(user, 0)
        return self.authenticated


    def set_user_login_attempts(self, user, attempts_num, block_to=None):
        user.login_attempts = attempts_num
        if user.login_attempts > User.LOGIN_ATTEMPTS:
            user.blocked_to = datetime.datetime.now() + datetime.timedelta(hours=24)
        self.session.add(user)
        self.session.commit()
