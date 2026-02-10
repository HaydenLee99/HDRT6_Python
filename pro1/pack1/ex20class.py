class Car:
    handle = 1
    speed = 0
    def __init__(self, name, speed):
        self.name = name                            # 현재 객체의 name에게 name 인자값을 준다
        self.speed = speed                          # 현재 객체의 speed에게 speed 인자값을 준다
    
    def showData(self):
        km = '킬로미터'
        msg = '속도:' + str(self.speed) + km
        return msg
    def printHandle(self):
        return self.handle
    
print(Car.handle)

car1 = Car('Rambo',10)
print('car1 : ',car1.name,' ',car1.speed,car1.handle)
car2 = Car('Fera',20)
print('car  주소',id(Car))
print('car 1 주소',id(car1))
print('car 2 주소',id(car2))

car1.color = '파랑'
print("car1.color는 ",car1.color)

print(car1.__dict__)
print(car2.__dict__)
print('----------------------method----------------------')

print("car1 ",car1.showData())
print("car2 ",car2.showData())

car1.speed = 80
car2.speed = 110
print("car1 ",car1.showData())
print("car2 ",car2.showData())

car1.handle = 90
car2.handle = -90
print("car1 handle",car1.printHandle())
print("car2 handle",car2.printHandle())