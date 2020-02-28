
"""
期权合约信息下载
期权标的：510050.SH/510300.SH/159919.SZ/000300.SH
"""

import os
import datetime
import pandas as pd
import rqdatac as rq

rq.init()


# 日期参数
trade_date = datetime.datetime.now().strftime('%Y-%m-%d')
# trade_date = '2019-12-20'

# 文件路径
outputPath = "E:/中泰证券/交易/期权波动率/合约信息/"
if not os.path.exists(outputPath):
    os.makedirs(outputPath)
    print(outputPath + '创建成功')

# 合约板块
plate_dict = {'510050.SH': ['1000018861000000', '1000018862000000'],
              '510300.SH': ['1000021611000000', '1000021612000000'],
              '159919.SZ': ['1000034605000000', '1000034606000000'],
              '000300.SH': ['1000034523000000', '1000034524000000']}

contract_df = rq.options.get_contracts('510300.XSHG', option_type=None, maturity='2001', strike=None, trading_date=None)


# for ind in plate_dict.keys():
#     # ind = '510050.SH'
#     call_windData = w.wset("sectorconstituent", "date=" + trade_date + ";sectorid=" + plate_dict[ind][0])
#     put_windData = w.wset("sectorconstituent", "date=" + trade_date + ";sectorid=" + plate_dict[ind][1])
#
#     call_list = call_windData.Data
#     call_df = pd.DataFrame({'call_code': call_list[1], 'call_name': call_list[2]})
#     put_list = put_windData.Data
#     put_df = pd.DataFrame({'put_code': put_list[1], 'put_name': put_list[2]})
#
#     contract_df = pd.concat([call_df, put_df], axis=1)
#
#     contract_df.to_excel(outputPath + ind + '_' + trade_date + "_合约列表.xlsx", encoding='utf-8')
