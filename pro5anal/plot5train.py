import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns
from scipy import stats

plt.style.use('ggplot')     # R의 ggplot 스타일 사용 설정

git_url = "https://raw.githubusercontent.com/pykwon/python/refs/heads/master/data/train.csv"
train = pd.read_csv(git_url, encoding='utf-8', parse_dates=['datetime'])
# print(train.info())
# print(train.isnull().sum())       # 0

# 년월일시 별도 컬럼 추가 생성
train['year'] = train['datetime'].dt.year
train['month'] = train['datetime'].dt.month
train['day'] = train['datetime'].dt.day
train['hour'] = train['datetime'].dt.hour       # 0-23 시
# print(train.head(3))

# 대여량 시각화
figure, ((ax1,ax2),(ax3,ax4)) = plt.subplots(nrows=2, ncols=2)
figure.set_size_inches(15,5)

sns.barplot(data=train, x='year', y='count', ax=ax1)
sns.barplot(data=train, x='month', y='count', ax=ax2)
sns.barplot(data=train, x='day', y='count', ax=ax3)
sns.barplot(data=train, x='hour', y='count', ax=ax4)

ax1.set(ylabel='대여수', title='연별 대여')
ax2.set(ylabel='대여수', title='월별 대여')
ax3.set(ylabel='대여수', title='일별 대여')
ax4.set(ylabel='대여수', title='시간별 대여')

plt.show()

# boxplot
fig, axes = plt.subplots(nrows=2, ncols=2)
figure.set_size_inches(20,10)

sns.boxplot(data=train, y='count', orient='v', ax=axes[0][0])
sns.boxplot(data=train, y='count', x='season', orient='v', ax=axes[0][1])
sns.boxplot(data=train, y='count', x='hour', orient='v', ax=axes[1][0])
sns.boxplot(data=train, y='count', x='workingday', orient='v', ax=axes[1][1])

axes[0][0].set(ylabel='대여수', title='대여')
axes[0][1].set(xlabel='계절', ylabel='대여수', title='계절별 대여')
axes[1][0].set(xlabel='시간', ylabel='대여수', title='시간별 대여')
axes[1][1].set(xlabel='근무여부', ylabel='대여수', title='근무여부별 대여')

plt.show()

# scatter:regplot
fig, (ax1,ax2,ax3) = plt.subplots(ncols=3)
figure.set_size_inches(15,5)

sns.regplot(data=train, y='count', x='temp', ax=ax1)
sns.regplot(data=train, y='count', x='humidity', ax=ax2)
sns.regplot(data=train, y='count', x='windspeed', ax=ax3)

ax1.set(xlabel='온도', ylabel='대여수', title='온도별 대여')
ax2.set(xlabel='습도', ylabel='대여수', title='습도별 대여')
ax3.set(xlabel='풍속', ylabel='대여수', title='풍속별 대여')

plt.show()
