#AI-TECHGYM-N-8

import pandas as pd

# データの準備
hand1 = {'id'  :['100','101','102','103','104','105','106','107','108','109'],
    'gender'  :['男性','男性','女性','男性','女性','男性','女性','女性','男性','男性'],
    'age'  :['30代','20代','10代','10代','40代','50代','40代','10代','20代','10代'],
    'address'  :['東京','大阪','名古屋','北海道','東京','鹿児島','大阪','名古屋','東京','大阪'],
    'hobby'  :['野球','ルーレット','じゃんけん','野球','ルーレット','野球','じゃんけん','ルーレット','野球','じゃんけん'],
    'job'  :['IT','医療','弁護士','事務','事務','弁護士','IT','IT','IT','事務'],
    'win'  :[20,21, 4,60,14,10,12,19,12,14],
    'lose'  :[24,15,35, 3,35,29, 2,12,11,43],
    'draw':[15,40,34,29,14, 4,22,17,12,10]}

hand_df1 = pd.DataFrame(hand1)

#分割の粒度
bins = [1, 20, 40]

#ビン分割の実施
hand_df1_draw_bins_cut = pd.cut(hand_df1.get('draw'), bins)
print(hand_df1_draw_bins_cut)

#中央値で2分割
hand_df1_draw_cut = pd.cut(hand_df1.get('draw'), 2)
print(hand_df1_draw_cut)

#データ個数が均等になるように2分割
hand_df1_draw_qcut = pd.qcut(hand_df1.get('draw'), 2)
print(hand_df1_draw_qcut)

# bins by cut, qcut
_, bins_cut = pd.cut(hand_df1.get('draw'), 2, retbins=True)
_, bins_qcut = pd.qcut(hand_df1.get('draw'), 2, retbins=True)
print(bins_cut)
print(bins_qcut)
