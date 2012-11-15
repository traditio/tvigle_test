import os.path

import pystache


class Template(object):
    BASE_PATH = os.path.abspath('templates')
    TEMPLATE_EXT = 'txt'

    def __init__(self, name):
        self.name = name

    def render(self, **locals):
        with open(os.path.join(self.BASE_PATH, '.'.join((self.name, self.TEMPLATE_EXT)))) as f:
            content = f.read().decode('utf-8')
        return pystache.render(content, locals)

