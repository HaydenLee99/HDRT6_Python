#2 
class ElecProduct:
    volume = 0
    def volimeControl(self):
        pass

class ElecTv(ElecProduct):
    def volimeControl(self):
        print('나는 ElecTv')
class ElecRadio(ElecProduct):
    def volimeControl(self):
        print('나는 ElecRadio')

tv = ElecProduct()
tv = ElecTv()
tv = ElecRadio()


#3
class Animal:
    def move(self):
        pass
class Dog(Animal):
    name = '개'
    def move(self):
        print('Dog의 move')
class Cat(Animal):
    name = '고양이'
    def move(self):
        print('Cat의 move')
class Wolf(Dog,Cat):
    pass
class Fox(Dog,Cat):
    def move(self):
        print('Dog의 move')
    def foxMethod(self):
        print('foxMethod 이에요')
