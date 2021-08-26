import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import pandas as pd
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from seaborn import scatterplot
from typing import List


def set_layout() -> List[Axes]:
  areas = []
  f = plt.figure(figsize=[5, 10], dpi=100)
  gs = f.add_gridspec(2, 1)
  areas.append(f.add_subplot(gs[0]))
  areas.append(f.add_subplot(gs[1]))
  return areas


def main() -> None:
  data, class_= make_blobs(random_state=5, centers=4)
  df = pd.DataFrame(data, columns=['x', 'y'])

  model = KMeans(n_clusters=4, random_state=0).fit(df)
  df['class_kmeans'] = model.predict(df)
  df['class'] = class_

  print(df)

  areas = set_layout()
  areas[0].set_title('scatter plot')
  scatterplot(data=df, x='x', y='y', hue='class', ax=areas[0])
  areas[1].set_title('clustering with KMeans')
  scatterplot(data=df, x='x', y='y', hue='class_kmeans', ax=areas[1])

  plt.savefig('clustering.png')


if __name__ == '__main__':
  main()
