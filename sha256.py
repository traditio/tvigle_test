import hashlib


class Sha256(object):
    def __init__(self, text):
        self.text = text

    def hexdigest(self):
        sha = hashlib.sha256()
        sha.update(self.text)
        return sha.hexdigest()
