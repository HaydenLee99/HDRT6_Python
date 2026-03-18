# Class의 포함관계 연습 - Lotto 부자되기
import random

class LottoBall:

    def __init__(self,num):
        self.num = num

class LottoMachine:
    
    def __init__(self):
        self.balllist = []
        for i in range(1,46):
            self.balllist.append(LottoBall(i))
    
    def selectBalls(self):
        # for a in range(45):
        #     print(self.balllist[a].num, end=' ')
        random.shuffle(self.balllist)
        # print()
        # for a in range(45):
        #     print(self.balllist[a].num, end=' ')
        return self.balllist[0:6]
    
class LottoUI:
    def __init__(self):
        self.machine = LottoMachine()
    def playLotto(self):
        start = input('Lotto Start? [y/n]')
        if start == 'y':
            selectedBalls = self.machine.selectBalls()
            for ball in selectedBalls:
                print(ball.num, end=' ')

if __name__ == '__main__':
    LottoUI().playLotto()