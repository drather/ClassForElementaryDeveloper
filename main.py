"""
상황
1. 다른 Store 가 들어오면 어떻게 할까?
    - Store 를 추상화(상위 개념을 하나 만들어서, 객체들의 공통적인 특징을 모아놓음)
    - User 가 Store 에 대한 의존성을 주입받아야 한다.
"""


class GrabStore:
    def __init__(self):
        self.money = 0
        self.name = "그랩마켓"
        self.products = {
            1: {"name": "키보드", "price": 30000},
            2: {"name": "모니터", "price": 50000},
        }

    def set_money(self, money):
        self.money = money

    def set_products(self, products):
        self.products = products

    def get_money(self):
        return self.money

    def get_products(self):
        return self.products


class User:
    def __init__(self):
        self.money = 0
        self.store = GrabStore()
        self.belongs = []

    def set_money(self, money):
        self.money = money

    def set_belongs(self, belongs):
        self.belongs = belongs

    def get_money(self):
        return self.money

    def get_belongs(self):
        return self.belongs

    def get_store(self):
        return self.store

    def see_product(self, product_id):
        products = self.store.get_products()
        return products[product_id]

    def purchase_product(self, product_id):
        product = self.see_product(product_id)
        if self.money >= product["price"]:
            self.store.products.pop(product_id)  # 상점에서 상품 꺼내기
            self.money -= product["price"]  # 사용자가 돈 내기
            self.store.money += product["price"]  # 상점에서 돈 받기
            self.belongs.append(product)
            return product
        else:
            raise Exception("잔돈이 부족합니다")


if __name__ == "__main__":
    user = User()
    user.set_money(100000)
    user.purchase_product(product_id=1)