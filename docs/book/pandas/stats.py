import pandas as pd

def test_1():
    df = pd.read_csv('../../../data/000300_index.csv')
    df.index =  df['date']
    df.sort_index(inplace=True)
    print(df.head())

    #计算收益率
    df['return'] = df['close']/df['close'].shift(1) - 1
    #计算涨跌
    df['up_or_down'] = df['close'] > df['close'].shift(1)

    print(df.head())
    print(df['up_or_down'].value_counts())

    print(df['return'].describe())

    import matplotlib.pyplot as plt
    #df['return'].plot()
    df['return'].hist(bins=80, alpha=0.3, color='g', normed=True)
    df['return'].plot(kind='kde', style='r',xlim=[-0.1, 0.1],grid=True)
    plt.show()

df = pd.DataFrame({'A': range(1, 6), 'B': range(10, 0, -2)})
print('raw df is:',df)
df.eval('where(A > {0}, {0}, where(label < -{0}, -{0}, label)) + {0}'.format(3),inplace=True,engine='numexpr')
print('eval:',df)