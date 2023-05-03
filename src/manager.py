from typing import Dict

from .order import Order


class Manager:
    def __init__(self, orders_in_stock: Dict[Order, int]):
        self._orders_in_stock = orders_in_stock
        self._orders: Dict[Order, int] = {}

    @property
    def orders_in_stock(self):
        return self.orders_in_stock

    @orders_in_stock.setter
    def orders_in_stock(self, value):
        self._orders_in_stock = value

    @orders_in_stock.getter
    def orders_in_stock(self):
        return self._orders_in_stock

    @property
    def orders(self):
        return self.orders

    @orders.setter
    def orders(self, value):
        self._orders = value

    @orders.getter
    def orders(self):
        return self._orders

    def get_order_in_stock_by_id(self, id: int):
        for order_in_stock in self.orders_in_stock.keys():
            if order_in_stock.id == id:
                return order_in_stock
        return None

    def check_if_order_is_in_stock(self, order: Order, amount: int) -> bool:
        if self.get_order_in_stock_by_id(order.id) is not None:
            order_in_stock = self.get_order_in_stock_by_id(order.id)
            if self.orders_in_stock[order_in_stock] >= amount:
                return True
            print(f"There is not enough {order_in_stock.name} in stock")
            return False
        print(f"{order.name.title()} are not in stock")
        return False

    def __is_order_in_orders(
        self, order: Order, amount: int, order_in_stock: Order
    ) -> bool:
        if order in self.orders:
            self.orders[order] += amount
            self.orders_in_stock[order_in_stock] -= amount
            print(f"{amount} of {order.name} was added")
            return True
        else:
            self.orders[order] = amount
            self.orders_in_stock[order_in_stock] -= amount
            print(f"{amount} of {order.name} was added")
            return True

    def add_order(self, order: Order, amount: int) -> bool:
        if self.check_if_order_is_in_stock(order, amount):
            order_in_stock = self.get_order_in_stock_by_id(order.id)
            self.__is_order_in_orders(order, amount, order_in_stock)
            return True
        return False

    def __is_order_larger_or_equal__amount(
        self, order: Order, amount: int, order_in_stock: Order
    ) -> bool:
        if self.orders[order] == amount:
            self.orders.pop(order)
            self.orders_in_stock[order_in_stock] += amount
            print(f"{amount} of {order.name} were deleted")
            return True
        elif self.orders[order] > amount:
            self.orders[order] -= amount
            self.orders_in_stock[order_in_stock] += amount
            print(f"{amount} of {order.name} were deleted")
            return True
        return False

    def delete_order(self, order: Order, amount: int) -> bool:
        if order in self.orders:
            order_in_stock = self.get_order_in_stock_by_id(order.id)
            self.__is_order_larger_or_equal__amount(order, amount, order_in_stock)
            print("The quantity to be removed exceeds the order")
            return False
        print(f"{order.name.title()} were not ordered")
        return False
