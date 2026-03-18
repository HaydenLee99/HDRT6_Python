# 반복문 for
# for i in [1,2,3,4,5]:
#     print(i, end=' ')
# print()

# for i in (1,2,3,4,5):
#     print(i, end=' ')
# print()

# for i in {1,2,3,4,5}:
#     print(i, end=' ')
# print()

print('분산/표준편차-----')
# 편차 = 값 - 평균
# 분산 = 편차 제곱의 합의 평균
# 표준편차 = 분산의 제곱근
numbers1 = [1,3,5,7,9]       # 합은 25, 평균은 5.0
numbers2 = [3,4,5,6,7]     # 합은 25, 평균은 5.0
numbers3 = [-3,4,5,7,12]   # 합은 25, 평균은 5.0
numbers = [numbers1, numbers2, numbers3]
tot = 0
for j in range(3):
    for a in numbers[j]:
        tot += a
    print(f"합은 {tot}, 평균은 {tot/len(numbers[j])}")
    avg = tot/len(numbers[j])
# 편차
    tmp = 0
    for i in numbers[j]:
        tmp += (i-avg)**2
    print(f"분산은 {tmp/len(numbers[j])}, 표준 편차는 {(tmp/len(numbers[j]))**0.5}")
    tot = 0

colors = {'r','g','b'}
for v in colors:
    print(v, end=' ')

print('\niter() : 반복가능한 객체를 하나씩 꺼낼 수 있는 상태로 만들어주는 함수')
iterator = iter(colors)
for v in iterator:
    print(v, end=' ')
print()

for idx, d in enumerate(colors):        # enumerate 인덱스와 값을 반환
    print(idx, ' ', d)

print('\n사전형---')
datas={'python':'만능언어', 'java':'웹용언어','mariadb':'db언어'}
for i in datas.items():
    print(i[0],' ~~ ',i[0])
for k, v in datas.items():
    print(k, end=' ')
print()
for val in datas.values():
    print(val, end=' ')

print('\n다중 for ------------')
for n in range(2,10):
    print('---{}단---'.format(n))
    for i in range(1,10):
        print('{} * {} = {}'.format(n, i, n*i))


nums=[1,2,3,4,5]
for i in nums:
    if i == 2:continue
    if i == 4:break
    print(i, end=' ')
else:
    print('정상종료')


print('\n정규 표현식 연습 + for')
str = '''이 최고위원은 이날 국회에서 열린 최고위원회의에서 “국민들이 이재명 정부의 중도·실용 노선을 신뢰하고 압도적 지지를 보내고 있는데 자꾸 당이 독자 노선을 추구하거나 당내 노선 갈등이 심각히 벌어진다면 당과 대통령의 지지율 계속 디커플링되다 결국 대통령 국정 지지까지흔들리게 될 수밖에 없다”며 이렇게 말했다. 이 최고위원은 “하늘 아래 2개의 태양 있을 수 없단 게 진리”라며 “이 사안의 정치적 본질은 대통령 지지율이 매우 높고 대통령의 권한이 강력한 임기 초반에 2·3인자들이 판을 바꿔 당권·대권에 대한 욕망이 표출된 결과임을 부인하기 어렵다”고도 주장했다.'''

import re
str2 = re.sub(r'[^가-힣\s]','',str)         # 한글과 공백 이외의 문자는 공백처리
print(str2)
str3 = str2.split(' ')                      # 공백을 구분자로 문자열 분리
print(str3)
cou = {}
for i in str3:
    if i in cou:
        cou[i] += 1                         # 같은 단어가 있으면 누적
    else:
        cou[i] = 1                          # 최초 단어인 경우 '단어':1
print(cou)

print('\n정규 표현식 좀 더 연습')
for test_ss in ['111-1234','일이삼-일이삼사','222-1234','333&1234']:
    if re.match(r'^\d{3}-\d{4}$', test_ss):
        print(test_ss, '전화번호 맞아요')
    else:
        print(test_ss, '전화번호 아니에요')

print('\ncomprehension : 반복문 + 조건문 + 값 생성을 한 줄로 표현')
a = range(1,11)
li = []
for i in a:
    if i % 2 == 0:
        li.append(i)
print(li)

print(list(i for i in a if i % 2 == 0))

datas = [1,2,'a',True,3.0]
li2 = [i*i for i in datas if type(i) == int]
print(li2)

id_name ={1:'tom',2:'lucy'}
name_id = {val:key for key, val in id_name.items()}
print(name_id)
print()
print([1,2,3])
print(*[1,2,3])         # * : unpack
aa = [(1,2),(3,4),(5,6)]
for a,b in aa:
    print(a+b)
print(*[a+b for a,b in aa], sep='\n')

print('\n수열 생성 : range')
print(list(range(-10,-100,-20)))
print(set(range(1,6,2)))
print(tuple(range(1,6,2)))

for i in range(6):
    print(i, end=' ')

for _ in range(6):
    print('반복')   

total = 0
for i in range(1,101):
    tot += i
print('tot : ',tot)

for i in range(2,10):
    for j in range(1,10):
        print(f'{i}*{j} = {i*j}', end=' ')
    print()

exit(0)