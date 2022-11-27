# coding:utf8
from loguru import logger

from engine.datafeed.dataset import Dataset


class Model:
    pass


class SklearnModel(Model):
    def __init__(self, clf):
        self.clf = clf

    def fit(self, dataset: Dataset):
        X_train, y_train = dataset.get_train_data()
        self.clf.fit(X_train, y_train)
        score_train = self.clf.score(X_train, y_train)

        X_test, y_test = dataset.get_test_data()
        score_test = self.clf.score(X_test, y_test)
        logger.info('模型在训练集得分：{}，测试集上得分：{}'.format(score_train, score_test))

    def predict(self, dataset: Dataset):
        X, _ = dataset.get_X_y_data()
        y_pred = self.clf.predict(X)
        return y_pred


if __name__ == '__main__':
    names = []
    fields = []
    feature_names = []

    fields += ['BBands($close)']
    names += ['BBands']
    feature_names += ['BBands_up', 'BBands_down']

    fields += ["RSRS($high,$low,18)"]
    names += ['RSRS']
    feature_names += ['RSRS_beta']

    fields += ['Norm($RSRS_beta,600)']
    names += ['Norm_beta']
    feature_names += ['Norm_beta']

    fields += ['OBV($close,$volume)']
    names += ['obv']
    feature_names += ['obv']

    fields += ['Slope($close,20)']
    names += ['mom_slope']
    feature_names += ['mom_slope']

    fields += ['KF($mom_slope)']
    names += ['kf_mom_slope']
    feature_names += ['kf_mom_slope']

    fields += ["Ref($close,-1)/$close - 1"]
    names += ['label']

    from engine.datafeed.dataloader import Dataloader

    loader = Dataloader()
    loader.load_one_df(['000300.SH', 'SPX'], names, fields)

    ds = Dataset(dataloader=loader, feature_names=feature_names, split_date='2020-01-01')
    X, y = ds.get_test_data()
    print(X, y)

    from sklearn.ensemble import RandomForestRegressor

    model = SklearnModel(RandomForestRegressor())
    model.fit(ds)
