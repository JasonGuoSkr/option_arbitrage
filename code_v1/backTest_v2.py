import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


"""
套利回测
"""


def strategy(data, mean_par, std_par, open_par=2, close_par=0, stop_par=3):
    """
    :param data:
    :param mean_par:
    :param std_par:
    :param open_par:
    :param close_par:
    :param stop_par:
    :return:
    """
    future_short_price = data['future_bid']
    future_long_price = data['future_ask']
    option_short_price = (data['call_ask'] - data['put_bid']) * 1000
    option_long_price = (data['call_bid'] - data['put_ask']) * 1000
    # option_short_price = (data['call_ask'] - data['put_bid'] + data['k_discount']) * 1000
    # option_long_price = (data['call_bid'] - data['put_ask'] + data['k_discount']) * 1000
    last_spread = data['last_spread']

    m_spread = last_spread - mean_par
    sigma = std_par
    open_threshold = open_par * sigma
    close_threshold = close_par * sigma
    stop_threshold = stop_par * sigma

    profit_list = []
    open_list = []
    close_list = []
    state_list = []
    hold_signal = False
    hold_price_future = 0
    hold_price_option = 0
    hold_state = 0  # 1 (future:long option:short); -1 (future:short option:long)
    profit_sum = 0

    for i in range(2, len(data) - 1):
        if not hold_signal:
            if m_spread[i - 2] < open_threshold < m_spread[i - 1]:
                hold_price_future = future_short_price[i]
                hold_price_option = option_short_price[i]
                hold_state = -1
                hold_signal = True
                open_list.append(future_short_price.index[i])
                state_list.append(hold_state)
            elif m_spread[i - 1] < -open_threshold < m_spread[i - 2]:
                hold_price_future = future_long_price[i]
                hold_price_option = option_long_price[i]
                hold_state = 1
                hold_signal = True
                open_list.append(future_short_price.index[i])
                state_list.append(hold_state)
        else:
            if (m_spread[i - 1] >= stop_threshold or m_spread[i - 1] <= close_threshold) and hold_state == -1:
                profit = (hold_price_future - future_long_price[i]) + (option_long_price[i] - hold_price_option)
                profit_sum += profit * 300
                hold_state = 0
                hold_signal = False
                close_list.append(future_short_price.index[i])
            if (m_spread[i - 1] <= -stop_threshold or m_spread[i - 1] >= -close_threshold) and hold_state == 1:
                profit = (future_long_price[i] - hold_price_future) + (hold_price_option - option_long_price[i])
                profit_sum += profit * 300
                hold_state = 0
                hold_signal = False
                close_list.append(future_short_price.index[i])
        profit_list.append(profit_sum)

    print(profit_list)

    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # ax.plot(range(len(profit_list)), profit_list)
    # plt.show()


if __name__ == '__main__':
    pass
    # for i in range(1, 5):
    #     print(i)
