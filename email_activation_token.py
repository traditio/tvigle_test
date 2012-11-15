#coding=utf-8
import datetime
import logging

from sha256 import Sha256


class EmailActivationToken(object):
    """Нет никакого смысла хранить одноразовые ключи в БД - они занимают место, а используются всего
    один раз. Но мы можем использовать значимую информацию, уже хранящуюся в БД и из нее сделать соль.
    Место заниматься не будет, а токены будут обладать сроком действия и можно будет проверить их валидность.
    """
    DEFAULT_EXPIRE_DAYS = 10

    def __init__(self, salt):
        self.salt = salt

    def generate(self, expiration_date=None):
        if expiration_date is None:
            expiration_date = datetime.date.today() + datetime.timedelta(days=self.DEFAULT_EXPIRE_DAYS)
        res = self._sign(expiration_date.strftime('%y%m%d'))
        logging.debug('Generate token salt=%s expiration_date=%s token=%s', self.salt, expiration_date, res)
        return res

    def check(self, token):
        date, sign = token[:6], token[6:]
        logging.debug('Check token salt=%s token=%s', self.salt, token)
        return token == self._sign(date)

    def _sign(self, date_str):
        return ''.join((date_str, Sha256(''.join((date_str, self.salt))).hexdigest()))
