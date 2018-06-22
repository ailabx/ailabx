import tushare as ts
import pandas as pd
import os


if __name__ == '__main__':
    df = ts.get_h_data('000300',index=True,start='2015-12-01')
    df.to_csv('d://devgit//ailabx//data//000300.csv')