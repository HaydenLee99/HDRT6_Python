var1 = "안녕 파이썬"
print(var1)         # 주석이에요        블럭 지정 후 ctrl + / 하면 블럭 주석 처리 가능
"""
여러 
줄 주석
"""
var1 = 5;           # RAM에 var1이라는 공간을 잡고, 기억장소 내에 '5의 주소'를 var1에 줌. (참조형)
print(var1)         # 5는 기억장소 내에 객체로 잡힘.

var2 = var1
print(var1, var2)

var3 = 7
print(var1, var2, var3)
print(id(var1), id(var2), id(var3))

Var3 = 8
print(var3, Var3)

a = 5
b = a
c = 5
print(a,b,c)
print(a is b, a == b)       # is: 주소 비교연산     ,   ==: 값 비교연산
print(b is c, b == c)

aa = [5]
bb = [5]
print(aa,bb)
print(aa is bb, aa == bb)   # 집합형 변수 aa와 bb는, 값은 같지만 주소는 서로 다름

print('------------------')             # Line skip
import keyword              # 키워드 목록 확인용 모듈 읽기
print('예약어 목록:', keyword.kwlist)

print('type(자료형) 확인')
kbs = 9
print(isinstance(kbs,int))
print(isinstance(kbs,float))
print(5, type(5))
print(5.3, type(5.3))
print(3+4j, type(3+4j))
print(True, type(True))
print('good', type('good'))
print((1,), type((1,)))
print([1], type([1]))
print({1}, type({1}))
print({'k':1}, type({'k':1}))