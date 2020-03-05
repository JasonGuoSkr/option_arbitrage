import os
import time
import numpy as np
import pandas as pd
import datetime
import rqdatac as rq


"""
期权期货价差计算
"""


def get_tick(contract_id, start_date, end_date):
    """
    tick数据下载
    :param contract_id: 合约代码
    :param start_date: 开始日期
    :param end_date: 结束日期
    :return:
    """
    df_tick = rq.get_price(contract_id, start_date=start_date, end_date=end_date, frequency='tick', fields=None)

    # list_str_stamp = df_tick.index.strftime("%Y-%m-%d %H:%M:%S.%f")
    # list_stamp = [ind[11:] for ind in list_str_stamp]
    # list_stamp_bool = ['09:25:00.000000' <= ind <= '15:01:00.000000' for ind in list_stamp]

    return df_tick.between_time('09:25:00', '15:01:00')


def data_resample(data, freq='500ms'):
    """
    :param data: 原数据
    :param freq: 频率
    :return:
    """
    data = data.resample(freq).ffill()
    data = data.between_time('09:31:00', '14:55:00')
    return data.between_time('13:00:00', '11:30:00')
    # date_ind = data.index[0].strftime("%Y-%m-%d")
    # return data.between_time(datetime.datetime.strptime(date_ind + '13:00:00.000000', "%Y-%m-%d %H:%M:%S.%f"),
    #                          datetime.datetime.strptime(date_ind + '11:30:00.000000', "%Y-%m-%d %H:%M:%S.%f"))


def daily_compute(trade_date, underlying_spot, underlying_symbol, strike_price, maturity_month, risk_free=0.035):
    """
    :param trade_date: 交易日期
    :param underlying_spot: 标的代码
    :param underlying_symbol: 期货代号IH/IF/IC
    :param strike_price: 期权执行价
    :param maturity_month: 期权到期月
    :param risk_free: 无风险利率
    :return: spread_data 做多/做空/最新价差
    """

    # 数据加载 期权/期货
    call_option_code = rq.options.get_contracts(underlying_spot, option_type='C', maturity=maturity_month,
                                                strike=strike_price, trading_date=trade_date)[0]
    put_option_code = rq.options.get_contracts(underlying_spot, option_type='P', maturity=maturity_month,
                                               strike=strike_price, trading_date=trade_date)[0]
    future_code = rq.futures.get_dominant(underlying_symbol, start_date=trade_date, end_date=trade_date, rule=0)[0]

    call_option_data = get_tick(call_option_code, trade_date, trade_date)
    put_option_data = get_tick(put_option_code, trade_date, trade_date)
    future_data = get_tick(future_code, trade_date, trade_date)

    # 数据聚合
    call_option_data.drop_duplicates(keep='first', inplace=True)
    put_option_data.drop_duplicates(keep='first', inplace=True)
    future_data.drop_duplicates(keep='first', inplace=True)

    filter_call_option_data = data_resample(call_option_data)
    filter_put_option_data = data_resample(put_option_data)
    filter_future_data = data_resample(future_data)

    # 到期时间
    # option_day_delta = rq.instruments(call_option_code).days_to_expire(date=trade_date)
    future_day_delta = rq.instruments(future_code).days_to_expire(date=trade_date)
    inday_list = [ind / len(filter_future_data)for ind in list(range(len(filter_future_data)))]
    allday_list = [(ind + future_day_delta) / 365 for ind in inday_list]

    data_join = pd.concat([filter_call_option_data['a1'], filter_call_option_data['b1'],
                           filter_call_option_data['last'], filter_put_option_data['a1'],
                           filter_put_option_data['b1'], filter_put_option_data['last'],
                           filter_future_data['a1'], filter_future_data['b1'],
                           filter_future_data['last']], axis=1)
    data_join.columns = ['call_ask', 'call_bid', 'call_last', 'put_ask', 'put_bid', 'put_last',
                         'future_ask', 'future_bid', 'future_last']
    data_join['k_discount'] = [strike_price * np.exp(-risk_free * t) for t in allday_list]

    # 价差计算
    short_spread = data_join['future_bid'] - (data_join['call_ask'] - data_join['put_bid']
                                              + data_join['k_discount']) * 1000
    long_spread = data_join['future_ask'] - (data_join['call_bid'] - data_join['put_ask']
                                             + data_join['k_discount']) * 1000
    last_spread = data_join['future_last'] - (data_join['call_last'] - data_join['put_last']
                                              + data_join['k_discount']) * 1000

    spread_data = pd.concat([short_spread, long_spread, last_spread], axis=1)
    spread_data.columns = ['short_spread', 'long_spread', 'last_spread']

    # short_data = pd.concat([filter_call_option_data['a1'], filter_put_option_data['b1'],
    #                         filter_future_data['b1']], axis=1)
    # long_data = pd.concat([filter_call_option_data['b1'], filter_put_option_data['a1'],
    #                        filter_future_data['a1']], axis=1)
    # last_data = pd.concat([filter_call_option_data['last'], filter_put_option_data['last'],
    #                        filter_future_data['last']], axis=1)

    return pd.concat([spread_data, data_join], axis=1)


if __name__ == '__main__':
    rq.init("ricequant", "8ricequant8", ('10.29.135.119', 16010))

    # 参数
    tradeDate = '20200304'

    ID = '10002157'
    startDate = '20200304'
    endDate = '20200304'

    dfTick = rq.get_price(ID, start_date=startDate, end_date=endDate, frequency='tick', fields=None)
    dfTick = dfTick.between_time('09:25:00', '15:01:00')

    underlyingSpot = '510300.XSHG'
    underlyingSymbol = 'IF'
    strikePrice = 4.000
    maturityMonth = 2003
    riskFree = 0.035

    callOptionCode = rq.options.get_contracts(underlyingSpot, option_type='C', maturity=maturityMonth,
                                              strike=strikePrice, trading_date=tradeDate)[0]
    futureCode = rq.futures.get_dominant(underlyingSymbol, start_date=tradeDate, end_date=tradeDate, rule=0)[0]

    callOptionData = get_tick(callOptionCode, tradeDate, tradeDate)
    callOptionData.drop_duplicates(keep='first', inplace=True)
    futureData = get_tick(futureCode, tradeDate, tradeDate)
    futureData.drop_duplicates(keep='first', inplace=True)

    filterCallOptionData = data_resample(callOptionData)
    filterFutureData = data_resample(futureData)

    Data = daily_compute(tradeDate, underlyingSpot, underlyingSymbol, strikePrice, maturityMonth, risk_free=riskFree)

