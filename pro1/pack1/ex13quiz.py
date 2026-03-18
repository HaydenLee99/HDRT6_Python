# 재귀문제 :  리스트 자료 v = [7, 9, 15, 43, 32, 21] 에서 최대값 구하기 - 재귀 호출 사용 

#                   print(find_max(v, len(v)))

v = [7, 9, 15, 43, 32, 21]
def find_max(a:list,b:int):
    tmp = a[b-1]
    def tempFunc(b):
        nonlocal tmp
        if b == 0:
            return tmp
        else:    
            print('현재 최대값은',tmp)     
            if tmp < a[b-1]:
                tmp = a[b-1]
            return tempFunc(b-1)
    return tempFunc(b)

print(find_max(v, len(v)))