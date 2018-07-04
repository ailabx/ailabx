
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm

from sklearn import metrics
from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split

class StockRanker(object):
    def __init__(self,algorithm='gbdt'):
        algo = GradientBoostingClassifier(random_state=10)
        if algorithm == 'gbdt':
            algo = GradientBoostingClassifier(random_state=10)
        if algorithm == 'svm':
            algo = svm.LinearSVC()
        if algorithm == 'rf':
            algo = RandomForestClassifier()
        self.algo = algo

    def train(self,X,y):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
        self.algo.fit(X_train,y_train)
        print('模型训练完成!')
        y_train_pred = self.algo.predict(X_train)
        print("在训练上Accuracy : %.4g" % metrics.accuracy_score(y_train.values, y_train_pred))
        y_pred = self.algo.predict(X_test)
        print("在测试集上Accuracy : %.4g" % metrics.accuracy_score(y_test.values, y_pred))