import dataclasses
import requests
from abc import abstractmethod, ABC


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


@dataclasses.dataclass
class Product:
    """
    product 객체 생성을 쉽게하도록 하는 클래스
    """
    title: str
    price: int


class GrabStore(Store):
    def __init__(self, url="https://fakestoreapi.com"):
        self._money = 0
        self.name = "그랩마켓"
        self.url = url

    def show_product(self, product_id):
        """
        외부 의존성이 있음.
        테스트에는 mock 을 사용하고 싶다면?
        """
        res = requests.get(f"{self.url}/products/{product_id}")
        product = res.json()

        return Product(title=product["title"], price=product["price"])

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
        return Product(title=product["title"], price=product["price"])

    def _return_money(self, money):
        self._money -= money


if __name__ == "__main__":
    store = GrabStore()
    result = store.show_product(product_id=1)
    print(result)
