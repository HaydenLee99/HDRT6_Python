# 커피 자판기 프로그램
COFFEE = 200

class Machine:

    def __init__(self):
        self.coin = int(input('동전을 입력하세요 : '))
        self.cup = int(input('몇 잔을 원하세요 : '))
        # self.coinin = CoinIn()
        # self.change = self.coinin.calcChange(self.coin, self.cup)
        self.change = CoinIn().calcChange(self.coin,self.cup)

    def showData(self):
        if self.coin < self.cup * COFFEE:
            print('요금 부족')
        elif self.coin >= self.cup * COFFEE:
            print(f'커피 {self.cup}잔과 잔돈 {self.change}원')

class CoinIn:
    def calcChange(self,coin,cup):
        return coin-(cup*COFFEE)

if __name__ == '__main__':
    Machine().showData()