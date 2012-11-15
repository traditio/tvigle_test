#coding=utf-8
import datetime
import re

from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError

from controllers.base import Controller
from email_activation_token import EmailActivationToken
from email_message import EmailMessage
from models.user import User
from sha256 import Sha256
from template import Template


class RegistrationController(Controller):
    class InvalidActivationToken(BaseException):
        pass

    def _token_salt(self, email, password):
        return Sha256(''.join((email, password))).hexdigest()

    def register(self, email, password):
        user = User(email, password)
        self.session.add(user)
        try:
            self.session.commit()
        except IntegrityError, e:
            #проверяем что ошибка возникла из-да дублирования email, а не по какой-то другой причине
            if not re.search(r'email is not unique', e.message): raise
            #мы не будем проверять дополнительным запросом наличие юзера с таким же емайлом,
            #пусть база сама проверит, а мы словим IntegrityError
            user = self.session.query(User).filter(and_(User.email == email, User.confirmed_at == None)).first()
            if not user: raise User.AlreadyConfirmed(email)
        token = EmailActivationToken(self._token_salt(email, user.password)).generate()
        text = Template('email/activate').render(email=email, token=token)
        EmailMessage(text).send(email)
        return token

    def confirm(self, email, token):
        user = self.session.query(User).filter(User.email == email).first()
        if user is None:
            raise User.NotFound(email)
        if user.confirmed_at is not None:
            raise User.AlreadyConfirmed(email)
        if EmailActivationToken(self._token_salt(user.email, user.password)).check(token):
            user.confirmed_at = datetime.datetime.now()
            self.session.add(user)
            self.session.commit()
        else:
            raise self.InvalidActivationToken(token)


