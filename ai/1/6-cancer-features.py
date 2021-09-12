import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.datasets import load_breast_cancer
from sklearn.preprocessing import StandardScaler

DATASET = load_breast_cancer()

data_ = pd.DataFrame(DATASET.get('data'))
data = pd.DataFrame(StandardScaler(copy=True).fit_transform(data_), columns=DATASET.get('feature_names'))
target = pd.Series(DATASET.get('target'), name='malignant or benign')

print(DATASET.get('DESCR'))
print(data.info())

target_columns = [
  'mean radius',
  'mean texture',
  'mean perimeter',
  'mean area',
  'mean smoothness',
  'mean compactness',
  'mean concavity',
  'mean concave points',
  'mean symmetry',
  'mean fractal dimension',
]

sns.pairplot(data[target_columns])
plt.savefig('1-6_cancer_features.png')
