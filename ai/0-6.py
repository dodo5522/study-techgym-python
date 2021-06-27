import pandas as pd
import numpy as np

# pandas API doc
# https://pandas.pydata.org/pandas-docs/stable/index.html

feature1_en = ['gender','age','win','lose','draw']
feature1_ja = ['性別','年齢','勝ち','負け','あいこ']

hand = {
  '性別'  :['男性','男性','女性','男性','女性','男性','女性','女性','男性','男性'],
  '年齢'  :['30代','20代','10代','10代','40代','50代','40代','10代','20代','10代'],
  '勝ち'  :[20,21, 4,60,14,10,12,19,12,14],
  '負け'  :[24,15,35, 3,35,29, 2,12,11,43],
  'あいこ':[15,40,34,29,14, 4,22,17,12,10]}
hand_df1 = pd.DataFrame(hand)
hand_df1.columns = [feature1_en, feature1_ja]
hand_df1.columns.names = ['feature', '特徴']

# idを追加してindexとして用いる
# https://www.geeksforgeeks.org/adding-new-column-to-existing-dataframe-in-pandas/
id1 = ['100','101','102','103','104','105','106','107','108','109']
hand_df1 = hand_df1.assign(id = id1).set_index('id')

print(hand_df1)

feature2_en =['address','hobby','job']
feature2_ja =['住所','趣味','仕事']

hand2 = {
  '住所'  :['東京','大阪','名古屋','北海道','東京','鹿児島','大阪','名古屋','東京','大阪'],
  '趣味'  :['野球','賭博','じゃんけん','野球','賭博','野球','じゃんけん','賭博','野球','じゃんけん'],
  '仕事'  :['IT','医療','弁護士','事務','事務','弁護士','IT','IT','IT','事務']}

hand_df2 = pd.DataFrame(hand2)
hand_df2.columns = [feature2_en, feature2_ja]
hand_df2.columns.names = ['feature', '特徴']

# idを追加してindexとして用いる
id2 = ['100','101','102','103','110','111','106','113','108','114']
hand_df2 = hand_df2.assign(id = id2).set_index('id')

print(hand_df2)
print(hand_df1.merge(hand_df2, how='inner', on='id'))
print(hand_df1.merge(hand_df2, how='outer', on='id'))
print(hand_df1.merge(hand_df2, how='left', on='id'))
print(hand_df1.merge(hand_df2, how='right', on='id'))
print(hand_df1.merge(hand_df2, how='cross'))
