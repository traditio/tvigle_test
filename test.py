#coding=utf-8
import os
import signal
import unittest

from settings import *


if __name__ == '__main__':
    #Запускаем отладочный почтовый сервер для перехвата сообщений
    pid = os.spawnlp(os.P_NOWAIT, 'python', 'python', '-m', 'smtpd', '-n', '-c', 'DebuggingServer', '{}:{}'.format(SMTP_HOST, SMTP_PORT))
    try:
        #http://stackoverflow.com/questions/3295386/python-unittest-and-discovery
        loader = unittest.TestLoader()
        tests = loader.discover('tests')
        testRunner = unittest.runner.TextTestRunner()
        testRunner.run(tests)
    finally:
        os.kill(pid, signal.SIGKILL)
