from sklearn.datasets import load_breast_cancer
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import seaborn as sns

DATASET = load_breast_cancer()

data_ = pd.DataFrame(DATASET.get('data'), columns=DATASET.get('feature_names'))
target = pd.DataFrame(DATASET.get('target'), columns=['class']) # 0:Malignant, 1:Benign
target['class name'] = pd.Series(['Malignant' if i==0 else 'Benign' for i in target.get('class')])

print(DATASET.get('DESCR'))
print(data_.info())

labels = [
  'mean radius',
  'mean concavity',
  'mean concave points',
]

fig = plt.figure(figsize=(12, 16), dpi=200)
gs = fig.add_gridspec(nrows=4, ncols=3)

for i, azim in enumerate(range(30, 120, 30)):
  ax = fig.add_subplot(gs[i], projection='3d')
  ax.set_xlabel(labels[0])
  ax.set_ylabel(labels[1])
  ax.set_zlabel(labels[2])
  ax.view_init(elev=10, azim=azim)
  ax.plot(data_.get(labels[0]), data_.get(labels[1]), data_.get(labels[2]), marker='.', linestyle='None')

# Compress 30 -> 2 dimensions by PCA
data_std = pd.DataFrame(StandardScaler(copy=True).fit_transform(data_), columns=DATASET.get('feature_names'))
pca = PCA(n_components=2).fit(data_std)
data_pca = pd.concat([pd.DataFrame(pca.transform(data_std), columns=['pca1', 'pca2']), target], axis=1)

print(pca.explained_variance_ratio_)

ax = fig.add_subplot(gs[3:])
ax.set_xlabel('pca1')
ax.set_ylabel('pca2')
sns.scatterplot(data=data_pca, x='pca1', y='pca2', hue='class name')

plt.savefig('1-6_cancer.png')
