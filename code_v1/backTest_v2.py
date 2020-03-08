import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


"""
套利回测
"""


def strategy(data, open_par=2, close_par=0, stop_par=3):





    future_short_price = data['future_bid']
    future_long_price = data['future_ask']
    option_short_price = (data['call_ask'] - data['put_bid'] + data['k_discount']) * 1000
    option_long_price = (data['call_bid'] - data['put_ask'] + data['k_discount']) * 1000

    last_spread = data['last_spread']
    m_spread = last_spread - np.mean(last_spread)
    sigma = np.std(m_spread)
    open_threshold = open_par * sigma
    close_threshold = close_par * sigma
    stop_threshold = stop_par * sigma

    profit_list = []
    hold_signal = False
    hold_price_future = 0
    hold_price_option = 0
    hold_state = 0  # 1 (future:long option:short); -1 (future:short option:long)
    profit_sum = 0

    for i in range(1, len(data)):
        if not hold_signal:
            if m_spread[i - 1] >= open_threshold:
                hold_price_future = future_short_price[i]
                hold_price_option = option_short_price[i]
                hold_state = -1
                hold_signal = True
            elif m_spread[i - 1] <= -open_threshold:
                hold_price_future = future_long_price[i]
                hold_price_option = option_long_price[i]
                hold_state = 1
                hold_signal = True
        else:
            if m_spread[i - 1] >= stop_threshold and hold_state == -1:
                profit = (hold_price_future - future_long_price[i]) + (option_long_price[i] - hold_price_option)
                profit_sum += profit * 300
                hold_state = 0
                hold_signal = False
            if m_spread[i - 1] <= -stop_threshold and hold_state == 1:
                profit = (future_long_price[i] - hold_price_future) + (hold_price_option - option_long_price[i])
                profit_sum += profit * 300
                hold_state = 0
                hold_signal = False
            if m_spread[i - 1] <= close_threshold and hold_state == -1:
                profit = (hold_price_future - future_long_price[i]) + (option_long_price[i] - hold_price_option)
                profit_sum += profit * 300
                hold_state = 0
                hold_signal = False
            if m_spread[i - 1] >= -close_threshold and hold_state == 1:
                profit = (future_long_price[i] - hold_price_future) + (hold_price_option - option_long_price[i])
                profit_sum += profit * 300
                hold_state = 0
                hold_signal = False
        profit_list.append(profit_sum)

    print(profit_list)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(range(len(profit_list)), profit_list)
    plt.show()


if __name__ == '__main__':
    pass
