import logging
import matplotlib.pyplot as plt
import os
import pandas as pd
import requests
import seaborn as sns


logger = logging.getLogger('main')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


def get_data(url: str) -> pd.DataFrame:
  data_set_file = os.path.basename(url)

  if os.path.isfile(data_set_file):
    logger.info(f'{data_set_file} already exists')
  else:
    res = requests.get(url)

    if res.status_code != 200:
      logger.err(res.content.decode('utf-8'))
      return pd.DataFrame()

    with open(data_set_file, 'w') as fp:
      if fp.write(res.content.decode('utf-8')) <= 0:
        logger.err(f'Cannot write the below content to {data_set_file}')
        logger.err(res.content.decode('utf-8'))
        return pd.DataFrame()

  return pd.read_csv(data_set_file)


def main() -> None:
  df = get_data('https://archive.ics.uci.edu/ml/machine-learning-databases/balloons/adult+stretch.data')
  df.columns = ['color', 'size', 'act', 'age', 'inflated']
  print(df)

  crossed_df = pd.crosstab(df.get('size'), df.get('color'))
  print(crossed_df)

  plt.subplot(3, 1, 1)
  sns.countplot(y='color', data=df)

  plt.subplot(3, 1, 2)
  sns.countplot(y='color', hue='age', hue_order=['CHILD', 'ADULT'], data=df)

  plt.subplot(3, 1, 3)
  sns.countplot(y='color', hue='size', hue_order=['SMALL', 'LARGE'], data=df)

  plt.show()


if __name__ == '__main__':
  main()
