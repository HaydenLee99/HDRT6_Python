# 연산자
v1 = 3
v1 = v2 = v3 = 5
print(v1,v2,v3)
print('출력1',end = ',')
print('출력2')
print('출력3')

v1, v2 = 10, 20
print(v1,v2)
v2, v1 = 10, 20
print(v1,v2)

print('값 할당 : packing 연산')
v1=1,2,3,4,5
print(v1)
v1=[1,2,3,4,5]
print(v1)
*v1,v2=[1,2,3,4,5]
print(v1,'   ',v2)
# v1,v2*=[1,2,3,4,5] error
v1,*v2=[1,2,3,4,5]
print(v1,'   ',v2)

print()
print(format(1.5678, '10.3f'))
print('나는 나이가 %d 이다.'%23)
print('나는 나이가 %s 이다.'%'스물셋')
print('나는 나이가 %d 이고 이름은 %s이다.'%(23, '홍길동'))
print('나는 나이가 %s 이고 이름은 %s이다.'%(23, '홍길동'))
print('나는 키가 %f이고, 에너지가 %d%%.'%(177.7, 100))
print('이름은 {0}, 나이는 {1}'.format('한국인', 33))
print('이름은 {}, 나이는 {}'.format('신선해', 33))
print('이름은 {1}, 나이는 {0}'.format(34, '강나루'))
abc = 123
print(f"abc의 값은 {abc}임")

print('\n 본격적 연산------------------------------------')
print(5+3,5-3,5*3,5/3,5//3,5%3,3**3)
print(divmod(5,3),' ',5%3)      
# 연산순서: () -> ** -> 단항 -> 산술(*,/->+,-) -> 관계 -> 논리(not -> and -> or) -> =
print(4+5)  #산술연산   
print('4'+'5')  #문자열 더하기
print('한국'*5)  #문자열 곱하기

a = 10
a = a+1
a += 1
print(f'a는 {a}')


print('boolean 처리',bool(True),bool(False))

# r 선행문자
print('aa\t\bb')
print('aa\n\bb')
print(r'aa\t\bb')
print(r'aa\n\bb')

