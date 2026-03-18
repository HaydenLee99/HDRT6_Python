# 매개변수 유형 4가지
# 위치 매개변수 : 인수와 순서대로 대응
# 기본값 매개변수 : 매개변수에 입력값이 없으면 기본값 사용
# 키워드 매개변수 : 실인수와 가인수 간 동일 이름으로 대응
# 가변 매개변수 : 인수의 개수가 동적인 경우

def showGugu(start, end=5):                       # start 실인수      end 가인수
    for dan in range(start, end+1):
        print(' ', str(dan) + '단 출력')
        for i in range(1,10):
            print(str(dan) + "*" + \
                  str(i) + "=" + str(dan*i), end=' ')
        print()
showGugu(2,3)

# 가변 매개변수 : 인수의 개수가 동적인 경우
print('\n가변 매개변수 : 인수의 개수가 동적인 경우-----------')
def func1(*ar):
    print(ar)
    for i in ar:
        print('밥 : '+i)
func1('김밥','비빔밥','볶음밥','공기밥')
func1('김밥')                       # ('김밥',) tuple이라서 이렇게 출력됨

def func2(a, *ar):
    print(a)
    print(ar)
func2('김밥','비빔밥','볶음밥','공기밥')

def func3(w,h,**other):
    print(f'몸무게 : {w}, 키 : {h}')
    print(f'기타 : {other}')
func3(80,158,irum='신기루',nai=23)

def func4(a,b,*c,**d):
    print(a,b)
    print(c)
    print(d)
func4(1,2,3,4,5)
func4(1,2,3,4,5,kbs=9,mbc=11)

# type hint : 함수의 인자와 반환값에 type을 적어 가독성 향상
def typeFunc(num:int, data:list[str]) -> dict[str, int]:
    print(num)
    print(data)
    result={}
    for idx, item in enumerate(data,start=1):
        print(f'idx:{idx}, item:{item}')
        result[item] = idx

    return result

rdata = typeFunc(1, ['일','이','삼'])
print(rdata)

