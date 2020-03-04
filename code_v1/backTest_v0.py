
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def strategy(spread):
    df = pd.read_csv('./data.csv')
    price_A = df['rb1907'].values
    price_B = df['rb1908'].values

    spread = price_A - price_B
    mspread = spread - np.mean(spread)
    sigma = np.std(mspread)
    open = 2 * sigma
    stop = 3 * sigma
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

