"""
파일 이름앞에 test_ 를 붙여야, pytest 가 파일을 읽어서 테스트함
"""


def add(a, b):
    return a + b


# add 함수에 대한 테스트 코드
def test_add():
    a, b = 1, 2
    assert add(1, 2) == 3



