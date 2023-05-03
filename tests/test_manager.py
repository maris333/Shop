from decimal import Decimal

import pytest
from src.manager import Manager
from src.order import Order


class TestManager:
    @pytest.fixture
    def manager(self) -> Manager:
        orders = {
            Order.create(1, "oranges", Decimal(10)): 100,
            Order.create(2, "bananas", Decimal(10)): 100,
        }
        return Manager(orders)

    @pytest.fixture
    def oranges_order(self) -> Order:
        return Order.create(1, "oranges", Decimal(10))

    def test_get_order_in_stock_by_id(self, manager: Manager, oranges_order: Order):
        assert manager.get_order_in_stock_by_id(oranges_order.id).id == oranges_order.id

    def test_check_if_order_is_in_stock(self, manager: Manager, oranges_order: Order):
        assert manager.check_if_order_is_in_stock(oranges_order, 10) is True

    def test_check_if_order_is_not_in_stock(self, manager: Manager):
        order = Order.create(3, "grapes", Decimal(10))
        assert manager.check_if_order_is_in_stock(order, 10) is False

    def test_check_if_too_little_is_in_stock(
        self, manager: Manager, oranges_order: Order
    ):
        assert manager.check_if_order_is_in_stock(oranges_order, 110) is False

    def test_add_order(self, manager: Manager, oranges_order: Order):
        manager.add_order(oranges_order, 10)
        assert len(manager.orders) == 1

    def test_add_existing_order(self, manager: Manager, oranges_order: Order):
        manager.add_order(oranges_order, 1)
        manager.add_order(oranges_order, 1)
        assert manager.orders[oranges_order] == 2

    def test_add_existing_order_check_if_stock_is_reduced(
        self, manager: Manager, oranges_order: Order
    ):
        manager.add_order(oranges_order, 10)
        order_in_stock = manager.get_order_in_stock_by_id(oranges_order.id)
        assert manager.orders_in_stock[order_in_stock] == 90

    def test_add_existing_order_check_if_not_in_stock(self, manager: Manager):
        order = Order.create(3, "apples", Decimal(10))
        assert not manager.add_order(order, 10)

    def test_add_existing_order_check_if_not_enough_in_stock(
        self, manager: Manager, oranges_order: Order
    ):
        assert not manager.add_order(oranges_order, 110)

    def test_delete_order(self, manager: Manager, oranges_order: Order):
        manager.orders = {oranges_order: 1}
        manager.delete_order(oranges_order, 1)
        assert len(manager.orders) == 0

    def test_delete_more_than_one_order(self, manager: Manager, oranges_order: Order):
        manager.orders = {oranges_order: 3}
        manager.delete_order(oranges_order, 2)
        assert manager.orders[oranges_order], 1

    def test_delete_not_existing_order(self, manager: Manager):
        order = Order.create(3, "apples", Decimal(10))
        assert not manager.delete_order(order, 1)

    def test_delete_existing_order_check_if_stock_is_refilled(
        self, manager: Manager, oranges_order: Order
    ):
        manager.add_order(oranges_order, 10)
        manager.delete_order(oranges_order, 10)
        order_in_stock = manager.get_order_in_stock_by_id(oranges_order.id)
        assert manager.orders_in_stock[order_in_stock] == 100
