import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns

iris_data = sns.load_dataset('iris')
# print(iris_data.info())
# print(iris_data.columns)    # ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species']

# scatter
plt.scatter(iris_data['sepal_length'], iris_data['petal_length'])
plt.xlabel('sepal_length')
plt.ylabel('petal_length')
plt.title('iris data')
plt.show()

print()
# print(iris_data['species'].unique())        # ['setosa' 'versicolor' 'virginica']
