import pandas as pd
import numpy as np
import os


# データの準備
hand = {'id'  :['100','101','102','103','104','105','106','107','108','109'],
   'gender'  :['男性','男性','女性','男性','女性','男性','女性','女性','男性','男性'],
   'age'  :['30代','20代','10代','10代','40代','50代','40代','10代','20代','10代'],
   'address'  :['東京','大阪','名古屋','北海道','東京','鹿児島','大阪','名古屋','東京','大阪'],
   'hobby'  :['野球','ルーレット','じゃんけん','野球','ルーレット','野球','じゃんけん','ルーレット','野球','じゃんけん'],
   'job'  :['IT','医療','弁護士','事務','事務','弁護士','IT','IT','IT','事務'],
   'win'  :[20,21, 4,60,14,10,12,19,12,14],
   'lose'  :[24,15,35, 3,35,29, 2,12,11,43],
   'draw':[15,40,34,29,14, 4,22,17,12,10]}
hand_df1 = pd.DataFrame(hand)
print(hand_df1)

#サイズ情報
print(hand_df1.groupby('age').size())

#ageを軸に、winの平均値を求める
# DataFrame.groupby(by=None, axis=0, ...
# by mapping, function, label, or list of labels
print(hand_df1.groupby('age').win.mean())
print(hand_df1.groupby(['age', 'gender', 'address']).win.mean())

#各年齢のDataFrameを表示する
for g, df in hand_df1.groupby('age'):
  print(g)
  print(df.values)

#年齢別での勝ち回数、平均、最大、最小
print(hand_df1.groupby('age').win.aggregate(['count', 'mean', 'max', 'min']))

#2行 1列目 をNaNに変更 (index base)
hand_df1.iloc[1, 0] = np.nan
print(hand_df1)

#2行 1列目 をNaNに変更 (label base)
hand_df1 = pd.DataFrame(hand)
hand_df1.loc[1, 'id'] = np.nan
print(hand_df1)
hand_df1 = pd.DataFrame(hand)
hand_df1.loc[hand_df1.get('id') == '101', 'id'] = np.nan
print(hand_df1)

#7行 7列目 をNaNに変更
hand_df1.iloc[6, 6] = np.nan
#3~4行 3列目 をNaNに変更
hand_df1.iloc[2:4, 2] = np.nan
#6~最終行目 4列目 をNaNに変更
hand_df1.iloc[5:, 3] = np.nan
print(hand_df1)
print(hand_df1.isna().sum())

# fillna with some methods
print(hand_df1.dropna())
print(hand_df1.fillna(0))
print(hand_df1.ffill())
print(hand_df1.bfill())
print(hand_df1.fillna(hand_df1.mean()))

hand_df1.fillna(hand_df1.mean()).to_csv(os.path.join(os.path.curdir, 'fillna_with_mean.csv'))
