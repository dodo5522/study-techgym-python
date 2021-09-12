from sklearn.datasets import load_iris
import matplotlib.pyplot as plt
import pandas as pd

DATASET = load_iris()
print(DATASET.get('DESCR'))

exp_data = pd.DataFrame(DATASET.get('data'), columns=DATASET.get('feature_names'))
target_data = pd.DataFrame(DATASET.get('target'), columns=['class'])
target_data['name'] = ['Iris-Setosa' if i == 0 else 'Iris-Versicolour' if i == 1 else 'Iris-Virginica' for i in target_data.get('class')]

print(exp_data.info())
print(target_data.info())

fig = plt.figure(figsize=(12, 24), dpi=100)
gs = fig.add_gridspec(nrows=4, ncols=2)

ax3d = []
for i in range(4):
  ax = fig.add_subplot(gs[i], projection='3d')
  ax.view_init(30, 40)
  ax3d.append(ax)

ax3d[0].set_xlabel(exp_data.columns[0])
ax3d[0].set_ylabel(exp_data.columns[1])
ax3d[0].set_zlabel(exp_data.columns[2])
ax3d[0].plot(exp_data.get(exp_data.columns[0]), exp_data.get(exp_data.columns[1]), exp_data.get(exp_data.columns[2]), marker='.', linestyle='None')

ax3d[1].set_xlabel(exp_data.columns[0])
ax3d[1].set_ylabel(exp_data.columns[1])
ax3d[1].set_zlabel(exp_data.columns[3])
ax3d[1].plot(exp_data.get(exp_data.columns[0]), exp_data.get(exp_data.columns[1]), exp_data.get(exp_data.columns[3]), marker='.', linestyle='None')

ax3d[2].set_xlabel(exp_data.columns[2])
ax3d[2].set_ylabel(exp_data.columns[3])
ax3d[2].set_zlabel(exp_data.columns[0])
ax3d[2].plot(exp_data.get(exp_data.columns[2]), exp_data.get(exp_data.columns[3]), exp_data.get(exp_data.columns[0]), marker='.', linestyle='None')

ax3d[3].set_xlabel(exp_data.columns[2])
ax3d[3].set_ylabel(exp_data.columns[3])
ax3d[3].set_zlabel(exp_data.columns[1])
ax3d[3].plot(exp_data.get(exp_data.columns[2]), exp_data.get(exp_data.columns[3]), exp_data.get(exp_data.columns[1]), marker='.', linestyle='None')

plt.show()
