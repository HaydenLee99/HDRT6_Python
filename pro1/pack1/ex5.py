# 조건 판단문 if
var=3
if var >= 3:
    print('크네')

if var >= 3:
    print('크구나')
else:
    print('작구나')

a='kbs'
b=9 if a=='kbs' else 11
print('b:',b)

a=3
if a<5:
    print(0)
elif a<10:
    print(1)
else:
    print(2)

print(0 if a<5 else 1 if a<10 else 2)   #3항 연산자
print('end')