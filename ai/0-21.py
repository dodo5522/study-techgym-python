import pandas as pd
from sklearn import linear_model
from sklearn import metrics


CSV_TRAIN = 'dataset/house-prices-advanced-regression-techniques/train.csv'
CSV_TEST = 'dataset/house-prices-advanced-regression-techniques/test.csv'


def get_dataframe(path: str, header = 0) -> pd.DataFrame:
  return pd.read_csv(path, header=(None if header is False else 0))


def create_model(data: pd.DataFrame, explanatory_label: str, objective_label: str) -> linear_model.LinearRegression:
  m = linear_model.LinearRegression()
  m.fit(data.get([explanatory_label]), data.get(objective_label))
  return m


if __name__ == '__main__':
  train = get_dataframe(CSV_TRAIN)
  test = get_dataframe(CSV_TEST)

  pd.set_option('display.max_rows', 100)
  pd.set_option('display.max_columns', 100)

  model = create_model(train, 'OverallQual', 'SalePrice')
  predict_y = model.predict(test.get(['OverallQual']))

  print(model.coef_)
  print(model.intercept_)
  print(model.score(train.get(['OverallQual']), train.get('SalePrice')))
  print(predict_y)

  submission_data = pd.DataFrame({'Id': test.get('Id'), 'SalePrice': predict_y})
  print(submission_data)

  submission_data.to_csv('submission.csv', index=False)
