# List 다양한 종류의 자료 묶음형. 순서 있고 수정, 중복 가능
a = [1, 2, 3]
print(a,a[0],a[0:3])
b = [10, a, 10, 20.5, True, '문자열']
print(b,' ',b[1],' ',b[1][0])

family = ['엄마','아빠','나','여동생']
print(id(family))
family.append('남동생')
family.remove('나')
family.insert(0,'할머니')
family.insert(0,['삼촌', '고모', '조카'])
family += ['이모']
print(id(family))
print (family)

name = ['tom','james','oscar']
name2 = name
print(name, id(name))
print(name2, id(name2))
import copy 
name3=copy.deepcopy(name)
print(name3,id(name))

# tuple 리스트와 유사. 읽기 전용으로 수정불가
t = (1, 2, 3,4)
print(t, type(t))
k=(1,)
print(k, type(k))
print(t[0],t[0:2])

imsi = list(t)
imsi[0]=77
t=tuple(imsi)
print(t)

#set : 숫정 및 중복을 줄여줌. 수정 불가 중복불가
ss={1,2,1,3}
print(ss)
ss2={3,4}

print(ss.intersection(ss2))
print(ss)
ss.update({6,7})
ss.discard(7)
ss.discard(7) # 있으면 지우고 없으면 말음
ss.remove(6) #있으면 지우고 없으면 에러
print(ss)

li=['aa','aa','bb','cc','aa']
print(li)
imsi=set(li) # 중복, 수정 불허
li=list(imsi)
print(li)

# dict 사전 자료형 {'키':값} 꼴
mydic=dict(k1=1,k2='ok',k3=123.4)
print(mydic,type(mydic))

dic={'파이썬':'뱀','자바':'커피','인사':'안녕'}
print(dic)
print(dic['자바'])
#print(dic[0])
dic['금요일']='와우'
print(dic)
del dic['인사']
print(dic)
print(dic.keys())
print(dic.values())