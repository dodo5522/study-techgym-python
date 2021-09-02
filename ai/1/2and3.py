import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import pandas as pd
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from seaborn import scatterplot
from typing import List


def set_layout(nrows: int, ncols: int, f_height: int, f_width: int) -> List[Axes]:
  areas = []
  f = plt.figure(figsize=[f_width, f_height], dpi=100)
  gs = f.add_gridspec(nrows, ncols)

  for i in range(nrows * ncols):
    areas.append(f.add_subplot(gs[i]))

  return areas


def plot_random_state_multi() -> None:
  # plot behavior of random state with 0, 5, 10, 15
  areas = set_layout(4, 2, 20, 10)
  for i, random_state in enumerate(range(0, 20, 5)):
    data, class_= make_blobs(random_state=random_state, centers=4)
    df = pd.DataFrame(data, columns=['x', 'y'])

    print(df)

    model = KMeans(init='random', n_clusters=4).fit(df)
    df['class_kmeans'] = model.predict(df)
    df['class'] = class_

    areas[i * 2].set_title(f'scatter plot {random_state}')
    scatterplot(data=df, x='x', y='y', hue='class', ax=areas[i * 2])
    areas[i * 2 + 1].set_title(f'clustering with KMeans {random_state}')
    scatterplot(data=df, x='x', y='y', hue='class_kmeans', ax=areas[i * 2 + 1])

  plt.savefig('clustering_behavior_random_state.png')


def plot_elbow_method() -> None:
  data = []
  d, _ = make_blobs(random_state=5, centers=4)
  data.append(d)
  d, _ = make_blobs(random_state=10, centers=4)
  data.append(d)

  areas = set_layout(2, 2, 20, 20)
  areas[0].set_title('random state 5')
  areas[2].set_title('random state 10')

  # plot scatter with random state 5 and 10 and SSE
  n_clusters = [i for i in range(1, 11)]
  for i, data_ in enumerate(data):
    # plot scatter
    scatterplot(data=pd.DataFrame(data_, columns=['x', 'y']), x='x', y='y', ax=areas[i * 2])

    # make SSE list for 1-10 and plot it
    inertias = []
    for n in n_clusters:
      model = KMeans(n_clusters=n, init='random', random_state=0).fit(data_)
      inertias.append(model.inertia_)

    areas[i * 2 + 1].set_xlabel('clusters')
    areas[i * 2 + 1].set_ylabel('distortion')
    areas[i * 2 + 1].plot(n_clusters, inertias)

  plt.savefig('clustering_sse.png')


if __name__ == '__main__':
  plot_elbow_method()
