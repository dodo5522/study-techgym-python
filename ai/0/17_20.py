import io
import logging
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec
import matplotlib.pyplot as plt
import os
import pandas as pd
import requests
import seaborn as sns
import scipy as sp
from sklearn import linear_model
from sklearn import metrics
from sklearn.model_selection import train_test_split
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
  |---|---|---|---|---|---|---|
  |   |           |   | 2 | 5 |
  |---|     1     |---|---|---|
  |   |           |   | 3 | 6 |
  |---|---|---|---|---|---|---|
  |   |   |   |   |   | 4 | 7 |
  |---|---|---|---|---|---|---|
  """
  areas = []
  figsize=(11.2, 4.8)  # width, height
  f = plt.figure(figsize=figsize, dpi=200)
  gs = GridSpec(nrows=3, ncols=7, height_ratios=[1, 1, 1])

  gs1 = GridSpecFromSubplotSpec(nrows=3, ncols=3, subplot_spec=gs[0:2, 1:4])
  areas.append(f.add_subplot(gs1[:, :]))

  gs234 = GridSpecFromSubplotSpec(nrows=3, ncols=1, subplot_spec=gs[0:3, 5])
  areas.append(f.add_subplot(gs234[0, :]))
  areas.append(f.add_subplot(gs234[1, :]))
  areas.append(f.add_subplot(gs234[2, :]))

  gs567 = GridSpecFromSubplotSpec(nrows=3, ncols=1, subplot_spec=gs[0:3, 6])
  areas.append(f.add_subplot(gs567[0, :]))
  areas.append(f.add_subplot(gs567[1, :]))
  areas.append(f.add_subplot(gs567[2, :]))

  return areas


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


def dump_wine(df: pd.DataFrame, save_to_file: bool) -> None:
  print(df.groupby('class').size())
  print(df.info())
  print(df.describe())

  objective_label = 'Alcohol'
  explanatory_labels = ['', 'Proline', 'Color intensity', 'Alcalinity of ash', 'Total phenols', 'Magnesium', 'Flavanoids']
  y = df.get(objective_label)

  areas = set_layout()
  sns.heatmap(
    ax=areas[0],
    data=df.corr()
  )

  rs = []
  for n, explanatory_label in enumerate(explanatory_labels):
    if len(explanatory_label) == 0:
      continue

    X = df.get([explanatory_label])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= 0.5, random_state=0)

    model = linear_model.LinearRegression().fit(X_train, y_train)
    y_predict = model.predict(X_test)

    # Pearson correlation coefficient
    # https://blog.amedama.jp/entry/2015/09/28/213745
    # (相関係数, 有意確率)
    # 相関係数は 1 に近いほど強い相関があることを指す
    # 有意確率 P 値は 0 に近いほどデータが偶然そうなった可能性が低いと言える
    r, p = sp.stats.pearsonr(X.get(explanatory_label), y)
    rs.append(r)

    score = model.score(X_test, y_test)
    r2_score = metrics.r2_score(y_test, y_predict)

    desc = f'coef: {model.coef_[0]:.3f}\n'
    desc += f'intercept: {model.intercept_:.3f}\n'
    desc += f'score: {score:.3f}\n'
    print(explanatory_label)
    print(desc + f'r2_score: {r2_score:.3f}' + f'pearsonr: {r:.3f}, {p:.3f}')

    sns.scatterplot(
      x=explanatory_label,
      y=objective_label,
      hue='class',
      data=df,
      ax=areas[n],
      legend=False
    )

    areas[n].plot(X_test, y_predict)
    areas[n].text(X_test.min(), y_predict.min(), explanatory_label + '\n' + desc + f'pearsonr: {r:.3f}', bbox=dict(facecolor='white', alpha=0.5), fontsize=6)

  m = max(rs)
  m_label = explanatory_labels[rs.index(m)]
  print('')
  print(f'Max corelation coefficient with {explanatory_label}: {m_label}')

  # Show ranking of corr
  sorted_corr = df.corr().abs().unstack().sort_values(ascending=False)
  dropped_dup_corr = sorted_corr[sorted_corr.index.map(lambda i: i[0] != i[1])]
  print('')
  print(dropped_dup_corr)

  # Show ranking of corr top 10 (5)
  print('')
  print('coefs Alcohol')
  print(dropped_dup_corr['Alcohol'])

  if save_to_file:
    plt.savefig('wine.png')
  else:
    plt.show()


def multiple_reg_wine(df: pd.DataFrame, explanatory_labels: List[str], objective_label: str, label: str) -> None:
  X = df.get(explanatory_labels)
  y = df.get(objective_label)

  X_train, X_test, y_train, y_test, = train_test_split(X, y, test_size=0.5, random_state=0)
  model = linear_model.LinearRegression().fit(X_train, y_train)

  score_train = model.score(X_train, y_train)
  score_test = model.score(X_test, y_test)
  coefs = pd.Series(model.coef_, index=X.columns)

  print('---')
  print(label)
  print(f'score(train): {score_train:.3f}')
  print(f'score(test) : {score_test:.3f}')
  print(f'intercept   : {model.intercept_:.3f}')
  print(coefs)


def multiple_reg_wine_including_alcalinity(df: pd.DataFrame) -> None:
  explanatory_labels = ['Proline', 'Color intensity', 'Alcalinity of ash', 'Total phenols', 'Magnesium', 'Flavanoids']
  multiple_reg_wine(df, explanatory_labels, 'Alcohol', 'wine_multi_with_alcalinity')


def multiple_reg_wine_excluding_alcalinity(df: pd.DataFrame) -> None:
  explanatory_labels = ['Proline', 'Color intensity', 'Total phenols', 'Magnesium', 'Flavanoids']
  multiple_reg_wine(df, explanatory_labels, 'Alcohol', 'wine_multi')


def multiple_reg_wine_all(df: pd.DataFrame) -> None:
  explanatory_labels = df.columns.drop(['Alcohol'])
  multiple_reg_wine(df, explanatory_labels, 'Alcohol', 'wine_all')


if __name__ == '__main__':
  df = wine()
  dump_wine(df, True)
  multiple_reg_wine_including_alcalinity(df)
  multiple_reg_wine_excluding_alcalinity(df)
  multiple_reg_wine_all(df)
