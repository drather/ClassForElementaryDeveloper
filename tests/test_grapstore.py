"""
통합 테스트 대상은 다음과 같음
- User: purchase_product()
- Store: sell_product()

그 하위 기능은 유닛 테스트로 진행

테스트 명령은 다음 두가지가 있음(동일함)
- python -m pytest tests: tests 디렉토리는 테스트코드를 모아놓은 디렉토리(약속된 이름)
- python -m pytest tests/test_grapstore.py (해당 코드만 테스트 실행)
"""
from main import GrabStore, Product


def test_show_product():
    # Given
    grab_store = GrabStore(
        products={
            1: Product(name="키보드", price=30000),
            2: Product(name="모니터", price=5000000)
        }
    )
    product_id = 1

    # When
    product = grab_store.show_product(product_id=product_id)

    # Then
    assert product == Product(name="키보드", price=30000)