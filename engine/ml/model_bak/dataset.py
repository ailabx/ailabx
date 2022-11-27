# coding: utf-8
import numpy as np
import pandas as pd

from engine.datafeed.expr.expr_mgr import ExprMgr


def make_dataset(time_lags=5):
    expr = ExprMgr()

    df = pd.DataFrame()

    fields = []
    names = []
    fields += ["Corr($close/Ref($close,1), Log($volume/Ref($volume, 1)+1), 30)"]
    names += ["CORR30"]
    fields += ["Corr($close/Ref($close,1), Log($volume/Ref($volume, 1)+1), 60)"]
    names += ["CORR60"]

    fields += ["Std($close, 30)/$close"]
    names += ["STD30"]
    fields += ["Corr($close, Log($volume+1), 5)"]
    names += ["CORR5"]

    # fields += ["Resi($close, 10)/$close"]
    # names += ["RESI10"]
    # fields += ["Resi($close, 5)/$close"]
    # names += ["RESI5"]

    fields += ["Std($close, 5)/$close"]
    names += ["STD5"]
    fields += ["Std($close, 20)/$close"]
    names += ["STD20"]
    fields += ["Std($close, 60)/$close"]
    names += ["STD60"]

    fields += ["Ref($low, 0)/$close"]
    names += ["LOW0"]

    fields += [
        "Std(Abs($close/Ref($close, 1)-1)*$volume, 30)/(Mean(Abs($close/Ref($close, 1)-1)*$volume, 30)+1e-12)"
    ]
    names += ['WVMA30']

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

    for name, field in zip(names, fields):
        exp = expr.get_expression(field)
        se = exp.load(code)
        df[name] = se

    df['r'] = df['close'].pct_change()
    df['label'] = np.where(df['close'].pct_change(-1) > 0, 1, 0)#np.sign(df['close'].pct_change(-1))
    # df_lag["volume_Direction"] = np.sign(df_lag["volume_Lag%s_Change" % str(time_lags)])
    print(names)
    return df.dropna(how='any')







    code = 'SPX'
    time_lags = 5
    #df = feed.get_one_df_by_codes(codes)
    #df.index = pd.to_datetime(df.index)
    df_dataset = make_dataset(time_lags=time_lags)

    print(df_dataset)
    X_train, X_test, Y_train, Y_test = split_dataset(df_dataset,
                                                     ['CORR30', 'CORR60', 'STD30', 'CORR5', 'STD5', 'STD20', 'STD60',
                                                      'LOW0', 'WVMA30', 'ROC5', 'KSFT', 'RSV5', 'KLEN'],
                                                     "label", 0.85)
    #print(X_train.shape[1])
    #print(X_test)

    def norm(raw):
        mu, std = raw.mean(), raw.std()
        data_ = (raw - mu) / std
        return data_

    train_ = norm(X_train)
    test_ = norm(X_test)

    from engine.ml.model.keras_dnn import create_model, set_seeds

    set_seeds()
    model = create_model(2, 64, input_dim= X_train.shape[1])
    model.fit(train_, Y_train,
              epochs=20, verbose=False,
              validation_split=0.2, shuffle=False)

    print(model.evaluate(train_, Y_train))
    print(model.evaluate(test_, Y_test))

    from engine.ml.model.models import do_svm, do_random_forest, do_logistic_regression, test_predictor

    lr_classifier = do_logistic_regression(train_, Y_train)
    lr_hit_ratio, lr_score = test_predictor(lr_classifier, train_, Y_train)

    rf_classifier = do_random_forest(train_, Y_train)
    rf_hit_ratio, rf_score = test_predictor(rf_classifier, test_, Y_test)

    svm_classifier = do_svm(train_, Y_train)
    svm_hit_ratio, svm_score = test_predictor(rf_classifier, test_, Y_test)

    print("%s : Hit Ratio - Logistic Regreesion=%0.2f, RandomForest=%0.2f, SVM=%0.2f" % (
        'name', lr_hit_ratio, rf_hit_ratio, svm_hit_ratio))


    def backtest(data, data_norm):
        data['pos'] = np.where(model.predict(data_norm) > 0.5, 1, 0)
        data['pos'] = np.where(data['pos'] == 1, 1, -1)
        data['收益率_对数'] = data['pos'] * data['r']
        data['收益率'] = data['pos'] * data['r_']
        # data_bkt['收益率'] = data_bkt['pos'] * data_bkt['r_']
        data['equity_基准'] = data['r'].cumsum().apply(np.exp)
        # data_bkt['equity_策略'] = (data_bkt['收益率']+1).cumprod()
        data['equity_策略_对数'] = data['收益率_对数'].cumsum().apply(np.exp)
        data['equity_策略'] = (data['收益率'] + 1).cumprod()
        data[['equity_基准', 'equity_策略_对数', 'equity_策略']].plot(figsize=(10, 6))


    backtest(X_train, train_)
