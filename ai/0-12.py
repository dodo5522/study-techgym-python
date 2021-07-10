import logging
import os
import pandas as pd
import requests


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
  print(df)
  print(df.info())


if __name__ == '__main__':
  main()
