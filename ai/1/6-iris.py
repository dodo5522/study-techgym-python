from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

DATASET = load_iris()
print(DATASET.get('DESCR'))

feature_names = DATASET.get('feature_names')
class_names = ['Iris-Setosa', 'Iris-Versicolour', 'Iris-Virginica']
class_colors = ['Red', 'Green', 'Blue']
exp_data = pd.DataFrame(DATASET.get('data'), columns=DATASET.get('feature_names'))
target_data = pd.DataFrame(DATASET.get('target'), columns=['class'])
target_data['class_name'] = [class_names[i] for i in target_data.get('class')]
concat_data = pd.concat([exp_data, target_data], axis=1)

print(concat_data.info())

fig = plt.figure(figsize=(10, 20), dpi=80)
gs = fig.add_gridspec(nrows=4, ncols=2)

# 3D plot to check iris data relation
ax3d = []
for i in range(4):
  ax = fig.add_subplot(gs[i], projection='3d')
  ax.view_init(30, 20)
  ax3d.append(ax)

ax3d[0].set_xlabel(feature_names[0])
ax3d[0].set_ylabel(feature_names[1])
ax3d[0].set_zlabel(feature_names[2])
for i, class_name in enumerate(class_names):
  class_data = concat_data[concat_data['class_name'] == class_name]
  ax3d[0].plot(class_data.get(feature_names[0]), class_data.get(feature_names[1]), class_data.get(feature_names[2]), marker='.', linestyle='None', color=class_colors[i])

ax3d[1].set_xlabel(feature_names[0])
ax3d[1].set_ylabel(feature_names[1])
ax3d[1].set_zlabel(feature_names[3])
for i, class_name in enumerate(class_names):
  class_data = concat_data[concat_data['class_name'] == class_name]
  ax3d[1].plot(class_data.get(feature_names[0]), class_data.get(feature_names[1]), class_data.get(feature_names[3]), marker='.', linestyle='None', color=class_colors[i])

ax3d[2].set_xlabel(feature_names[2])
ax3d[2].set_ylabel(feature_names[3])
ax3d[2].set_zlabel(feature_names[0])
for i, class_name in enumerate(class_names):
  class_data = concat_data[concat_data['class_name'] == class_name]
  ax3d[2].plot(class_data.get(feature_names[2]), class_data.get(feature_names[3]), class_data.get(feature_names[0]), marker='.', linestyle='None', color=class_colors[i])

ax3d[3].set_xlabel(feature_names[2])
ax3d[3].set_ylabel(feature_names[3])
ax3d[3].set_zlabel(feature_names[1])
for i, class_name in enumerate(class_names):
  class_data = concat_data[concat_data['class_name'] == class_name]
  ax3d[3].plot(class_data.get(feature_names[2]), class_data.get(feature_names[3]), class_data.get(feature_names[1]), marker='.', linestyle='None', color=class_colors[i])

scaled_exp_data = StandardScaler().fit_transform(exp_data)
pca_data = PCA(n_components=2).fit_transform(scaled_exp_data)
concat_data = pd.concat([pd.DataFrame(pca_data, columns=['pca1', 'pca2']), target_data], axis=1)

sns.scatterplot(data=concat_data, x='pca1', y='pca2', hue='class_name', ax=fig.add_subplot(gs[4:]))
plt.savefig('1-6_iris.png')
