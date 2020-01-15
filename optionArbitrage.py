import os
import pandas as pd
import datetime
import rqdatac as rq


"""
期权套利策略
"""


def data_upload(data_dir, *args, start_date, end_date):
    """
    数据载入
    :param data_dir:
    :param args:
    :param start_date:
    :param end_date:
    :return:
    """
    if args:
        data_dict = {}
        date_list = rq.get_trading_dates(start_date=start_date, end_date=end_date)
        for contract_id in args:
            data_union = pd.DataFrame()
            for date_ind in date_list:
                date_ind = date_ind.strftime('%Y%m%d')
                try:
                    contract_data = pd.read_csv(data_dir + contract_id + '_' + date_ind + '.csv', index_col=0,
                                                engine='python')
                except:
                    print('数据缺失：' + contract_id)
                    break
                else:
                    data_union = pd.concat([data_union, contract_data], axis=0)
            data_dict[contract_id] = data_union

        return data_dict


def contract_combination(underlying, maturity, strike):
    pass


def data_contact(data_dict):
    pass


def data_resample(data_id, freq_id):
    list_str_stamp = data_id.index.strftime("%Y-%m-%d %H:%M:%S.%f")
    list_stamp = [ind[11:] for ind in list_str_stamp]
    list_stamp_1 = ['09:30:00.000000' <= ind <= '11:30:00.000000' for ind in list_stamp]
    list_stamp_2 = ['13:00:00.000000' <= ind <= '15:00:00.000000' for ind in list_stamp]

    data_id_1 = data_id.loc[list_stamp_1]
    data_id_2 = data_id.loc[list_stamp_2]

    if freq_id == '500ms':
        data_id_1 = data_id_1.resample(freq_id).ffill()
        data_id_2 = data_id_2.resample(freq_id).ffill()
    else:
        sum_data_id_1 = data_id_1[['a1_v', 'b1_v']]
        fill_data_id_1 = data_id_1[['a1', 'b1', 'limit_up', 'limit_down', 'volume', 'open_interest', 'last']]
        sum_data_id_2 = data_id_2[['a1_v', 'b1_v']]
        fill_data_id_2 = data_id_2[['a1', 'b1', 'limit_up', 'limit_down', 'volume', 'open_interest', 'last']]

        sum_data_id_1 = sum_data_id_1.resample(freq_id, label='left').sum()
        fill_data_id_1 = fill_data_id_1.resample(freq_id, label='left').pad()
        sum_data_id_2 = sum_data_id_2.resample(freq_id, label='left').sum()
        fill_data_id_2 = fill_data_id_2.resample(freq_id, label='left').pad()

        data_id_1 = pd.concat([sum_data_id_1, fill_data_id_1], axis=1)
        data_id_2 = pd.concat([sum_data_id_2, fill_data_id_2], axis=1)

    data_return = pd.concat([data_id_1, data_id_2], axis=0)
    return data_return.fillna(method='bfill')


def data_index(start_date, end_date, freq_id):
    """
    时间戳索引序列
    :param start_date:
    :param end_date:
    :param freq_id:
    :return:
    """
    if end_date < start_date:
        print('时间错误')
    else:
        date_list = rq.get_trading_dates(start_date=start_date, end_date=end_date)
        index_list = []
        for date_ind in date_list:
            daily_index = get_second(date_ind, freq_id)
            index_list = index_list + daily_index

        return index_list


def get_second(date_id, freq_id):
    """
    日内时间戳序列
    :param date_id:
    :param freq_id:
    :return:
    """
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


if __name__ == '__main__':
    rq.init()

    # 日期参数
    trade_date = datetime.datetime.now().strftime('%Y-%m-%d')
    # trade_date = '2019-12-20'
    startDate = '2020-01-07'
    endDate = '2020-01-10'

    # 合约参数
    underlying = '510300.XSHG'
    maturity = '2001'
    strike = 4.100

    optionDir = "E:/中泰证券/策略/期权套利/期权tick数据/"
    futureDir = "E:/中泰证券/策略/期权套利/期货tick数据/"


