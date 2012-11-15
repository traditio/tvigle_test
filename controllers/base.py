from session import Session


class Controller(object):
    def __init__(self, session=None):
        self.session = session if session else Session()