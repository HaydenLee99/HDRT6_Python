# 사용자 정의 함수
'''
def 함수명(가인수,,,,):
    return 반환값           #하나의 값만 반환. return이 없을 경우 None을 반환함.

    
함수명(실인수,,,,)          # 호출방법
'''

def doFunc1():
    print('doFunc1 수행')
    return None

def doFunc2(name):
    print('name : ',name)
    return None

def doFunc3(arg1, arg2):
    re = arg1 + arg2
    return re

def doFunc4(a1, a2):
    imsi = a1 + a2
    if imsi % 2 == 0:
        return None
    elif imsi % 2 == 1:
        return imsi

doFunc1()
print('함수 주소는 ',doFunc1)
print('함수 주소(해시태그)는 ',id(doFunc1))

doFunc1()
doFunc2('길동')
print(doFunc3(20, 80))
print(doFunc3('20','80'))
print(doFunc3('대한','민국'))

def triArea(a,h):
    Area = a * h / 2
    triAreaPrint(Area)
def triAreaPrint(Aa):
    print('삼각형 면적은 ', Aa)

triArea(20,30)

def passResult(kor, eng):
    ss = kor + eng
    if ss >= 50:
        return True
    else:
        return False
if passResult(40,20):
    print('합격')
else:
    print('불합격')

def swapFunc(a,b):
    return b, a
a=10; b=20
print(a,' ',b)
print(swapFunc(a,b))

def funcTest():
    print('funxcTest 멤버 처리')
    def funcInner():
        print('내부 함수')
    funcInner()

funcTest()

def isOdd(para):
    return para%2==1
mydict={x:x*x for x in range(11) if isOdd(x)}
print(mydict)

# 파이썬 변수 (LEGB 규칙) : L -> E -> G -> B 순으로 탐색
# L(Local): 현재 함수 안
# E(Enclosing): 바깥 함수(중첩 함수일 때)
# G(Global): 파일(모듈) 전체
# B(Built-in): print, len 같은 내장 함수
# global 변수 : G 수준 변수로 사용선언
# nonlocal 변수 : E 수준 변수를 가져와 사용선언

a=10; b=20; c=30        # G
def Foo():
    a=7                 # E
    b=100
    def Bar():
        global c        # G로 사용선언
        nonlocal b      # E 수준 변수를 가져와 사용선언
        print(f'Bar 수행 후 a:{a}, b:{b}, c:{c}')
        c=9           # global c 선언이 없는 경우, UnboundLocalError 유의
    Bar()
    print(f'Foo 수행 후 a:{a}, b:{b}, c:{c}')
Foo()
print(f'함수 수행 후 a:{a}, b:{b}, c:{c}')
print()

g=1
def func():
    a = g
    # g = 2         # UnboundLocalError
                    # func 함수 내에서 g=2로 g를 선언 -> Local 변수로 g 생성 -> g에 값 치환 순으로 이루어짐
                    # a = g로 인해 g를 Global에서 가져오려 했는데 이미 함수 내에 g가 Local 변수로 있어 에러 발생
    return a
print(func())
