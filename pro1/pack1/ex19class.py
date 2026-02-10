# OOP(객체 중심 프로그래밍 기능) : 새로운 타입 생성, 포함, 상속, 다형성 등을 구사 가능
# Class로 인스턴스 해서 객체를 생성(별도의 이름 공간을 갖음)
# 객체는 멤버필드(변수)와 메소드로 구성
# 모듈의 멤버 : 변수, 명령문, 함수, 모듈, 클래스

class TestClass:
    aa = 1                      # 멤버필드, 현재 클래스 내에서 전역

    def __init__(self):         # 특별한 method
        print('생성자 : 객체 생성시 최초로 1회 호출 - 초기화 담당')
    
    def __del__(self):
        print('소멸자 : 프로그램 종료시 자동실행 - 마무리 작업')

    def printMsg(self):         # 일반 method
        name = '홍길동'          # 지역 변수
        print(name)
    
print(TestClass)
test = TestClass()
print('test 객체의 멤버 aa : ',test.aa)

# method call
test.printMsg()                 # Bound Method call

TestClass.printMsg(test)        # UnBound Method call
print(type(1))
print(type(1.0))
print(type(test))
print(id(test))
print(id(TestClass))
test2 = TestClass()
print(id(test2))

