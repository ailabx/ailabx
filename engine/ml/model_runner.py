# encoding:utf-8
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.model_selection import cross_validate, GridSearchCV

from engine.datafeed.dataset import Dataset
from loguru import logger
from time import time


class ModelRunner:
    def __init__(self, model, ds: Dataset):
        self.model = model
        self.dataset = ds

    def fit(self):
        X_train, y_train = self.dataset.get_train_data()
        self.model.fit(X_train, y_train)

    def predict(self):
        X_test, y_test = self.dataset.get_test_data()
        pred = self.model.predict(X_test)

        score = self.model.score(X_test, y_test)
        logger.debug("准确率得分:{}".format(round(score, 5)))
        return score

    def run_cv(self, cv, fit_params=None, n_jobs=-1):
        start = time()

        metrics = {'balanced_accuracy': 'Accuracy',
                   'roc_auc': 'AUC',
                   'neg_log_loss': 'Log Loss',
                   'f1_weighted': 'F1',
                   'precision_weighted': 'Precision',
                   'recall_weighted': 'Recall'
                   }
        X,y = self.dataset.get_X_y_data()
        scores = cross_validate(estimator=self.model,
                                X=X,
                                y=y,
                                scoring=list(metrics.keys()),
                                cv=cv,
                                return_train_score=True,
                                n_jobs=n_jobs,
                                verbose=1,
                                fit_params=fit_params)
        duration = time() - start
        return scores, duration


if __name__ == '__main__':
    codes = ['000300.SH', '399006.SZ']
    names = []
    fields = []

    fields += ["Corr($close/Ref($close,1), Log($volume/Ref($volume, 1)+1), 30)"]
    names += ["CORR30"]

    fields += ["Corr($close/Ref($close,1), Log($volume/Ref($volume, 1)+1), 60)"]
    names += ["CORR60"]

    fields += ["Ref($close, 5)/$close"]
    names += ["ROC5"]

    fields += ["(2*$close-$high-$low)/$open"]
    names += ['KSFT']

    fields += ["($close-Min($low, 5))/(Max($high, 5)-Min($low, 5)+1e-12)"]
    names += ["RSV5"]

    fields += ["($high-$low)/$open"]
    names += ['KLEN']

    fields += ["$close"]
    names += ['close']

    fields += ['KF(Slope($close,20))']
    names += ['KF']

    fields += ['$close/Ref($close,20)-1']
    names += ['ROC_20']

    fields += ['KF($ROC_20)']
    names += ['KF_ROC_20']

    dataset = Dataset(codes, names, fields, split_date='2020-01-01')

    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.svm import SVC
    from sklearn.linear_model import LogisticRegression
    from engine.ml.model.boosting_models import gb_clf, xgb_clf

    for model in [xgb_clf, gb_clf, LogisticRegression(), RandomForestClassifier(), SVC()]:
        m = ModelRunner(model, dataset)
        m.fit()
        m.predict()


    #m = ModelRunner(xgb_clf, dataset)
    #cv = OneStepTimeSeriesSplit(n_splits=12)

    #dummy_cv_result,time = m.run_cv(cv=5)
    #print(dummy_cv_result, time)

    fi = pd.Series(xgb_clf.feature_importances_,
                   index=dataset.get_X_y_data()[0].columns)
    fi.nlargest(25).sort_values().plot.barh(figsize=(10, 5),
                                            title='Feature Importance')
    sns.despine()
    plt.tight_layout();


    def stack_results(scores):
        metrics = {'balanced_accuracy': 'Accuracy',
                   'roc_auc': 'AUC',
                   'neg_log_loss': 'Log Loss',
                   'f1_weighted': 'F1',
                   'precision_weighted': 'Precision',
                   'recall_weighted': 'Recall'
                   }

        columns = pd.MultiIndex.from_tuples(
            [tuple(m.split('_', 1)) for m in scores.keys()],
            names=['Dataset', 'Metric'])
        data = np.array(list(scores.values())).T
        df = (pd.DataFrame(data=data,
                           columns=columns)
              .iloc[:, 2:])
        results = pd.melt(df, value_name='Value')
        results.Metric = results.Metric.apply(lambda x: metrics.get(x))
        results.Dataset = results.Dataset.str.capitalize()
        return results
    #results = stack_results(dummy_cv_result)
    #results = results.groupby(['Metric', 'Dataset']).Value.mean().unstack()
    #print(results)



    params = {'learning_rate': np.linspace(0.05, 0.25, 5), 'max_depth': [x for x in range(1, 8, 1)], 'min_samples_leaf':
        [x for x in range(1, 5, 1)], 'n_estimators': [x for x in range(50, 100, 10)]}

    clf = GradientBoostingClassifier()
    grid = GridSearchCV(clf, params, cv=2, scoring="f1")
    X,y = dataset.get_X_y_data()
    grid.fit(X=X, y=y)

    print(grid.best_score_)  # 查看最佳分数(此处为f1_score)
    print(grid.best_params_)  # 查看最佳参数

    plt.show()


