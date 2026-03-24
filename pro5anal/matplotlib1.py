import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.rc('font', family='Malgun Gothic')          # window 한글 깨짐 방지
plt.rcParams['axes.unicode_minus'] = False      # 음수 기호 깨짐 방지

# x = ["서울", "인천", "수원"]
x = "서울", "인천", "수원"
# x = {"서울", "인천", "수원"}            # set type은 에러. TypeError: unhashable type: 'set'
y = [5,3,7]

plt.plot(x,y)
plt.xlim([-1, 3])
plt.ylim([0, 10])
plt.yticks(list(range(0,11,1)))
plt.show()

data = np.arange(1,11,2)
plt.plot(data)
x=[0,1,2,3,4]
for a,b in zip(x,data):
    plt.text(a,b,str(b))
plt.show()

x=np.arange(10)
y=np.sin(x)
print(x,y)
# plt.plot(x,y, 'b*')
plt.plot(x,y,'go--',linewidth=2, markersize=12)

plt.show()

# hold : 복수의 plot으로 여러개의 차트를 겹쳐 그림
x=np.arange(0,np.pi*3,0.1)
y_sin = np.sin(x)
y_cos = np.cos(x)

plt.figure(figsize=(10,6))
plt.plot(x,y_sin, 'r')
plt.scatter(x,y_cos)

plt.xlabel('x 축')
plt.ylabel('y 축')
plt.title("sine & cosine")
plt.legend(['sine','cosine'])

plt.show()


plt.subplot(2,1,1)
plt.plot(x,y_sin)
plt.title('sine')

plt.subplot(2,1,2)
plt.plot(x,y_cos)
plt.title('cosine')

plt.show()

irum = ['a','b','c','d','e']
kor=[80,40,50,10,20]
eng=[10,80,40,50,40]
plt.plot(irum, kor,'ro-')
plt.plot(irum, eng,'bo--')
plt.title('시험점수')
plt.legend(['국어','영어'], loc='best')
plt.grid(True)
# fig=plt.gcf()     # 이미지 저장 준비
plt.show()
# fig.savefig('plot1.png')
from matplotlib.pyplot import imread
# img=imread('plot1.png')   # 이미지 read
# plt.imshow(img)
