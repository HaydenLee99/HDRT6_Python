# 여러 개의 부품 객체를 조립해서 완성차 생성
# Class의 포함 관계 사용 (자원의 재활용)
# 다른 클래스를 마치 자신의 멤버처럼 선언하고 사용

from ex23pohamhandle import PohamHandle

class PohamCar:
    turnShowMessage = '정지'
    def __init__(self,ownerName):
        self.ownerName = ownerName
        self.handle = PohamHandle()         # 클래스의 포함관계
    def turnHandle(self,q):
        if q > 0:
            self.turnShowMessage = self.handle.rightTurn(q)
        elif q < 0:
            self.turnShowMessage = self.handle.leftTurn(q)
        else:
            self.turnShowMessage = '직진'

if __name__ == '__main__':
    tom = PohamCar('Mr. Tom')
    tom.turnHandle(10)
    print(tom.ownerName + ' 현재 ' + tom.turnShowMessage +\
           ' 중 이에요 ' + str(tom.handle.quantity) + ' 만큼요!')
    
    john = PohamCar('Mr. John')
    john.turnHandle(-20)
    print(john.ownerName + ' 현재 ' + john.turnShowMessage +\
           ' 중 이에요 ' + str(john.handle.quantity) + ' 만큼요!')
    
    suzy = PohamCar('Ms. Suzy')
    suzy.turnHandle(0)
    print(suzy.ownerName + ' 현재 ' + suzy.turnShowMessage +\
           ' 중 이에요 ' + str(suzy.handle.quantity) + ' 만큼요!')

