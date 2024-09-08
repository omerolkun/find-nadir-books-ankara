class Book:
    def __init__(self, name, author, price):
        self._name = name
        self._author = author
        self._price = price

    def set_name(self, name):
        self._name = name

    def get_name(self):
        return self._name
