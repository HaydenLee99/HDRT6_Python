kor = 100
def abc():
    kor = 0
    print('모듈의 멤버 함수')

class My:
    kor = 80
    def abc(self):
        print('My member method')

    def show(self):
        #kor = 77
        print(kor)
        print(self.kor)
        self.abc()
        abc()

my = My()
my.show()

print(My.kor)
tom = My()
print(tom.kor)
tom.kor = 88
print(tom.kor)
oscar = My()
print(oscar.kor)

