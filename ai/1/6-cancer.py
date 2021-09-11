from sklearn.datasets import load_breast_cancer
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd

DATASET = load_breast_cancer()

data_ = pd.DataFrame(DATASET.get('data'), columns=DATASET.get('feature_names'))
data = pd.DataFrame(StandardScaler(copy=True).fit_transform(data_), columns=DATASET.get('feature_names'))
target = pd.Series(DATASET.get('target'), name='malignant or benign')

print(DATASET.get('DESCR'))
print(data.info())

labels = [
  'mean radius',
  'mean concavity',
  'mean concave points',
]

fig = plt.figure(figsize=(9, 3), dpi=300)
gs = fig.add_gridspec(nrows=1, ncols=3)

for i, azim in enumerate(range(5, 30, 10)):
  ax = fig.add_subplot(gs[0, i], projection='3d')
  ax.set_xlabel(labels[0])
  ax.set_ylabel(labels[1])
  ax.set_zlabel(labels[2])
  ax.view_init(elev=10, azim=azim)
  ax.plot(data_.get(labels[0]), data_.get(labels[1]), data_.get(labels[2]), marker='.', linestyle='None')

plt.savefig('1-6_cancer.png')

model = PCA().fit(data)
print(model.components_)
print(model.explained_variance_)
print(model.explained_variance_ratio_)
