import io
import logging
import matplotlib.pyplot as plt
import os
import pandas as pd
import requests
import seaborn as sns
from sklearn import linear_model
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


def wine() -> pd.DataFrame:
  print(get_data(f'{DB_BASE_URL}/wine/wine.names').read())
  df = get_dataframe(f'{DB_BASE_URL}/wine/wine.data', False)
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
  return df


def dump_wine(df: pd.DataFrame, show_figure: bool = True) -> None:
  print(df.groupby('class').size())
  print(df.info())
  print(df.describe())

  X = df.get(['Alcohol'])
  Y = df.get('Color intensity')

  model = linear_model.LinearRegression().fit(X, Y)
  print(f'coef: {model.coef_}, intercept: {model.intercept_}, score: {model.score(X, Y)}')

  sns.pairplot(df.get([
    'class',
    'Alcohol',
    'Malic acid',
    'Ash',
    'Total phenols',
    'Color intensity',
  ]), hue='class', diag_kind='hist')

  if show_figure:
    plt.show()
  else:
    plt.savefig('wine.png')


if __name__ == '__main__':
  df = wine()
  dump_wine(df, True)
