# Class의 포함관계 연습 - 냉장고 객체의 음식 객체 담기

class Fridege:

    isOpened = False
    foods = []

    def open(self):
        self.isOpened = True
        print('냉장고 문이 열렸다!')

    def close(self):
        self.isOpened = False
        print('냉장고 문이 닫혔다!')

    def foodsList(self):
        for f in self.foods:
            print(f'{f.name}_{f.expiry_date}')
        print()

    def put(self, thing):
        if self.isOpened:
            self.foods.append(thing)
            print(f'냉장고에 {thing.name} 넣었다!')
            self.foodsList()
        else:
            print('냉장고 문이 닫혀있다!')

class FoodData:

    def __init__(self, name, expiry_date):
        self.name = name
        self.expiry_date = expiry_date
    
fobj = Fridege()

apple = FoodData('사과','20260801')
coke = FoodData('콜라','20270101')

fobj.put(apple)

fobj.open()
fobj.put(apple)
fobj.close()
print()
fobj.open()
fobj.put(coke)
fobj.close()


