#coding=utf-8
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


    def set_user_login_attempts(self, user, attempts_num):
        user.login_attempts = attempts_num
        if user.login_attempts > User.LOGIN_ATTEMPTS:
            user.blocked_to = datetime.datetime.now() + datetime.timedelta(hours=24)
        #значит мы сбрасываем кол-во попыток входа юзера
        if attempts_num == 0:
            user.blocked_to = None
        self.session.add(user)
        self.session.commit()
