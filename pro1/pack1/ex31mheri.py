# 클래스의 다중 상속 - 부모가 복수
def hobby():
    print('나는 모듈의 멤버 이다. 일반함수이다.')

class Tiger:
    data = "호랑이 세 마리"
    def cry(self):
        print('호랑이 : 어흥')
    def eat(self):
        print('육식을 즐겨')
class Lion:
    def cry(self):
        print('사자 : 으르렁')
    def hobby(self):
        print('백수의 왕은 낮잠이 취미')

class Liger1(Tiger, Lion):
    pass

class Liger2(Lion, Tiger):
    data = '사자가 최고야'
    def play(self):
        print('Liger_2의 고유 메소드 입니다')
    def hobby(self):
        print(r'라이거는 쉬는 날 산책을 좋아해 \^o^/')
    def showData(self):
        self.hobby()
        super().hobby()
        hobby()

        self.eat()
        super().eat()

        print(self.data + ' '+super().data)
a1 = Liger1()
print(a1.data)
a1.eat()
a1.hobby()
a1.cry()

print('-'*27)
a2 = Liger2()
a2.cry()
a2.showData()
