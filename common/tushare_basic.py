# 导入tushare
import tushare as ts

# 初始化pro接口
pro = ts.pro_api('854634d420c0b6aea2907030279da881519909692cf56e6f35c4718c')


# 就是所有基金列表，类似ods直接导入，不过滤，不处理字段。
def get_fund_basics(offset=0):
    # 拉取数据
    df = pro.fund_basic(**{
        "ts_code": "",
        "market": "",
        "update_flag": "",
        "offset": "{}".format(offset),
        "limit": "",
        "status": "L"
    }, fields=[
        "ts_code",
        "name",
        "management",
        "custodian",
        "fund_type",
        "found_date",
        "due_date",
        "list_date",
        "issue_date",
        "delist_date",
        "issue_amount",
        "m_fee",
        "c_fee",
        "duration_year",
        "p_value",
        "min_amount",
        "exp_return",
        "benchmark",
        "status",
        "invest_type",
        "type",
        "trustee",
        "purc_startdate",
        "redm_startdate",
        "market"
    ])
    return df


# 场内基金列表
def get_etf_basics():
    # 导入tushare
    import tushare as ts
    # 初始化pro接口
    pro = ts.pro_api('854634d420c0b6aea2907030279da881519909692cf56e6f35c4718c')

    # 拉取数据
    df = pro.fund_basic(**{
        "ts_code": "",
        "market": "E",
        "update_flag": "",
        "offset": "",
        "limit": "",
        "status": "L",
        "name": ""
    }, fields=[
        "ts_code",
        "name",
        "management",
        "custodian",
        "fund_type",
        "found_date",
        "due_date",
        "list_date",
        "issue_date",
        "delist_date",
        "issue_amount",
        "m_fee",
        "c_fee",
        "duration_year",
        "p_value",
        "min_amount",
        "exp_return",
        "benchmark",
        "status",
        "invest_type",
        "type",
        "trustee",
        "purc_startdate",
        "redm_startdate",
        "market"
    ])
    return df


# 可转债列表
def get_cb_basics():
    # 导入tushare
    import tushare as ts
    # 初始化pro接口
    pro = ts.pro_api('854634d420c0b6aea2907030279da881519909692cf56e6f35c4718c')

    # 拉取数据
    df = pro.cb_basic(**{
        "ts_code": "",
        "list_date": "",
        "exchange": "",
        "limit": "",
        "offset": ""
    }, fields=[
        "ts_code",
        "bond_full_name",
        "bond_short_name",
        "cb_code",
        "stk_code",
        "stk_short_name",
        "maturity",
        "par",
        "issue_price",
        "issue_size",
        "remain_size",
        "value_date",
        "maturity_date",
        "rate_type",
        "coupon_rate",
        "add_rate",
        "pay_per_year",
        "list_date",
        "delist_date",
        "exchange",
        "conv_start_date",
        "conv_end_date",
        "first_conv_price",
        "conv_price",
        "rate_clause",
        "put_clause",
        "maturity_put_price",
        "call_clause",
        "reset_clause",
        "conv_clause",
        "guarantor",
        "guarantee_type",
        "issue_rating",
        "newest_rating",
        "rating_comp"
    ])
    return df

if __name__ == '__main__':
    #df = get_fund_basics()
    df = get_etf_basics()
    df['_id'] = df['ts_code']
    from common.mongo_utils import write_df
    write_df('basic_etfs', df, drop_tb_if_exist=True)

    #df = df[~df['name'].str.contains("C|定开|持有|D|I|联接E|定期开放|短债|H|个月")]
    #df = df[~df['fund_type'].str.contains('货币')]
    #print(df)
    #df.to_csv('all.csv')
