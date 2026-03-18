# method overiding : 부모에서 정의 된 method를 자식이 동일 이름의 method로 내용만 변경해 사용
# 부모 method의 기능을 대체하는 새로운 기능을 갖게 됨
# 동작의 구체화(공통 틀은 부모가 행동은 자식이 한다) 실현
# 다형성 Polymorphism 같은 method이나 객체에 따라 다른 기능을 수행
# 부모 코드는 유지한테 자식코드만 변경하여 자원의 확장, 유지 보수에 도움 됨

class Parent:
    def printData(self):
        pass

class Child1(Parent):
    def abc():
        print('child_1 고유 메소드')
    def printData(self):
        print('Child_1에서 printData 재정의 한 거에요')

class Child2(Parent):
    def printData(self):
        print('Child_2에서 printData 재정의 한 거에요')
        msg = '부모와 동일 메소드명이나 내용은 다르다.'
        print(msg)

c1 = Child1()
c1.printData()
c2 = Child2()
c2.printData()

par = Parent()
par = c1
par.printData()
par = c2
par.printData()
