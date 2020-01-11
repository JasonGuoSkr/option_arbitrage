import os
import datetime
import rqdatac as rq


"""
期权套利策略
"""


def data_load():
    pass


def data_contact(*args):
    pass


if __name__ == '__main__':
    # 日期参数
    trade_date = datetime.datetime.now().strftime('%Y-%m-%d')
    # trade_date = '2019-12-20'
    start_date = '2020-01-07'
    end_date = '2020-01-10'

    # 合约参数
    underlying = '510300.XSHG'
    maturity = '2001'
    strike = 4.100
