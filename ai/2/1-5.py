from sklearn.datasets import load_breast_cancer
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


if __name__ == '__main__':
  target_names = load_breast_cancer().get('target_names')
  target = pd.DataFrame(load_breast_cancer().get('target'), columns=['target'])
  feature_names = load_breast_cancer().get('feature_names')
  data_ = pd.DataFrame(load_breast_cancer().get('data'), columns=feature_names)
  data = pd.concat([data_, target], axis=1)

  desc = load_breast_cancer().get('DESCR')
  print(desc)

  target_num = 3
  target_name = 'mean radius'
  ax = []
  f = plt.figure(figsize=[8 * target_num, 8], dpi=200)
  gs = f.add_gridspec(nrows=1, ncols=target_num)
  for i in range(target_num):
    ax.append(f.add_subplot(gs[i]))
    ax[i].set_xlabel('Mean of distance for each cell nucleus')
    ax[i].set_ylabel('Density: Number of cell nucleus')

  hist_target_names = filter(lambda c: 'mean' in c, data.columns)

  sns.set_style('darkgrid')
  a = sns.histplot(data=data, x=target_name, bins=32, ax=ax[0])
  a.set_title(f'{target_name} (hist)')
  a = sns.kdeplot(data=data, x=target_name, ax=ax[1])
  a.set_title(f'{target_name} (kde)')
  a = sns.histplot(data=data, x=target_name, kde=True, ax=ax[2])
  a.set_title(f'{target_name} (hist + kde)')
  plt.savefig(f'{target_name.replace(" ", "_")}.png')

  data.get(hist_target_names).hist(bins=32, figsize=[16, 40], layout=[5, 2])
  plt.tight_layout()
  plt.savefig('mean_hist.png')
