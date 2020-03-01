import os
import datetime
import rqdatac as rq


"""
期权tick数据下载，每日更新所有期权数据，每个合约一个文件
"""


def option_data_load(data_dir, *args, start_date, end_date):
    """
    期权数据下载
    :param data_dir: 数据路径
    :param args: 期权标的list
    :param start_date: 开始日期
    :param end_date: 结束日期
    :return:
    """
    if args:
        date_list = rq.get_trading_dates(start_date=start_date, end_date=end_date)
        for underlying in args:
            for date_ind in date_list:
                date_ind = date_ind.strftime('%Y%m%d')
                contract_list = rq.options.get_contracts(underlying, trading_date=date_ind)
                for contract_id in contract_list:
                    try:
                        contract_data = get_tick(contract_id, date_ind, date_ind)
                    except AttributeError:
                        print(contract_id)
                    else:
                        contract_data.to_csv(data_dir + contract_id + '_' + date_ind + '.csv')


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


if __name__ == '__main__':
    rq.init("ricequant", "8ricequant8", ('10.29.135.119', 16010))

    dataDir = "E:/中泰证券/策略/期权套利/期权tick数据/"
    if not os.path.exists(dataDir):
        os.makedirs(dataDir)

    # trade_date = datetime.datetime.now().strftime('%Y%m%d')
    startDate = '20200203'
    endDate = '20200207'

    # underlyingList = ['510050.XSHG', '510300.XSHG', '159919.XSHE']
    underlyingList = ['510300.XSHG']

    option_data_load(dataDir, *underlyingList, start_date=startDate, end_date=endDate)
