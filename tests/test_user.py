"""
User 관련 테스트
"""


# Unit 테스트
import pytest


def test_check_money_enough(user):
    cheap_price = 500
    expensive_price = 999999999

    can_buy = user._check_money_enough(price=cheap_price)
    assert can_buy

    can_buy = user._check_money_enough(price=expensive_price)
    assert not can_buy


def test_give_money(user):
    price = 500
    pre_money = user._money

    user._give_money(money=price)

    assert user._money == pre_money - price


# Integration test
def test_purchase_product_well(user):
    """
    1. 유저 돈 잘 냈나?
    2. 유저의 주머니에 상품이 들어 갔는가?
    :param user:
    :return:
    """
    product_id = 1
    pre_user_money = user._money

    product = user.purchase_product(product_id=product_id)

    assert user._money == pre_user_money - product.price
    assert user.get_belongs() == [product]


def test_purchase_product_expensive(user):
    # price 500,000
    product_id = 2

    with pytest.raises(Exception):
        user.purchase_product(product_id=product_id)

