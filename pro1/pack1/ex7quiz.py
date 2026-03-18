# 문1 1 ~ 100 사이의 정수 중 3의 배수이나 2의 배수가 아닌 수를 출력하고, 합을 출력
ans=[]
for i in range(1,101):
    if i % 3 == 0:
        continue
    elif i % 2 ==0:
        continue 
    else:
        ans.append(i)
print(f'문1 답은 {ans}, 합은 {sum(ans)}')
print('\n')

# 문2 2 ~ 5 까지의 구구단 출력
for i in range(2,6):
    print(f'{i}단 시작!')
    for j in range(1,10):
        print(f'{i}*{j}={i*j}') 
print('\n')

# 문3  1 ~ 100 사이의 정수 중 “짝수는 더하고, 홀수는 빼서” 최종 결과 출력
total = 0
for i in range(1,101):
    if i % 2 == 0:
        total += i
    elif i % 2 == 1:
        total -= i
print('문3 답은 %d'%total)
print('\n')

#문4 -1, 3, -5, 7, -9, 11 ~ 99 까지의 모두에 대한 합을 출력
total = 0
for i in range(1,100,2):
    total += i
for i in range(1,100,4):
    total -= 2*i  
print('문4 답은 %d'%total)
print('\n')

#문5 1 ~ 100 사이의 숫자 중 각 자리 수의 합이 10 이상인 수만 출력       예) 29 → 2 + 9 = 11 (출력)
ans = []
for i in range(1,101):
    if i < 10:
        pass
    elif 10 <= i <100:
        if i//10 + i%10 < 10:
            pass
        else:
            ans.append(i)
    else:
        pass
print(ans)
print('\n')

#문6 1부터 시작해서 누적합이 처음으로 1000을 넘는 순간의 숫자와 그때의 합을 출력
total = 0
i = 0
while 1:
    if total <= 1000:
        total += i
        i += 1
    else:
        print(f'문6 답은 숫자는 {i}, 합은 {total}')
        break
print('\n')

#문7 구구단을 출력하되 결과가 30을 넘으면 해당 단 중단하고 다음 단으로 이동
for i in range(2,10):
    for j in range(1,10):
        if i*j <= 30:
            print(f"{i}*{j}={i*j}", end=' ')
print('\n')

# 문8) 1 ~ 1000 사이의 소수(1보다 크며 1과 자신의 수 이외에는 나눌 수 없는 수)와 그 갯수를 출력
ans=[]
for i in range(2, 1001):
    tmp = True
    for j in range(2, i):
        if i % j == 0:
            tmp = False
            break
    if tmp:
        ans.append(i)
print('문8 답은', ans)
print('소수의 개수:', len(ans))

# 문제9) 1부터 50까지의 숫자 중 3의 배수는 건너뛰고 나머지 수만 출력하라
print('문9 답은', end=' ')
for i in range(1,51):
    if i % 3 == 0:
        continue
    print(i, end=' ')
print('\n')

# 문제10) 1부터 100까지 출력하되 4의 배수, 6의 배수는 건너뛴다. 그 외의 수 중 5의 배수만 출력하고 그들의 합도 출력하라
ans = []
for i in range(1,101):
    if i % 4 == 0 or i % 6 == 0:
        continue
    else:
        ans.append(i)
total = []
for i in ans:
    if i % 5 == 0:
        total.append(i)
print('문10 답은', ans,'\n', total, '\n합은', sum(total))     