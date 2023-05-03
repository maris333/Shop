from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Order:
    __create_key = object()

    @classmethod
    def create(cls, id, name, price):
        return Order(cls.__create_key, id, name, price)

    def __init__(self, create_key, id: int, name: str, price: Decimal):
        assert (create_key == Order.__create_key)
        self._id = id
        self._name = name
        self._price = price

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._id

    def __hash__(self):
        return hash((self._id, self._name, self._price))

    def __eq__(self, other):
        if isinstance(other, Order):
            return (self._id, self._name, self._price) == (
                other.id,
                other.name,
                other.price,
            )
        return False
