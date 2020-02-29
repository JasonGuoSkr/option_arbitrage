import os
import pandas as pd
import datetime
import rqdatac as rq


"""
期权期货价差计算
"""


def get_tick(contract_id, start_date, end_date):
    """
    tick数据下载
    :param contract_id:
    :param start_date:
    :param end_date:
    :return:
    """
    df_tick = rq.get_price(contract_id, start_date=start_date, end_date=end_date, frequency='tick', fields=None)

    list_str_stamp = df_tick.index.strftime("%Y-%m-%d %H:%M:%S.%f")
    list_stamp = [ind[11:] for ind in list_str_stamp]
    list_stamp_bool = ['09:30:00.000000' <= ind <= '15:00:01.000000' for ind in list_stamp]

    return df_tick.loc[list_stamp_bool]


def data_resample(data, freq='500ms'):
    """
    :param data: 原数据
    :param freq: 频率
    :return:
    """
    data = data.resample(freq).ffill()

    return data


if __name__ == '__main__':
    rq.init()

    # 参数
    startDate = '20200107'
    endDate = '20200110'

    underlyingIndexCode = '000300.XSHG'
    underlyingSpotCode = '510300.XSHG'
    underlyingSymbol = 'IF'
    # futureCode = 'IF2001'
    strikePrice = 4.000
    maturityMonth = '2001'

    # 数据加载 期权/期货
    callOptionCode = rq.options.get_contracts(underlyingSpotCode, option_type='C', maturity=maturityMonth,
                                              strike=strikePrice, trading_date=endDate)
    putOptionCode = rq.options.get_contracts(underlyingSpotCode, option_type='P', maturity=maturityMonth,
                                             strike=strikePrice, trading_date=endDate)
    futureCode = rq.futures.get_dominant(underlyingSymbol, start_date=endDate, end_date=endDate, rule=0)

    callOptionData = get_tick(callOptionCode, startDate, endDate)
    putOptionData = get_tick(putOptionCode, startDate, endDate)
    futureData = get_tick(futureCode, startDate, endDate)

    # 数据聚合


    pass

