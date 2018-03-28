
class onupdate():
    def __init__(self):
        self._limit = 8
        self._option = 'offline'

    @property
    def limit(self):
        return self._limit

    @limit.setter
    def limit(self, x):
        self._limit = x

    @property
    def option(self):
        return self._option

    @option.setter
    def option(self, opt):
        self._option = opt
