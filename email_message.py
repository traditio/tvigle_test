from smtp_server import SmtpServer


class EmailMessage(object):
    DEFAULT_FROM = 'user@localhost'

    def __init__(self, text):
        self.text = text

    def send(self, to, from_=DEFAULT_FROM):
        msg = "From: %s\r\nTo: %s\r\n\r\n" % (from_, to) + self.text
        with SmtpServer.reserve() as server:
            server.sendmail(to, from_, msg.encode('utf-8'))