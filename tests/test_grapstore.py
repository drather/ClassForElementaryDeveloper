"""
1강.
통합 테스트 대상은 다음과 같음
- User: purchase_product()
- Store: sell_product()

그 하위 기능은 유닛 테스트로 진행

테스트 명령은 다음 두가지가 있음(동일함)
- python -m pytest tests: tests 디렉토리는 테스트코드를 모아놓은 디렉토리(약속된 이름)
- python -m pytest tests/test_grapstore.py (해당 코드만 테스트 실행)

2강.
- grab_store 를 생성하는 과정에서, 코드 중복이 발생한다.
- 이를 없애고, 편하게 사용하고자 conftest.py 를 만든다.

3강.
- 하나의 테스트 코드에서는 하나의 assert 만 작성하는 것이 좋다.
- 테스트 코드를 작성하다보면, 예외 사항을 좀 더 꼼꼼이 생각하게 된다.

외부의존성 대체 2강
- 외부 API 에서 오는 값은 우리가 통제할 수 없음(외부이므로)
- delete, update 등은 기존 데이터에 영향을 주기 때문에, 할 수 없음
- 따라서, mocking 이 필요하며, 예측할 수 있는 값이 필요함.
- 따라서, 외부와 실제로 통신하면 안됨
- mock.patch() 를 사용해서 외부와 통신하는 코드가 실제로 호출되지 않도록 할 수 있음!
"""
import pytest

from main import GrabStore, Product
from unittest import mock

from tests.conftest import API_URL


def test_show_product(requests_mock, grab_store, mock_products):
    """
    파라미터로 주어진 grab_store 가, conftest.py 에서 grab_store 메서드를 의미한다.
    그럼, grab_store() 메서드가 실행되어 GrabStore 객체를 리턴하게 된다.
    :param grab_store:
    :return:
    """
    # Given
    product_id = 1
    mock_product = mock_products[product_id]

    # When
    # 외부 의존성 대체 3강
    # with: 컨텍스트 매니저
    # # request.get 이 호출되면, mock_api 로 컨트롤하겠다는 뜻
    # with mock.patch("requests.get") as mock_api:
    #     # request.get 호출되면,
    #     # mock 객체가 이에 응답하여 미리 정해진 응답을 주게 된다.
    #     res = mock_api.return_value
    #     res.status_code = 200
    #
    #     # 결과값은 res.status_code 로 접근 가능
    #     # res.json() 메소드의 결과가 실제로 데이터를 응답하는 것
    #     # 따라서, res.json() 도 대체해야 함
    #     res.json.return_value = mock_product
    #
    #     product = grab_store.show_product(product_id=product_id)

    # When
    # 외부 의존성 대체 4강: request-mock 활용
    # 써놓은 url 에 요청을 보냈을 때, 미리 정한 json 객체를 응답으로 받아서 사용한다.
    requests_mock.get(f"{API_URL}/{product_id}", json=mock_product)

    product = grab_store.show_product(product_id=product_id)

    # Then
    assert product == Product(title=mock_product["title"], price=30000)


def test_give_money_expensive(user):
    price = 10000000

    with pytest.raises(Exception):
        user._give_money(money=price)


def test_take_money(grab_store):
    price = 100
    pre_money = grab_store._money

    grab_store._take_money(money=price)

    assert grab_store._money == pre_money + price


def test_return_money(grab_store):
    price = 100

    pre_money = grab_store._money
    grab_store._return_money(price)

    assert grab_store._money == pre_money - price


def test_take_out_product(requests_mock, grab_store, mock_products):
    product_id = 1
    mock_product = mock_products[product_id]
    requests_mock.delete(url=f"{API_URL}/{product_id}", json=mock_product)

    product = grab_store._take_out_product(product_id=product_id)

    assert product == Product(title=mock_product["title"], price=mock_product["price"])
    # assert grab_store._products.get(product_id, None) is None


def test_sell_product_well(requests_mock, grab_store, mock_products):
    """
    통합 테스트 코드
    통합 테스트로 넘어올 수록, 로직이 복잡해지고 발생할 수 있는 예외도 많아진다.
    따라서, 시간이 걸리더라도 신경써서 작성하는 것이 안전한 코드를 만드는 방법이다.
    :param grab_store:
    :return:
    """
    product_id = 1
    pre_money = grab_store._money
    mock_product = mock_products[product_id]

    # mocking
    requests_mock.get(f"{API_URL}/{product_id}", json=mock_product)
    requests_mock.delete(f"{API_URL}/products/{product_id}", json=mock_product)

    product = grab_store.show_product(product_id=product_id)
    _product = grab_store.sell_product(product_id=product_id, money=product.price)

    assert grab_store._money == pre_money + product.price
    # assert grab_store.show_product(product_id=product_id) is None


def test_sell_product_not_found(requests_mock, grab_store, mock_products):
    product_id = 100
    # product = grab_store.show_product(product_id=product_id)

    mock_products = mock_products.get(product_id, None)

    # mocking
    requests_mock.get(f"{API_URL}/{product_id}", json=mock_products)
    requests_mock.delete(f"{API_URL}/{product_id}", json=mock_products)

    with pytest.raises(Exception):
        grab_store.sell_product(product_id=product_id, money=0)


