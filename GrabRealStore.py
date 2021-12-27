import requests

from main import Store, Product


class GrabStore(Store):
    def __init__(self, url="https://fakestoreapi.com"):
        self._money = 0
        self.name = "그랩마켓"
        self.url = url

    def show_product(self, product_id):
        res = requests.get(f"{self.url}/products/{product_id}")
        product = res.json()

        return Product(product["title"], price=product["price"])

    def _take_money(self, money):
        self._money += money

    def sell_product(self, product_id, money):
        product = self.show_product(product_id=product_id)

        if not product:
            raise Exception("상품이 없습니다")

        self._take_money(money=money)
        try:
            _product = self._take_out_product(product_id=product_id)
        except Exception as e:
            self._return_money(money)
            raise e

        return _product

    def _take_out_product(self, product_id):
        res = requests.delete(url=f"{self.url}/products/{product_id}")
        product = res.json()
        return Product(name=product["title"], price=product["price"])

    def _return_money(self, money):
        self._money -= money


if __name__ == "__main__":
    store = GrabStore()
    result = store.show_product(product_id=1)
    print(result)