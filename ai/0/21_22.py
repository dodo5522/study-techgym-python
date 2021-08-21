import copy
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn import linear_model
from sklearn import metrics
import sys
from typing import List


CSV_TRAIN = '../dataset/house-prices-advanced-regression-techniques/train.csv'
CSV_TEST = '../dataset/house-prices-advanced-regression-techniques/test.csv'


def get_dataframe(path: str, header = 0) -> pd.DataFrame:
  return pd.read_csv(path, header=(None if header is False else 0))

def create_model(data: pd.DataFrame, explanatory_labels: List[str], objective_label: str) -> linear_model.LinearRegression:
  m = linear_model.LinearRegression()
  labels = copy.deepcopy(explanatory_labels)
  labels.append(objective_label)
  d = data.get(labels).dropna()
  m.fit(d.get(explanatory_labels), d.get(objective_label))
  return m

def get_top_corr(data: pd.DataFrame, objective_label: str, top_n: int) -> List[str]:
  corr = data.select_dtypes(include=['number']).dropna().corr()
  corr[objective_label + 'Abs'] = corr.get(objective_label).abs().drop(['Id'])
  top_corr = corr.sort_values(objective_label + 'Abs', ascending=False).head(top_n)
  return top_corr.drop(objective_label + 'Abs', axis=1)


if __name__ == '__main__':
  #pd.set_option('display.max_rows', 100)
  #pd.set_option('display.max_columns', 100)

  train = get_dataframe(CSV_TRAIN)
  test = get_dataframe(CSV_TEST)
  objective_label = 'SalePrice'

  top_corr = get_top_corr(train, objective_label, 15)
  top_corr_and_objective_labels = top_corr.index.to_list()
  top_corr_labels = copy.deepcopy(top_corr_and_objective_labels)
  top_corr_labels.remove(objective_label)
  top_corr_and_id_labels = copy.deepcopy(top_corr_labels)
  top_corr_and_id_labels.append('Id')

  print(top_corr)
  print(top_corr_labels)
  print(top_corr_and_objective_labels)
  print(top_corr_and_id_labels)

  sns.pairplot(data=train.get(top_corr_and_objective_labels))
  plt.savefig('house_pair_top_corr.png')

  model = create_model(train, top_corr_labels, objective_label)

  test_X_id = test.get(top_corr_and_id_labels).fillna(0)
  test_X = test_X_id.drop('Id', axis=1)
  predict_y = model.predict(test_X)

  print(model.coef_)
  print(model.intercept_)
  #print(model.score(train.get(['OverallQual']), train.get('SalePrice')))
  print(predict_y)

  submission_data = pd.DataFrame({'Id': test_X_id.get('Id'), objective_label: predict_y})
  print(submission_data)

  submission_data.to_csv('submission.csv', index=False)
