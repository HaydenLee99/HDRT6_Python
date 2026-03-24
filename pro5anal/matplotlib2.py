import matplotlib.pyplot as plt
import numpy as np

# matplotlib 스타일 인터페이스 방식
plt.figure() 

x = np.arange(10)

plt.subplot(2,1,1)
plt.plot(x,np.sin(x))

plt.subplot(2,1,2)
plt.plot(x,np.cos(x))

plt.show()

# 객체 지향 인터페이스 방식
fig, ax = plt.subplots(nrows=2, ncols=1)

ax[0].plot(x,np.sin(x))
ax[1].plot(x,np.cos(x))

plt.show()

# 차트 종류 일부 확인
fig = plt.figure()
ax1 = fig.add_subplot(1,2,1)
ax2 = fig.add_subplot(1,2,2)

ax1.hist(np.random.randn(1000), bins=100, alpha=0.9)
ax2.plot(np.random.rand(1000))

plt.show()

# bar chart
data = [50,80,100,90,70]
plt.bar(range(len(data)), data, alpha=0.4)
plt.show()

err = np.random.rand(len(data))

plt.barh(range(len(data)), data, alpha=0.4, xerr=err)
plt.show()

# pie chart
plt.pie(data, colors=['r','g','b'], explode=(0, 0, 0.1, 0, 0))
plt.show()

# box plot
data = [1,50,60,80,100,90,70,300]
plt.boxplot(data)
plt.show()

# bubble chart
n = 30
x = np.random.rand(n)
y = np.random.rand(n)
color = np.random.rand(n)
scale = np.pi * (np.random.rand(n)*15)
plt.scatter(x,y,c=color, s=scale)
plt.show()

# 시계열 데이터로 선그래프
import pandas as pd
fdata = pd.DataFrame(np.random.randn(1000,4), index=pd.date_range('1/1/2000', periods=1000), columns=list('abcd'))
fdata = fdata.cumsum()
plt.plot(fdata)
plt.show()

# pandas의 plot 기능
fdata.plot(kind='bar')
plt.show()