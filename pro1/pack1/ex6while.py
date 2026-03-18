# 반복문 while
a = 10                          # 변수의 초기값
while a >= 5:                   # 조건
    print(a, end=' ')           # 출력
    a -= 1                      # 변수 변화
else:
    print('\n수행 성공!')

print()

i=1
while i<=3:
    j=1
    while j<=4:
        print('i=' + str(i) + '/j=' + str(j))
        j+=1
    i+=1
    

su = 1
hap = 0
while su<=100:
    # print(su)
    if su % 3 == 0:
        # print(su)
        hap += su 
    su += 1
print(f'1~100 사이의 정수 중 3의 배수의 합은 {hap} 이다.')

print()

colors=['빨강','파랑','노랑','초록']
print(len(colors))
i=0
while i < len(colors):
    print(colors[i])
    i += 1

print('\n별 찍기------')
i = 1
while i <= 10:
    j = 1
    msg = ''
    while j <= i:
        msg += '*'
        j += 1
    print(msg)
    i += 1


# print('if 블럭 내 while 블럭 사용---')
# import time
# sw = input('폭탄 스위치를 누를까요?[y/n]')
# #print('sw : ', sw)
# if sw == 'Y' or sw == 'y':
#     cnt = 5
#     while 1 <= cnt:
#         print('%d초 남았습니다.' %cnt)
#         time.sleep(1)       # 1 sec 후 다음 문장 실행
#         cnt -= 1
#     print('폭발!')

# elif sw == 'N' or sw == 'n':
#     print('작업 취소.')
# else:
#     print('y 또는 n을 누르세요')

print('\ncontinue와 break-----')
a = 0
while a < 10:
    a += 1
    if a == 3 or a == 5:
        continue            # 아래 문을 무시하고 while로 이동한다.
    if a == 7:
        break               # 무조건 while문에서 탈출
    print(a)
else:
    print('정상종료')
print('while 수행 후 a값은 %d이다.'%a)

print('\n키보드로 숫자를 입력 받아 홀수 짝수 확인하기(무한반복)-------')
while True:
    key = input('확인할 숫자를 입력하세요. [q:종료]')
    if key == 'Q' or key == 'q':
        break
    elif int(key) % 2 == 0:
        print('%d는 짝수입니다.'%int(key))
        continue
    elif int(key) % 2 == 1:
        print('%d는 홀수입니다.'%int(key))
        continue

print('end')