import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn import cross_validation, metrics

import numpy as np

from sklearn.grid_search import GridSearchCV

import matplotlib.pylab as plt

train = pd.read_csv('train_modified.csv')
print(train.head())
print(train['Disbursed'].value_counts())

target='Disbursed' # Disbursed的值就是二元分类的输出
IDcol = 'ID'
x_columns = [x for x in train.columns if x not in [target, IDcol]]
X = train[x_columns]
y = train['Disbursed']

gbc = GradientBoostingClassifier(random_state=10)
gbc.fit(X,y)

print('模型训练完成!')

y_pred = gbc.predict(X)
print("Accuracy : %.4g" % metrics.accuracy_score(y.values, y_pred))


y_predprobs = gbc.predict_proba(X)
print('概率矩阵：',y_predprobs)
y_predprob = y_predprobs[:,1]
print("AUC Score (Train): %f" % metrics.roc_auc_score(y, y_predprob))