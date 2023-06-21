## automated stock trader on robinhood

import pandas as pd
import numpy as np
import robin_stocks.robinhood as rh
import os
import matplotlib.pyplot as plt
import time 


password = os.environ.get('robinhood_password') # get password from global environment
username = os.environ.get('robinhood_username')
rh.login(username = str(username), password = str(password), expiresIn = 86400)

def moving_average(ticker, timeframe ,window):
    # get moving average of a stock's closing price within a certain timeframe
    hist_data = pd.DataFrame(rh.stocks.get_stock_historicals(ticker, span=timeframe))
    hist_data['close_price'] = hist_data['close_price'].astype(float)
    return hist_data['close_price'].rolling(window = window).mean()

desired_stock_list = ['AAPL', 'MSFT', 'GE', 'NKE']

def get_current_portfolio():
    # get value of my portfolio 
    portfolio = rh.build_holdings()
    total = sum(float(stock['equity']) for stock in portfolio)
    return total 

def trade(ticker, trade_size, price):
    # function that checks if the short term moving avg > long term moving avg before buying
    short_moving_avg = moving_average(ticker, 'day', 50)
    long_moving_avg = moving_average(ticker, 'day', 200)
    closing_price = rh.stocks.get_stock_quote_by_symbol(ticker)['last_trade_price'].astype(float)
    num_shares = float(trade_size / price)

    if short_moving_avg.iloc[-1] > long_moving_avg.iloc[-1] and current_price > closing_price:
        rh.orders.order_buy_market(ticker, num_shares)
        print('bought')
    elif short_moving_avg.iloc[-1] < long_moving_avg.iloc[-1] and current_price < closing_price:
        rh.orders.order_sell_market(ticker, num_shares)
        print('not bought')

    time.sleep(3)

def backtest_trader(start_date, end_date):
    # implement backtest trading to check how well our trading strat would've done in the past
    portfolio_value = get_current_portfolio()
    trade_size = portfolio_value * 0.01

    fig, axes = plt.subplots(len(desired_stock_list), figsize = (10,24))

    for n, company in enumerate(desired_stock_list): # get moving averages for companies in desired stock list
        past_prices = pd.DataFrame(rh.stocks.get_stock_historicals(company, span = 'year', interval = 'day'))
        past_prices['close_price'] = past_prices['close_price'].astype(float)

        mask = (past_prices['begins_at'] >= start_date) & (past_prices['begins_at'] <= end_date)
        backtest_data = past_prices.loc[mask]

        short_moving_avg = moving_average(company, 'day', 50)
        long_moving_avg = moving_average(company, 'day', 200)

        axes[n].plot(backtest_data['begins_at'], backtest_data['close_price'], label='Stock Price')
        axes[n].plot(backtest_data['begins_at'], short_moving_avg, label='Short Moving Average')
        axes[n].plot(backtest_data['begins_at'], long_moving_avg, label='Long Moving Average')
        axes[n].set_title(company)
        axes[n].legend()

        for index, row in backtest_data.iterrows():
            current_price = row['close_price']
            trade(company, trade_size, current_price)

        time.sleep(3)
        print('working')

    plt.tight_layout()
    plt.show()



if '__name__' == '__main__':
    # do backtest trading over 18 month period to evaluate 
    start_date = '2022-01-01'
    end_date = '2023-06-01'

    backtest_trader(start_date, end_date)