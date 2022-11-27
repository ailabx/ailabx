# coding:utf8
import numpy as np
import datetime as dt
from engine.datafeed.dataloader import Dataloader
from loguru import logger


class OneStepTimeSeriesSplit:
    """Generates tuples of train_idx, test_idx pairs
    Assumes the index contains a level labeled 'date'"""

    def __init__(self, n_splits=3, test_period_length=1, shuffle=False):
        self.n_splits = n_splits
        self.test_period_length = test_period_length
        self.shuffle = shuffle

    @staticmethod
    def chunks(l, n):
        for i in range(0, len(l), n):
            print(l[i:i + n])
            yield l[i:i + n]

    def split(self, X, y=None, groups=None):
        unique_dates = (X.index
                        # .get_level_values('date')
                        .unique()
                        .sort_values(ascending=False)
        [:self.n_splits * self.test_period_length])

        dates = X.reset_index()[['date']]
        for test_date in self.chunks(unique_dates, self.test_period_length):
            train_idx = dates[dates.date < min(test_date)].index
            test_idx = dates[dates.date.isin(test_date)].index
            if self.shuffle:
                np.random.shuffle(list(train_idx))
            yield train_idx, test_idx

    def get_n_splits(self, X, y, groups=None):
        return self.n_splits


def get_date_by_percent(start_date, end_date, percent):
    days = (end_date - start_date).days
    target_days = np.trunc(days * percent)
    target_date = start_date + dt.timedelta(days=target_days)
    # print days, target_days,target_date
    return target_date


def split_df(df, x_cols, y_col, split_date=None, split_ratio=0.8):
    if not split_date:
        split_date = get_date_by_percent(df.index[0], df.index[df.shape[0] - 1], split_ratio)

    input_data = df[x_cols]
    output_data = df[y_col]

    # Create training and test sets
    X_train = input_data[input_data.index < split_date]
    X_test = input_data[input_data.index >= split_date]
    Y_train = output_data[output_data.index < split_date]
    Y_test = output_data[output_data.index >= split_date]

    return X_train, X_test, Y_train, Y_test


class Dataset:
    def __init__(self, dataloader, split_date, feature_names, label_name='label'):
        self.split_date = split_date
        self.feature_names = feature_names
        self.label_name = label_name

        self.loader = dataloader
        if dataloader.data is None:
            logger.error('dataloader未加载数据。')
        self.df = dataloader.data

    def get_split_dataset(self):
        X_train, X_test, Y_train, Y_test = split_df(self.df, x_cols=self.feature_names, y_col=self.label_name,
                                                    split_date=self.split_date)
        return X_train, X_test, Y_train, Y_test

    def get_train_data(self):
        X_train, X_test, Y_train, Y_test = split_df(self.df, x_cols=self.feature_names, y_col=self.label_name,
                                                    split_date=self.split_date)
        return X_train, Y_train

    def get_test_data(self):
        X_train, X_test, Y_train, Y_test = split_df(self.df, x_cols=self.feature_names, y_col=self.label_name,
                                                    split_date=self.split_date)
        return X_test, Y_test

    def get_X_y_data(self):
        X = self.df[self.feature_names]
        y = self.df[self.label_name]
        return X, y


if __name__ == '__main__':
    codes = ['000300.SH', 'SPX']
    names = []
    fields = []
    fields += ["Corr($close/Ref($close,1), Log($volume/Ref($volume, 1)+1), 30)"]
    names += ["CORR30"]

    dataset = Dataset(codes, names, fields, split_date='2020-01-01')
    X_train, Y_train = dataset.get_train_data()
    print(X_train, Y_train)
