import numpy as np
import pandas as pd

# refer to pandas doc
# https://pandas.pydata.org/pandas-docs/stable/index.html

feature1 =['gender','age','win','lose','draw']
feature2 =['性別','年齢','勝ち','負け','あいこ']
id = ['100','101','102','103','104','105','106','107','108','109']
num = ['0','1','2','3','4','5','6','7','8','9']

hand = {'性別'  :['男性','男性','女性','男性','女性','男性','女性','女性','男性','男性'],
        '年齢'  :['30代','20代','10代','10代','40代','50代','40代','10代','20代','10代'],
        '勝ち'  :[20,21, 4,60,14,10,12,19,12,14],
        '負け'  :[24,15,35, 3,35,29, 2,12,11,43],
        'あいこ':[15,40,34,29,14, 4,22,17,12,10]}

#データフレームの生成
hand_df = pd.DataFrame(hand)

#表示
print('性別が男性がどうか')
print(hand_df['性別'] == '男性')

print('性別が男性である行')
print(hand_df.where(hand_df['性別'] == '男性').dropna())

print('年齢の列のみ削除')
print(hand_df.drop(['年齢',], axis=1))

print('転置')
print(hand_df.transpose())

print('indexを変更して先頭三行の表示')
new_index=['e','b','a','d','c','f','g','h','i','j']
hand_df = pd.DataFrame(hand, index=new_index)
print(hand_df)

print(hand_df[['性別', '勝ち',]].groupby(['性別',]).max())
print(hand_df[['性別', '勝ち',]].groupby(['性別',]).min())
print(hand_df[['性別', '勝ち',]].groupby(['性別',]).mean())

print('勝ちの回数でソート')
print(hand_df.sort_values('勝ち'))

#print('あいこを全て欠損値にして表示')
#hand_df['あいこ'] = np.nan
#print(hand_df)
#
#print('欠損値がいくつあるか表示する')
#print(hand_df.isna().sum())
#print(hand_df.isnull().sum())

#index,columnsを複数つけ、さらに名前を指定する
hand_df2 = hand_df.copy()

#index columnsのレベル1を削除する
hand_df2.columns = [feature1, feature2]
hand_df2.columns.names = ['en', 'ja']
hand_df2.index = [id, num]
hand_df2.index.names = ['index', 'NUM']
print(hand_df2)
#hand_df2.columns = hand_df2.columns.droplevel(1)
#print(hand_df2)
#hand_df2.index = hand_df2.index.droplevel(1)
#print(hand_df2)

#Columnがgenderのデータのみ表示
print(hand_df2['gender'])
print(hand_df2[['gender']])

#Indexが106のところを削除,行方向に合計する場合は、axisパラメータを0に設定
print(hand_df2.drop('106', axis=0))

#Columnがgenderのところを削除,列方向に合計する場合は、axisパラメータを1に設定
print(hand_df2.drop('gender', axis=1))
