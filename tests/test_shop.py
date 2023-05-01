from decimal import Decimal

import pytest
from manager import Manager
from order import Order


@pytest.fixture
def manager():
    orders = {
        Order(1, "oranges", Decimal(10)): 100,
        Order(2, "bananas", Decimal(10)): 100,
    }
    return Manager(orders)


@pytest.fixture
def oranges_order():
    return Order(1, "oranges", Decimal(10))


def test_get_order_in_stock_by_id(manager, oranges_order):
    assert manager.get_order_in_stock_by_id(oranges_order.id).id == oranges_order.id


def test_check_if_order_is_in_stock(manager, oranges_order):
    assert manager.check_if_order_is_in_stock(oranges_order, 10) is True


def test_check_if_order_is_not_in_stock(manager):
    order = Order(3, "grapes", Decimal(10))
    assert manager.check_if_order_is_in_stock(order, 10) is False


def test_check_if_too_little_is_in_stock(manager, oranges_order):
    assert manager.check_if_order_is_in_stock(oranges_order, 110) is False


def test_add_order(manager, oranges_order):
    manager.add_order(oranges_order, 10)
    assert len(manager.orders) == 1


def test_add_existing_order(manager, oranges_order):
    manager.add_order(oranges_order, 1)
    manager.add_order(oranges_order, 1)
    assert manager.orders[oranges_order] == 2


def test_add_existing_order_check_if_stock_is_reduced(manager, oranges_order):
    manager.add_order(oranges_order, 10)
    order_in_stock = manager.get_order_in_stock_by_id(oranges_order.id)
    assert manager.orders_in_stock[order_in_stock] == 90


def test_add_existing_order_check_if_not_in_stock(manager):
    order = Order(3, "apples", Decimal(10))
    assert not manager.add_order(order, 10)


def test_add_existing_order_check_if_not_enough_in_stock(manager, oranges_order):
    assert not manager.add_order(oranges_order, 110)


def test_delete_order(manager, oranges_order):
    manager.orders = {oranges_order: 1}
    manager.delete_order(oranges_order, 1)
    assert len(manager.orders) == 0


def test_delete_more_than_one_order(manager, oranges_order):
    manager.orders = {oranges_order: 3}
    manager.delete_order(oranges_order, 2)
    assert manager.orders[oranges_order], 1


def test_delete_not_existing_order(manager):
    order = Order(3, "apples", Decimal(10))
    assert not manager.delete_order(order, 1)


def test_delete_existing_order_check_if_stock_is_refilled(manager, oranges_order):
    manager.add_order(oranges_order, 10)
    manager.delete_order(oranges_order, 10)
    order_in_stock = manager.get_order_in_stock_by_id(oranges_order.id)
    assert manager.orders_in_stock[order_in_stock] == 100
