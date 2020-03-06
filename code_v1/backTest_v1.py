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
    hold = False
    hold_price_A = 0
    hold_price_B = 0
    hold_state = 0  # 1 (A:long B:short)   -1 (A:short B:long)
    profit_sum = 0

    for i in range(len(price_A)):
        if hold == False:
            if mspread[i] >= open:
                hold_price_A = price_A[i]
                hold_price_B = price_B[i]
                hold_state = -1
                hold = True
            elif mspread[i] <= -open:
                hold_price_A = price_A[i]
                hold_price_B = price_B[i]
                hold_state = 1
                hold = True
        else:
            if mspread[i] >= stop and hold_state == -1:
                profit = (hold_price_A - price_A[i]) + (price_B[i] - hold_price_B)
                profit_sum += profit
                hold_state = 0
                hold = False
            if mspread[i] <= -stop and hold_state == 1:
                profit = (price_A[i] - hold_price_A) + (hold_price_B - price_B[i])
                profit_sum += profit
                hold_state = 0
                hold = False
            if mspread[i] <= 0 and hold_state == -1:
                profit = (hold_price_A - price_A[i]) + (price_B[i] - hold_price_B)
                profit_sum += profit
                hold_state = 0
                hold = False
            if mspread[i] >= 0 and hold_state == 1:
                profit = (price_A[i] - hold_price_A) + (hold_price_B - price_B[i])
                profit_sum += profit
                hold_state = 0
                hold = False
        profit_list.append(profit_sum)

    print(profit_list)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(range(len(profit_list)), profit_list)
    plt.show()

