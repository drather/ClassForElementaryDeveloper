"""
문제 제기 1. 다른 Store 가 들어오면 어떻게 할까?
    - Store 를 추상화(상위 개념을 하나 만들어서, 객체들의 공통적인 특징을 모아놓음)
    - User 가 Store 에 대한 의존성을 주입받아야 한다.

문제 제기 2: User 가 Store 에 있는 상품과 돈에 마음대로 접근할 수 있다.
    - Store 의 책임을 정의하고, 캡술화한다.
    - User 의 결제 로직을 수정한다.
    - User 도 캡슐화하자.

    => User 가 Store 의 속성에 직접 접근하지 못하게 함. 즉, 캡슐화
    => 또한, get, set 등이 메서드 이름을 좀 더 도메인에 맞게 수정함.

문제 제기 3: User 가 많은 행위를 책임지고 있다. Store 가 판매에 대한 책임을 가져야 한다.
    -  상점에서 상품을 판매하는 행위를 추상화하고, 구체적인 로직은 Store 의 메서드로 옮긴다.

문제 제기 4: product 가 책임을 가지게끔 하자.
    - 딕셔너리 타이을 클래스(데이터 클래스) 객체로 변환하자.

외부 의존성 대체
- 1강: DB 를 대체할 수 있는 fakestoreapi.com 에 requests 모듈을 통해 request, response 를 받는다.
"""

import dataclasses
import traceback
from abc import ABC, abstractmethod

from GrabRealStore import GrabStore


@dataclasses.dataclass
class Product:
    """
    product 객체 생성을 쉽게하도록 하는 클래스
    """
    name: str
    price: int


class Store(ABC):
    @abstractmethod
    def __init__(self):
        self._money = 0
        self.name = ""
        self._products = {}

    @abstractmethod
    def show_product(self, product_id):
        """
        사용자에게 상품 보여주는 메서드
        :param product_id:
        :return:
        """
        pass

    @abstractmethod
    def sell_product(self, product_id, money):
        """
        상점이 사용자에게 물건을 판매하는 행위
        Validation 코드는 최소화
        :param product_id:
        :param money:
        :return:
        """
        pass


class User:
    def __init__(self, money, store: Store):
        self._money = money
        self._store = store
        self._belongs = []

    def get_money(self):
        return self._money

    def get_belongs(self):
        return self._belongs

    def get_store(self):
        return self._store

    def see_product(self, product_id):
        products = self._store.show_product(product_id=product_id)
        return products

    def _give_money(self, money):
        if self._money < money:
            raise Exception("위그든씨, 나는 돈이 없습니다.")
        else:
            self._money -= money

    def _take_money(self, money):
        self._money += money

    def _add_belongs(self, belongs):
        self._belongs.append(belongs)

    def purchase_product(self, product_id):
        product = self.see_product(product_id=product_id)
        price = product.price
        if self._check_money_enough(price):
            self._give_money(money=price)
            try:
                my_product = self._store.sell_product(product_id=product_id, money=price)
                self._add_belongs(my_product)
                return product

            except Exception as e:
                self._take_money(money=price)
                print(f"구매 중 문제가 발생했습니다: {e}")
                print(traceback.format_exc())

        else:
            raise Exception("잔돈이 부족합니다")

    def _check_money_enough(self, price):
        return self._money >= price


if __name__ == "__main__":
    store = GrabStore(
        products={
            1: Product(name="키보드", price=30000),
            2: Product(name="모니터", price=5000000)
        }
    )

    user = User(money=100000, store=store)
    user.purchase_product(product_id=2)

    print(f"user가 구매한 상품: {user.get_belongs()} ")
    print(f"user 의 잔돈: {user.get_money()}")



