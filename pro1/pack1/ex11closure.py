# Closure : Scope에 제약을 받지 않는 변수들을 포함하고 있는 코드블럭.
# 내부 함수의 주소를 반환해 함수 밖에서 함수 내의 멤버를 참조하기

def funcTimes(a,b):
    c=a*b
    return c
print(funcTimes(2,3))
kbs = funcTimes(2,3)
print(kbs)
kbs = funcTimes
print(kbs)
print(kbs(2,3))
print(id(kbs),id(funcTimes))
mbc=sbs=kbs
del funcTimes
print(mbc(2,3),sbs(2,3),kbs(2,3))

print('\n클로저를 사용하지 않는 경우----------')
def out():
    count = 0
    def inn():
        nonlocal count
        count += 1
        return count
    print(inn())
out()
out()

print('\n클로저를 사용하는 경우----------')
def outer():
    count = 0
    def inner():
        nonlocal count
        count += 1
        return count
    return inner            # closure 내부 함수의 주소를 변환
var1 = outer()              # 내부 함수의 주소를 변수 var1에 저장
print('var1의 주소: ', var1)
print(var1())
print(var1())
myvar=var1()
print(myvar)

var2=outer()                # 새로운 객체(inner함수) 생성
print(var2())
print(var2())

print('수량 * 단가 * 세금 한 결과를 출력')
def outer2(tax):
    def inner2(su,dan):
        amount = su*dan*tax
        return amount
    return inner2

q1 = outer2(0.1)     # 1분기 tax 0.1
result1 = q1(5,50000)
print('result 1 ', result1)
result2 = q1(2,10000)
print('result 2 ', result2)

q2 = outer2(0.05)     # 2분기 tax 0.05
result3 = q2(5,50000)
print('result 3 ', result3)
result4 = q2(2,10000)
print('result 4 ', result4)

print('\n일급함수 : 함수 안의 함수, 인자로 함수 전달 가능, 반환값이 함수')
def func1(a,b):
    return a+b
func2 = func1
print(func1(3,4))
print(func2(3,4))
def func3(fu):
    def func4():
        print('나는 내부함수야~')
    func4()
    return fu
mbc = func3(func1)
print(mbc(3,4))

print('\n축약함수(lambda) : 이름이 없는 한 줄 짜리 함수')
# lambda 매개변수들,:반환식 꼴              return 없이 결과 반환

def hapfunc(x,y):
    return x+y
print(hapfunc(1,2))
print((lambda x,y:x+y)(1,2))
gg = lambda x,y:x+y
print(gg(1,2))

kbs = lambda a,su=10:a+su
print(kbs(1))
print(kbs(1,2))
sbs = lambda a, *tu, **di:print(a,tu,di)
sbs(1,2,3,4,5,var1=4,var2=5)
li=[lambda a,b:a+b, lambda a,b:a*b]
print(li[0](3,4), li[1](3,4))

print('\n다른 함수애새 람다 사용하기')
filter(함수, 반복가능한과제)
print(list(filter(lambda a:a <5, range(10))))
print(list(filter(lambda a:a %2, range(10))))

# 문1 1~100 사이 정수 중 5의 배수이거나 7의 배수만 술력