

class NameNotFoundException(Exception):
    def __init__(self, name):
        Exception.__init__(self, name)
        self.name = name
