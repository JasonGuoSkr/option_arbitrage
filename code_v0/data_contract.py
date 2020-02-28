
"""
期权、期货数据下载
"""

import os
import datetime
import pandas as pd
import rqdatac as rq

rq.init()


# 日期参数
trade_date = datetime.datetime.now().strftime('%Y-%m-%d')
# trade_date = '2019-12-20'
start_date = '2020-01-06'
end_date = '2020-01-07'


# 合约参数
underlying = '510300.XSHG'
maturity = '2001'
strike = 4.100


# 文件路径
# outputPath = "E:/中泰证券/交易/期权波动率/合约信息/"
# if not os.path.exists(outputPath):
#     os.makedirs(outputPath)
#     print(outputPath + '创建成功')


def get_tick(contract_id, start_date, end_date):
    """
    tick数据下载
    :param contract_id:
    :param start_date:
    :param end_date:
    :return:
    """
    df_tick = rq.get_price(contract_id, start_date=start_date, end_date=end_date, frequency='tick',
                           fields=['a1', 'a1_v', 'b1', 'b1_v', 'last'])
    list_str_stamp = df_tick.index.strftime("%Y-%m-%d %H:%M:%S.%f")
    list_stamp = [ind[11:] for ind in list_str_stamp]
    list_stamp_bool = ['09:30:00.000000' <= ind <= '15:00:00.000000' for ind in list_stamp]
    return df_tick.loc[list_stamp_bool]


def get_second(freq_id, start_date, end_date):
    # 交易日秒标签序列
    list_second = []
    begin_second_1 = datetime.datetime.strptime(date_id.strftime("%Y-%m-%d") + ' 09:30:00.000000',
                                                "%Y-%m-%d %H:%M:%S.%f")
    end_second_1 = datetime.datetime.strptime(date_id.strftime("%Y-%m-%d") + ' 11:30:00.000000',
                                              "%Y-%m-%d %H:%M:%S.%f")
    begin_second_2 = datetime.datetime.strptime(date_id.strftime("%Y-%m-%d") + ' 13:00:00.000000',
                                                "%Y-%m-%d %H:%M:%S.%f")
    end_second_2 = datetime.datetime.strptime(date_id.strftime("%Y-%m-%d") + ' 15:00:00.000000',
                                              "%Y-%m-%d %H:%M:%S.%f")

    while begin_second_1 <= end_second_1:
        second_str = begin_second_1.strftime("%Y-%m-%d %H:%M:%S.%f")
        list_second.append(second_str)
        begin_second_1 += datetime.timedelta(seconds=freq_id)

    while begin_second_2 <= end_second_2:
        second_str = begin_second_2.strftime("%Y-%m-%d %H:%M:%S.%f")
        list_second.append(second_str)
        begin_second_2 += datetime.timedelta(seconds=freq_id)

    return [datetime.datetime.strptime(ind, "%Y-%m-%d %H:%M:%S.%f") for ind in list_second]


# 标的对应期货合约
id_dict = {'510050.XSHG': 'IH2001', '510300.XSHG': 'IF2001', '159919.XSHE': 'IF2001', '000300.XSHG': 'IF2001'}


# 期权合约代码
contract_call = rq.options.get_contracts(underlying, option_type='C', maturity=maturity,
                                         strike=strike, trading_date=trade_date)

contract_put = rq.options.get_contracts(underlying, option_type='P', maturity=maturity,
                                        strike=strike, trading_date=trade_date)

# 数据下载
# data_call = rq.get_price(contract_call[0], start_date=start_date, end_date=end_date, frequency='tick',
#                          fields=['a1', 'a1_v', 'b1', 'b1_v', 'last'])
# data_put = rq.get_price(contract_put[0], start_date=start_date, end_date=end_date, frequency='tick',
#                         fields=['a1', 'a1_v', 'b1', 'b1_v', 'last'])
# data_future = rq.get_price(id_dict[underlying], start_date=start_date, end_date=end_date, frequency='tick',
#                            fields=['a1', 'a1_v', 'b1', 'b1_v', 'last'])
data_call = get_tick(contract_call[0], start_date, end_date)
data_put = get_tick(contract_put[0], start_date, end_date)
data_future = get_tick(id_dict[underlying], start_date, end_date)

# 数据resample
contract_id = contract_call[0]



