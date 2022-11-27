import numpy as np
import pandas as pd
import lightgbm as lgb
from sklearn.metrics import r2_score, accuracy_score

class LGBModel:
    def __init__(self, regression = True):
        self.regression = regression
    def fit(self, dataset):
        X_train, X_valid, y_train, y_valid = dataset.split()

        dtrain = lgb.Dataset(X_train, label=y_train)
        dvalid = lgb.Dataset(X_valid, label=y_valid)

        #params = {"objective": 'mse', "verbosity": -1}
        # 参数
        params_regression = {
            'learning_rate': 0.1,
            'metrics':{'auc','mse'},
            'lambda_l1': 0.1,
            'lambda_l2': 0.2,
            'max_depth': 4,
            'objective': 'mse'#'mse',  # 目标函数
        }

        params = {'num_leaves': 90,
                  'min_data_in_leaf': 30,
                  'objective': 'multiclass',
                  'num_class': 10,
                  'max_depth': -1,
                  'learning_rate': 0.03,
                  "min_sum_hessian_in_leaf": 6,
                  "boosting": "gbdt",
                  "feature_fraction": 0.9,
                  "bagging_freq": 1,
                  "bagging_fraction": 0.8,
                  "bagging_seed": 11,
                  "lambda_l1": 0.1,
                  "verbosity": -1,
                  "nthread": 15,
                  'metric': {'multi_logloss'},
                  "random_state": 2022,
                  #'device': 'gpu'
                  }

        if self.regression:
            params = params_regression
        self.model = lgb.train(
            params,
            dtrain,
            num_boost_round=1000,
            valid_sets=[dtrain, dvalid],
            valid_names=["train", "valid"],
            early_stopping_rounds=50,
            verbose_eval=True,
            # evals_result=evals_result,
            #**kwargs
        )
        y_pred = self.model.predict(X_valid)
        if not self.regression:
            y_pred = np.argmax(y_pred, axis=1)
            print('accuracy:',accuracy_score(y_pred, y_valid))

            y_pred_train = np.argmax(self.model.predict(X_train), axis=1)
            print('accuracy_train:',accuracy_score(y_pred_train, y_train))
        else:
            print('R2系数：', r2_score(y_valid, y_pred))
            print('训练集——R2系数：', r2_score(y_train, self.model.predict(X_train)))

    def predict(self, dataset):
        if self.model is None:
            raise ValueError("model is not fitted yet!")
        x_test,_ = dataset.get_data(date_range=['20160101', '20211231'])
        pred = self.model.predict(x_test)
        print(pred)
        if not self.regression:
            return pd.Series(np.argmax(pred, axis=1), index=x_test.index)
        else:
            return pd.Series(pred, index=x_test.index)


if __name__ == '__main__':
    from bak.data.dataset import Dataset
    from engine.data.datahandler import DataHandler

    fields = ['Return($close,5)', 'Return($close,20)', 'Ref($close,126)/$close -1','$close','$open','$high','$low','$volume','$amount']
    names = ['return_5', 'return_20', 'return_126','close','open','high','low','volume','amount']

    #fields += ['Ref($close,-5)/$close -1']
    #names += ['return_-5']

    #ds = Dataset(codes=, fields=fields, feature_names=names,
    #             label_expr='QCut(Ref($close,-20)/$close -1,10)')
    #print(ds.df)
    codes = ['512690.SH', '512170.SH', '512660.SH','159928.SZ','512010.SH']
    codes = ['159915.SZ','510300.SH','512690.SH', '512170.SH', '512660.SH','159928.SZ','512010.SH']
    codes = ['159928.SZ','510050.SH','512010.SH','513100.SH','518880.SH','511220.SH','511010.SH','161716.SZ']
    codes = [
        '000300.SH',
        '000905.SH',
        '399006.SZ', #创业板
        '000852.SH', #中证1000
        '399324.SZ', #深证红利
        #'000922.SH', #中证红利
        '399997.SZ', #中证白酒
        '399396.SZ', #食品饮料

        '000013.SH',#上证企债
        '000016.SH' #上证50
    ]
    ds = Dataset(codes=codes, handler=DataHandler())
    print(ds.df)

    m = LGBModel()
    m.fit(ds)
    pred = m.predict(ds)
    print(pred)