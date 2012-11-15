#coding=utf-8
import re

from sqlalchemy import *
from sqlalchemy.orm import relationship, validates
from sqlalchemy.sql.functions import current_timestamp

from session import Base
from sha256 import Sha256


class User(Base):
    #http://www.regular-expressions.info/email.html
    EMAIL_RE = re.compile(r"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+(?:[A-Z]{2}|com|org|net|edu|gov|mil|biz|info|mobi|name|aero|asia|jobs|museum)\b")
    LOGIN_ATTEMPTS = 3 #кол-во попыток входа перед блокировкой
    BLOCK_HRS = 24 #кол-во часов на которые пользователь блокируется

    class AlreadyExists(BaseException):
        pass

    class AlreadyConfirmed(BaseException):
        pass

    class NotFound(BaseException):
        pass

    class EmailValidationError(BaseException):
        pass

    class PasswordValidationError(BaseException):
        pass

    __tablename__ = 'users'

    #целочисленный id здесь необязателен, но некоторые библиотеки не умеют работать  со строковыми Primary key
    id = Column(Integer, primary_key=True)
    email = Column(String(50), index=True, unique=True, nullable=False)
    _password = Column(String(32), nullable=False) #размер sha256 - 32 байта
    created_at = Column(DateTime(), default=current_timestamp(), nullable=False)
    #у неподтвержденного юзера confirmed_at == None
    confirmed_at = Column(DateTime())
    login_attempts = Column(Integer(), default=0, nullable=False)
    blocked_to = Column(DateTime(), nullable=True)
    perms = relationship("Permission", lazy='dynamic')

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.authenticated = False

    def has_perm(self, permission):
        return self.perms.filter(Permission.permission == permission).first()

    def add_perm(self, perm):
        self.perms.append(Permission(self, perm))

    def remove_perm(self, perm):
        self.perms.filter(Permission.permission == perm).delete()

    @property
    def password(self):
        return self._password

    #noinspection PyPropertyDefinition
    @password.setter
    def password(self, password):
        #циферки длины пароля от балды
        #мы не можем выполнить проверку этого поля через декоратор validates
        #так в ф-цию декорированную validates передается уже измененное значение
        if not 3 <= len(password) < 30:
            raise self.PasswordValidationError(password)
        self._password = Sha256(password).hexdigest()
        return self._password

    @validates('email')
    def _validate_email(self, key, email):
        """К сожалению, валидаторы в SqlAlchemy позволяют только вызывать исключения или изменять
        значения. Это не так удобно как в Django ORM, когда можно провалидировать несколько полей
        сразу, но тоже сгодится как черновой вариант
        """
        if self.EMAIL_RE.match(email):
            return email
        raise self.EmailValidationError(email)

    def authenticate(self, password):
        self.authenticated = (Sha256(password).hexdigest() == self._password)
        return self.authenticated


class Permission(Base):
    """Права пользователя - это всего лишь строки с произвольным текстом,
        принадлежащие пользователю
    """
    __tablename__ = 'perms'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    permission = Column(String(64), nullable=False)
    user = relationship(User, primaryjoin=user_id == User.id)

    def __init__(self, user, permission):
        self.user_id = user.id
        self.permission = permission
