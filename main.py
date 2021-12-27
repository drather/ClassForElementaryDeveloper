"""
상황
문제 제기 1. 다른 Store 가 들어오면 어떻게 할까?
    - Store 를 추상화(상위 개념을 하나 만들어서, 객체들의 공통적인 특징을 모아놓음)
    - User 가 Store 에 대한 의존성을 주입받아야 한다.

문제 제기 2: User 가 Store 에 있는 상품과 돈에 마음대로 접근할 수 있다.
    - Store 의 책임을 정의하고, 캡술화한다.
    - User 의 결제 로직을 수정한다.
    - User 도 캡슐화하자.

    => User 가 Store 의 속성에 직접 접근하지 못하게 함. 즉, 캡슐화
    => 또한, get, set 등이 메서드 이름을 좀 더 도메인에 맞게 수정함.
"""
from abc import ABC, abstractmethod


class Store(ABC):
    @abstractmethod
    def __init__(self):
        self.money = 0
        self.name = ""
        self.products = {}

    @abstractmethod
    def show_product(self, product_id):
        """
        사용자에게 상품 보여주는 메서드
        :param product_id:
        :return:
        """
        pass

    @abstractmethod
    def give_product(self, product_id):
        """
        사용자에게 상품 주는 메서드
        :param product_id:
        :return:
        """

    @abstractmethod
    def take_money(self, money):
        """
        사용자에게 돈 받는 메서드
        :param money:
        :return:
        """
        pass


class GrabStore(Store):
    def __init__(self, products):
        self._money = 0
        self.name = "그랩마켓"
        self._products = products

    def set_money(self, money):
        self._money = money

    def set_products(self, products):
        self._products = products

    def show_product(self, product_id):
        return self._products[product_id]

    def give_product(self, product_id):
        self._products.pop(product_id) # products id 에 product_id 를 key 로 가지는 value 를 지운다.

    def take_money(self, money):
        self._money += money


class User:
    def __init__(self, money, store: Store):
        self.money = money
        self.store = store
        self.belongs = []

    def get_money(self):
        return self.money

    def get_belongs(self):
        return self.belongs

    def get_store(self):
        return self.store

    def see_product(self, product_id):
        products = self.store.show_product(product_id=product_id)
        return products

    def purchase_product(self, product_id):
        product = self.see_product(product_id=product_id)
        if self.money >= product["price"]:
            self.store.give_product(product_id=product_id)  # 상점에서 상품 꺼내기
            self.money -= product["price"]  # 사용자가 돈 내기
            self.store.take_money(product["price"])  # 상점에서 돈 받기
            self.belongs.append(product)
            return product
        else:
            raise Exception("잔돈이 부족합니다")


if __name__ == "__main__":
    store = GrabStore(
        products={
            1: {"name": "키보드", "price": 30000},
            2: {"name": "모니터", "price": 50000}
        }
    )

    user = User(money=100000, store=store)

    user.purchase_product(product_id=1)

    print(f"user가 구매한 상품: {user.get_belongs()} ")




