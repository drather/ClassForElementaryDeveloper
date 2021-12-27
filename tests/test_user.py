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

