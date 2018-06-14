import tushare as ts
import pandas as pd
import os



if __name__ == '__main__':
    df = ts.get_h_data('000001',index=True,start='2008-01-01')
    df.to_csv('d://devgit//ailabx//data//000001_index.csv')