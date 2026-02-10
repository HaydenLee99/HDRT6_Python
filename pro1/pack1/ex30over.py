# 오버라이딩 : 결제 시스템
class Payment:
    def pay(self, amount):
        print(f'{amount}원 결제 처리')

class CardPayment(Payment):    
    def pay(self, amount):
        print(f'{amount}원 카드 결제 완료 - 고맙습니다 ^_^')

class CashPayment(Payment):
    def pay(self, amount):
        print(f'{amount}원 현금 결제 완료 - 감사합니다 ^^7')

payment = [CardPayment(),CashPayment()]
for p in payment:
    p.pay(5000)