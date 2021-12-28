"""
conftest.py
- 여러가지 테스트에서, 반복적으로 쓰이는 부분들, 예를 들어 Store 객체 생성 및 User 객체 생성 등을
이 파일에 생성해놓고, @pytest.fixture 어노테이션을 통해 지정해놓는다.

- 그러면 test_....py 에서 해당 메서드를 불러오면서, 반복적으로 객체 생성 코드를 작성하는, 즉 Given 부분을 작성하는 수고를 줄일 수 있다.
"""
import pytest

from main import GrabStore, Product, User
from GrabRealStore import GrabStore

API_URL = "https://fakestoreapi.com/products"


@pytest.fixture(scope="function")
def mock_products():
    return {
        1: {"title":"키보드", "price":30000},
        2: {"title":"모니터", "price":5000000}
    }


@pytest.fixture(scope="function")
def mock_api(requests_mock, mock_products):
    mock_product1 = mock_products[1]
    mock_product2 = mock_products[2]

    requests_mock.get(f"{API_URL}/1", json=mock_product1)
    requests_mock.get(f"{API_URL}/2", json=mock_product2)

    requests_mock.delete(f"{API_URL}/1", json=mock_product1)
    requests_mock.delete(f"{API_URL}/2", json=mock_product2)


@pytest.fixture(scope="function")
def grab_store():
    """
    @pytest.fixture 데코레이터를 통해서, 함수가 해당 메소드(grab_store) 를 호출할 때마다 실행되게끔 함.
    즉, 함수 실행 횟수가 grab_store 메서드의 실행 단위
    :return: 
    """
    return GrabStore()
    # return GrabStore(
    #     products={
    #         1: Product(title="키보드", price=30000),
    #         2: Product(title="모니터", price=5000000)
    #     }
    # )


@pytest.fixture(scope="function")
def user(grab_store):
    return User(money=100000, store=grab_store)
