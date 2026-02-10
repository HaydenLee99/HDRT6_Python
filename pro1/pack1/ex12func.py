# 함수 장식자
def make2(fn):
    return lambda:'안녕' + fn()
def make1(fn):
    return lambda:'반가워' + fn()
def hello():
    return '홍길동'
hi = make2(make1(hello))
print(hi())

@make2
@make1
def hello2():
    return '신기루'

print(hello2())

def tracfunc(func):
    def wrapper(a,b):
        r = func(a,b)
        print(f'함수명 : {func.__name__} (a={a}, b={b})->{r})')
        return r
    return wrapper

@tracfunc
def addfunc(a,b):
    return a+b
print(addfunc(10,20))

