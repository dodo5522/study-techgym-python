import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import pandas as pd
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from seaborn import scatterplot
from typing import List


def set_layout() -> List[Axes]:
  areas = []
  nrows, ncols = 4, 2

  f = plt.figure(figsize=[10, 20], dpi=100)
  gs = f.add_gridspec(nrows, ncols)

  for i in range(nrows * ncols):
    areas.append(f.add_subplot(gs[i]))

  return areas


def main() -> None:
  areas = set_layout()
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

  plt.savefig('clustering.png')


if __name__ == '__main__':
  main()
