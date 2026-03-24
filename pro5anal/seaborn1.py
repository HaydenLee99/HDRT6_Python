# seaborn : matplotlib 보충용

import matplotlib.pyplot as plt
import koreanize_matplotlib             # 한글 및 음수 기호 깨짐 방지
import seaborn as sns
import pandas as pd

titanic = sns.load_dataset("titanic")
# print(titanic.info())

sns.displot(titanic['age'])
plt.show()

sns.boxplot(y='age',data=titanic, palette='Paired')
plt.show()

sns.relplot(x='sex',y='age',data=titanic)
plt.show()

titanic_pivot = titanic.pivot_table(index='class',columns='sex',aggfunc='size')
print(titanic_pivot)
sns.heatmap(titanic_pivot, cmap=sns.light_palette('gray'), annot=True, fmt='d')
plt.show()

# boxplot 기준 이상치의 확인
# 1. 데이터의 정의
data = [10,12,13,14,15,11,100]
df=pd.DataFrame({'score':data})

# 2. IQR 기반 이상치 탐지
Q1 = df['score'].quantile(0.25)
Q3 = df['score'].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5*IQR
upper_bound = Q3 + 1.5*IQR

# 3. 이상치, 정상치 분리
outliers = df[(df['score'] < lower_bound) | (df['score'] > upper_bound)]
filtered_df = df[(df['score'] >= lower_bound) & (df['score'] <= upper_bound)]

# 4. 이상치 출력
print('이상치 값 : ', outliers)

# 5. 박스플롯 시각화: 제거 전/후 비교
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# 이상치 포함
sns.boxplot(y=df['score'], ax=axes[0], color='salmon')
axes[0].set_title('이상치 포함 데이터')
axes[0].set_ylabel('Score')
axes[0].grid(True)

# 이상치 제거 후
sns.boxplot(y=filtered_df['score'], ax=axes[1], color='lightblue')
axes[1].set_title('이상치 제거 후')
axes[1].set_ylabel('Score')
axes[1].grid(True)

plt.tight_layout()
plt.show()