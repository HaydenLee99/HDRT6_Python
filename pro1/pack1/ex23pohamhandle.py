# 어딘가에서 필요한 부품 핸들 클래스 작성
class PohamHandle:
    quantity = 0        # handle 회전량
    def leftTurn(self,quantity):
        self.quantity = quantity
        return '좌회전'
    
    def rightTurn(self,quantity):
        self.quantity = quantity
        return '우회전'


