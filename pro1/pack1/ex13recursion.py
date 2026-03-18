# 재귀함수 
# 재귀(Recursion):     문제를 더 작은 문제로 나눔, 각 호출마다 새 함수 스택 생성
#                      호출마다 새 스택 프레임, 깊어질수록 메모리 사용 증가, Stack Overflow 위험
#                      RecursionError: maximum recursion depth exceeded
# 반복문 : 하나의 함수 스택, 변수만 갱신, 메모리 효율적
# 반복으로 가능한 문제는 반복문이 더 안전

def cntDown(n):
    if n == 0:
        print('완료')
        return
    else:
        print(n,end=' ')
        cntDown(n-1)          # 재귀

cntDown(5)

print('1부터 n까지 합 구하기---')
def totFunc(n):
    print(f"호출: totFunc({n})")

    if n == 0:
        print("완료 → return 1")
        return 1                            # 더 이상 totFunc() 호출이 없으므로 재귀 종료

    result = n + totFunc(n-1)               # 재귀
    print(f"복귀: totFunc({n}) → {result}")
    return result

result = totFunc(3)
print("최종 결과: ", result)

print('\n계승 출력하기---')
def factFunc(n:int):
    if n == 1:
        return 1
    return n * factFunc(n-1)

result = factFunc(5)
print("최종 결과: ", result)


print('\nend'); exit(0)