class Book:
    def __init__(self, name, author, price, seller=None):
        self._name = name
        self._author = author
        self._price = price
        self._seller = seller

    def set_name(self, name):
        self._name = name

    def get_name(self):
        return self._name
    
    def get_author(self):
        return self._author

    def get_price(self):
        return self._price

    def get_seller(self):
        return self._seller
    

    def __str__(self):
        return f"Name: {self._name}, Author: {self._author}, Price: {self._price}, Seller: {self._seller}"
