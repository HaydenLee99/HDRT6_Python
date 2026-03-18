class Person:
    say = '난 사람이야~~'
    nai = 81
    __msg = 'private member good'
    def __init__(self, nai):
        self.nai = nai

    def printInfo(self):
        print(f'나이 : {self.nai}, 이야기:{self.say}')
    def helloMethod(self):
        print('안녕')

per = Person('25')
per.printInfo()

class Employee(Person):                     # 상속받아~
    subject = '근로자'
    say = '젊은이'
    def __init__(self):
        print("employee 생성자 먼저 뜨고~")
    def printInfo(self):
        print('employee의 printInfo가 실행되는거야~')
    def ePrintInfo(self):
        print(self.subject)
        self.helloMethod()
        self.printInfo()
        print(super().say)
        super().printInfo()
        
emp = Employee()
print(emp.subject)
print(emp.say)
print(emp.nai)

emp.ePrintInfo()
class Worker(Person):
    def __init__(self, nai):
        print('Worker 생성자')
        super().__init__(nai)           # 부모 클래스의 생성자를 호출
    
    def wPrintInfo(self):
        print('worker의 wPrintInfo 야~')
        # self.printInfo()
        super().printInfo()
wor = Worker('90')
print(wor.say,wor.nai)
wor.wPrintInfo()

class Programmer(Worker):
    def __init__(self, nai):
        print('Programmer  생성자야~')
        super().__init__(nai)
        Worker.__init__(self, nai)
    def pPrintInfo(self):
        print('Programmer의 pPrintInfo 야~')
    
    def wPrintInfo(self):              #부모 메소드와 동일 메소드 선언         
        print('Programmer에서 overriding')

pro = Programmer(35)
print(pro.say,pro.nai)
pro.pPrintInfo()
pro.wPrintInfo()

print('class type check')
a=3; print(type(a))
print(type(pro))
print(type(wor))
print(Person.__bases__)
print(Employee.__bases__)
print(Worker.__bases__)
print(Programmer.__bases__)