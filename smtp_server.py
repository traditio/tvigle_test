#coding=utf-8
import smtplib

from pylibmc import ThreadMappedPool

from settings import *


class SmtpServerBase(object):

    @classmethod
    def clone(cls):
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.set_debuglevel(1)
        return server


#мне очень нравится пул коннекшенов от библиотеки pylibmc благодаря
#его удобству и простоте использования. Можно написать самому, но если в проекте
#будет где-то юзаться Memcached и pylibmc, то можно сократить количество кода,
#позаимствовав достаточно универсальный пул коннекшенов от pylibmc
SmtpServer = ThreadMappedPool(SmtpServerBase)

