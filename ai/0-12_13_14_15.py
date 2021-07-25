import io
import logging
import matplotlib.pyplot as plt
import os
import pandas as pd
import requests
import seaborn as sns
from typing import TextIO


DB_BASE_URL = 'https://archive.ics.uci.edu/ml/machine-learning-databases'


logger = logging.getLogger('main')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


def get_data(url: str) -> TextIO:
  data_file = os.path.basename(url)

  if os.path.isfile(data_file):
    logger.info(f'{data_file} already exists')
  else:
    res = requests.get(url)

    if res.status_code != 200:
      logger.error(res.content.decode('utf-8'))
      return ''

    with open(data_file, 'w') as fp:
      if fp.write(res.content.decode('utf-8')) <= 0:
        logger.err(f'Cannot write the below content to {data_file}')
        logger.err(res.content.decode('utf-8'))
        return ''

  return io.StringIO(open(data_file, 'r').read())


def get_dataframe(url: str, header: bool) -> pd.DataFrame:
  return pd.read_csv(get_data(url), header=(None if header is False else 0))


def adult_stretch() -> None:
  df = get_dataframe(f'${DB_BASE_URL}/balloons/adult+stretch.data', False)
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


def tic_tac_toe() -> None:
  df = get_dataframe(f'${DB_BASE_URL}/tic-tac-toe/tic-tac-toe.data', False)
  df.columns = [
    'top-left-square',
    'top-middle-square',
    'top-right-square',
    'middle-left-square',
    'middle-middle-square',
    'middle-right-square',
    'bottom-left-square',
    'bottom-middle-square',
    'bottom-right-square',
    'Class',
  ]
  print(df.info())
  print(pd.crosstab(df.get('middle-middle-square'), df.get('Class')))

  for row in range(3):
    for col in range(3):
      i = row * 3 + col
      plt.subplot(3, 3, i + 1)
      sns.countplot(x='Class', hue=df.columns[i], hue_order=['x', 'o', 'b'], data=df)

  plt.show()


def wine() -> None:
  print(get_data(f'${DB_BASE_URL}/wine/wine.names').read())
  df = get_dataframe(f'${DB_BASE_URL}/wine/wine.data', False)
  df.columns = [
    'class',
    'Alcohol',
    'Malic acid',
    'Ash',
    'Alcalinity of ash',
    'Magnesium',
    'Total phenols',
    'Flavanoids',
    'Nonflavanoid phenols',
    'Proanthocyanins',
    'Color intensity',
    'Hue',
    'OD280/OD315 of diluted wines',
    'Proline',
  ]
  print(df.groupby('class').size())
  print(df.info())
  print(df.describe())

  #plt.hist(df.get('Alcohol'), bins=16)
  #plt.show()

  sns.pairplot(df.get([
    'class',
    'Alcohol',
    'Malic acid',
    'Ash',
    'Total phenols',
    'Color intensity',
  ]), hue='class', diag_kind='hist')
  plt.savefig('temp.png')


if __name__ == '__main__':
  wine()
