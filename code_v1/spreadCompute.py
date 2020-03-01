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
    :param contract_id:合约代码
    :param start_date:开始日期
    :param end_date:结束日期
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
    date_ind = data.index[0]
    return data.between_time(date_ind + '13:00:00.000000', date_ind + '11:30:00.000000')


def daily_compute(trade_date, underlying_spot, underlying_symbol, strike_price, maturity_month):
    """
    :param trade_date: 交易日期
    :param underlying_spot: 标的代码
    :param underlying_symbol: 期货代号IH/IF/IC
    :param strike_price: 期权执行价
    :param maturity_month: 期权到期月
    :return:
    """
    # 数据加载 期权/期货
    call_option_code = rq.options.get_contracts(underlying_spot, option_type='C', maturity=maturity_month,
                                                strike=strike_price, trading_date=trade_date)
    put_option_code = rq.options.get_contracts(underlying_spot, option_type='P', maturity=maturity_month,
                                               strike=strike_price, trading_date=trade_date)
    future_code = rq.futures.get_dominant(underlying_symbol, start_date=trade_date, end_date=trade_date, rule=0)

    call_option_data = get_tick(call_option_code, trade_date, trade_date)
    put_option_data = get_tick(put_option_code, trade_date, trade_date)
    future_data = get_tick(future_code, trade_date, trade_date)

    # 数据聚合
    filter_call_option_data = data_resample(call_option_data)
    filter_put_option_data = data_resample(put_option_data)
    filter_future_data = data_resample(future_data)

    filter_data = pd.concat([filter_call_option_data, filter_put_option_data, filter_future_data], axis=1)

    # 到期时间
    option_day_delta = rq.instruments(call_option_code).days_to_expire(date=trade_date)
    future_day_delta = rq.instruments(future_code).days_to_expire(date=trade_date)

    pass

    # 价差计算
    # c+ke-rt = p+f


if __name__ == '__main__':
    rq.init()

    # 参数
    tradeDate = '20200107'
    # startDate = '20200107'
    # endDate = '20200110'

    # underlyingIndexCode = '000300.XSHG'
    # underlyingSpotCode = '510300.XSHG'
    # underlyingSymbol = 'IF'
    # # futureCode = 'IF2001'
    # strikePrice = 4.000
    # maturityMonth = '2001'
    #
    # # 数据加载 期权/期货
    # callOptionCode = rq.options.get_contracts(underlyingSpotCode, option_type='C', maturity=maturityMonth,
    #                                           strike=strikePrice, trading_date=tradeDate)
    # putOptionCode = rq.options.get_contracts(underlyingSpotCode, option_type='P', maturity=maturityMonth,
    #                                          strike=strikePrice, trading_date=tradeDate)
    # futureCode = rq.futures.get_dominant(underlyingSymbol, start_date=tradeDate, end_date=tradeDate, rule=0)
    #
    # callOptionData = get_tick(callOptionCode, tradeDate, tradeDate)
    # putOptionData = get_tick(putOptionCode, tradeDate, tradeDate)
    # futureData = get_tick(futureCode, tradeDate, tradeDate)
    #
    # # 数据聚合
    # filterCallOptionData = data_resample(callOptionData)
    # filterPutOptionData = data_resample(putOptionData)
    # filterFutureData = data_resample(futureData)
    #
    # filterData = pd.concat([filterCallOptionData, filterPutOptionData, filterFutureData], axis=1)
    #
    # # 到期时间
    # optionDayDelta = rq.instruments(callOptionCode).days_to_expire(date=tradeDate)
    # futureDayDelta = rq.instruments(futureCode).days_to_expire(date=tradeDate)
    #
    # pass
    #
    # # 价差计算
    # # c+ke-rt = p+f
