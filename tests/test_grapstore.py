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
- 이를 없애고, 편하게 사용하고자 conftest.py 를 만든다.`

"""
from main import GrabStore, Product


def test_show_product(grab_store):
    """
    파라미터로 주어진 grab_store 가, conftest.py 에서 grab_store 메서드를 의미한다.
    그럼, grab_store() 메서드가 실행되어 GrabStore 객체를 리턴하게 된다.
    :param grab_store:
    :return:
    """
    # Given
    product_id = 1

    # When
    product = grab_store.show_product(product_id=product_id)

    # Then
    assert product == Product(name="키보드", price=30000)