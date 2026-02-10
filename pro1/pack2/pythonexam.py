# li = [1, 2, 2, 2, 3, 4, 5, 5, 5, 2, 2]
# print(list(set(li)))

# for i in {1, 2, 3, 4, 5, 5, 5, 5}:
#     print(i, end = ' ')
# tmp = []
# for i in range(1,101):
#     if i % 3 == 0 or i % 4 == 0:
#         if i % 7 == 0:
#             pass
#         else: 
#             print(i, end=' ')
#             tmp.append(i)
# print()
# print('건수 : ',len(tmp))
# print('배수의 총합 : ',sum(tmp))
# print(type(5%2))
# *v1, v2, v3 = {1, 2, 3, 4, 5, 1, 2, 3, 4, 5}

# print(v1)
# print(v2)
# print(v3)
# print((lambda m,n:m+n*5)(1,2))
# print(list(range(1, 6, 2)))
# try:
#     aa = int(input())
#     bb = 10 / aa
#     print(bb)
# except ZeroDivisionError as e:
#     print(e)

# i = 1
# while i <= 10:
#     j = 1
#     msg = ["*"]*10
#     while j < i:
#         msg[j-1]=' '
#         j += 1
#     print(*msg)
#     i += 1

# year = int(input("연도입력:"))
# if year % 4 == 0:
#     if year % 100 != 0 or year % 400 == 0:
#         print(f'{year}년은 윤년')
#     else:
#         print(f'{year}년은 평년')
# else:
#     print(f'{year}년은 평년')

# i = 0
# while True:
#     if i <= 100:
#         i += 1
#         if i % 10 != 3:continue
#     if i > 100:break

#     print(i,end=' ')
#     print(end='')

# i = 3
# while i < 10:
#     j = 1  
#     while j < 10:
#         if j != 9:
#             print(f'{i}*{j}={i*j}', end=' ')
#             j += 1
#         else:
#             print(f'{i}*{j}={i*j}')
#             j += 1
#     i += 2

# class Bicycle:

#     def __init__(self,name,wheel,price):
#         self.name = name
#         self.wheel = wheel
#         self.price = price

#     def display(self):
#         total = self.wheel * self.price
#         print(f"{self.name}님 자전거 바퀴 가격 총액은 {total}원 입니다.", end='')

# gildong = Bicycle('길동', 2, 50000) # 생성자로 name, wheel, price 입력됨
# gildong.display() 