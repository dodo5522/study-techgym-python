import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import requests
from sklearn.cluster import KMeans


DB_BASE_URL = 'https://archive.ics.uci.edu/ml/machine-learning-databases/00468/online_shoppers_intention.csv'


def get_data(url: str) -> pd.DataFrame:
  data_file = os.path.basename(url)

  if os.path.isfile(data_file):
    print(f'{data_file} already exists')
  else:
    res = requests.get(url)

    if res.status_code != 200:
      print(res.content.decode('utf-8'))
      return ''

    with open(data_file, 'w') as fp:
      if fp.write(res.content.decode('utf-8')) <= 0:
        print(f'Cannot write the below content to {data_file}')
        print(res.content.decode('utf-8'))
        return ''

  return pd.read_csv(data_file)


if __name__ == '__main__':
  columns = [
    'Administrative_Duration',
    'Informational_Duration',
    'ProductRelated_Duration',
    'SpecialDay',
    'Region']

  #pd.set_option('display.max_rows', 100)
  #pd.set_option('display.max_columns', 100)

  data = get_data(DB_BASE_URL)
  print(data.shape)
  print(data.columns)
  print(data.head(5))

  data = data.get(columns)
  model = KMeans(n_clusters=6, init='k-means++', random_state=0).fit(data)
  labels = pd.Series(model.labels_, name='class')
  data['class'] = labels

  if False:
    value_counts = labels.value_counts()
    print(value_counts)
    ax = value_counts.plot(kind='bar')
    ax.set_xlabel('class')
    ax.set_ylabel('number')
    plt.show()

  bins_sp = [i for i in np.arange(0, 1.1, 0.2)]
  cut_sp = pd.cut(data.get('SpecialDay'), bins_sp, right=False)
  special_days = pd.concat([data.get('class'), cut_sp], axis=1)
  special_days_sub = special_days.groupby(['class', 'SpecialDay']).size().unstack()
  ax1 = special_days_sub.plot(kind='bar')
  ax1.set_xlabel('class')
  ax1.set_ylabel('number')
  print(special_days_sub)
  plt.savefig('1-4_specialday.png')

  bins_r = [i for i in range(1, 10, 1)]
  cut_r = pd.cut(data.get('Region'), bins_r, right=False)
  region = pd.concat([data.get('class'), cut_r], axis=1)
  region_sub = region.groupby(['class', 'Region']).size().unstack()
  ax2 = region_sub.plot(kind='bar')
  ax2.set_xlabel('class')
  ax2.set_ylabel('number')
  print(region_sub)
  plt.savefig('1-4_region.png')
