import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn import neighbors
from sklearn.metrics import accuracy_score
from collections import deque
from sklearn.cross_validation import train_test_split
import matplotlib.pyplot as plt

df = pd.read_csv('../../../data/000300_index.csv')
df.index =  df['date']
df.sort_index(inplace=True)
print(df.head())

#计算收益率
df['return'] = df['close']/df['close'].shift(1) - 1
#计算涨跌
df['up_or_down'] = df['close'] > df['close'].shift(1)
se = df['up_or_down']

clf1 = RandomForestClassifier()
clf2 = svm.LinearSVC()
clf3 = neighbors.KNeighborsClassifier()

window = 3
index = window
x = deque()
y = deque()

for index in range(index, len(se)-1, 1):
    target = se[index + 1]
    x.append(list(se[(index - window): index]))
    y.append(se[index])


x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

clf1.fit(x_train, y_train)
clf2.fit(x_train, y_train)
clf3.fit(x_train, y_train)

y_pred1 = clf1.predict(x_test)
y_pred2 = clf2.predict(x_test)
y_pred3 = clf3.predict(x_test)

print('=============预测准确率================')
print('随机森林:',accuracy_score(y_test, y_pred1))
print('SVM:',accuracy_score(y_test,y_pred2))
print('KNN:',accuracy_score(y_test, y_pred3))
