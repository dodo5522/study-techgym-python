import io
import logging
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec
import matplotlib.pyplot as plt
import os
import pandas as pd
import requests
import seaborn as sns
from sklearn import linear_model
from typing import TextIO, List, Dict


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


def set_layout() -> List[plt.Axes]:
  """
  |---------|----|
  | (1) (2) |2(3)|
  |    1    |----|
  | (4) (5) |3(6)|
  |---------|----|
  """
  figsize=(12.8, 6.4)  # width, height
  f = plt.figure(figsize=figsize, dpi=200)
  gs = GridSpec(nrows=2, ncols=3, height_ratios=[1, 1])

  gs1 = GridSpecFromSubplotSpec(nrows=2, ncols=2, subplot_spec=gs[0:2, 0:2])
  area1 = f.add_subplot(gs1[:, :])

  gs23 = GridSpecFromSubplotSpec(nrows=2, ncols=1, subplot_spec=gs[0:2, 2])
  area2 = f.add_subplot(gs23[0, :])
  area3 = f.add_subplot(gs23[1, :])

  return area1, area2, area3


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


def create_models(
    df: pd.DataFrame,
    explanatory_label: str,
    objective_labels: List[str]) -> Dict[str, linear_model._base.LinearModel]:
  return {label: linear_model.LinearRegression().fit(
    df.get([explanatory_label]), df.get(label))
      for label in objective_labels}


def dump_wine(df: pd.DataFrame) -> None:
  print(df.groupby('class').size())
  print(df.info())
  print(df.describe())

  explanatory_label = 'Alcohol'
  objective_labels = ['Malic acid', 'Ash', 'Total phenols', 'Color intensity']
  models = create_models(df, explanatory_label, objective_labels)

  for label in models.keys():
    model = models.get(label)
    X = df.get([explanatory_label])
    Y = df.get(label)

    a1, a2, a3 = set_layout()

    sns.scatterplot(
      x=explanatory_label,
      y=label,
      hue='class',
      data=df,
      ax=a1
    )

    predicted_Y = model.predict(df.get(['Alcohol']))
    score = model.score(X, Y)
    a1.plot(X, predicted_Y)
    a1.text(
      X.min(),
      predicted_Y.min(),
      f'coef: {model.coef_[0]:.2f}\nintercept: {model.intercept_:.2f}\nscore: {score:.2f}',
      bbox=dict(facecolor='white', alpha=0.5))

    a2.set_xlabel('Alcohol')
    a2.hist(df.get('Alcohol'))
    a3.set_xlabel('Color intensity')
    a3.hist(df.get('Color intensity'))

    plt.show()


if __name__ == '__main__':
  df = wine()
  dump_wine(df)
