# function : 여러 개의 수행문을 하나의 이름으로 묶은 실행 단위
# 함수 고유의 실행 공간을 갖음
# 자원의 재활용

# 내장함수
print(sum([1,2,3]))
print(bin(8))
print(eval('4+5'))
print(round(1.74))                                  #반올림
import math
print(math.ceil(1.2), ' ',math.ceil(1.2))           # 올림
print(math.floor(1.2), ' ',math.floor(1.2))         # 내림

b_list = [True,1,False]
print(all(b_list))
print(any(b_list))

data1 = [10,20,30]
data2 = ['a','b']
for i in zip(data1,data2):
    print(i)