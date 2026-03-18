# 예외처리 : File, Network, DB, 실행에러 등의 대처

def divide(a,b):
    return a/b

try:
    # list = [-1,0,1]
    # print(list[3])

    # for i in list:
    #     print(divide(5,i))
    
    open("c:/work/abc.txt")

except IndexError as e:
    print('참조 범위 오류',e)
except ZeroDivisionError as e:
    print('0으로는 나눌 수 없다.', e)   
except Exception as e:
    print("에러 : ", e)
finally:
    print('에러 유무에 상관없이 반드시 실행되는 finally')
    print('\n-*-The_End-*-')








