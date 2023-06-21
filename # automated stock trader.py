# automated stock trader 
# idk how well this will work

import pandas as pd
import numpy as np
import robin_stocks.robinhood as rh
import os
import time 
import datetime 


password = os.environ.get('robinhood_password') # get password from global environment
username = os.environ.get('robinhood_username')
rh.login(username = str(username), password = str(password), expiresIn = 86400)

def moving_average(ticker, timeframe ,window):
    hist_data = pd.DataFrame(rh.stocks.get_stock_historicals(ticker, span=timeframe))
    hist_data['close_price'] = hist_data['close_price'].astype(float)
    return hist_data['close_price'].rolling(window = window).mean()

sp500 = rh.stocks.get_top_movers('up', info = 'symbol', span = 'day')

def get_current_portfolio():
    # get value of my portfolio (there's like one stock in there)
    portfolio = rh.build_holdings()
    total = sum(float(stock['equity']) for stock in portfolio)
    return total 

def trade(ticker, trade_size, price):
    # function that checks if the short term moving avg > long term moving avg before buying
    short_moving_avg = moving_average(ticker, 'day', 50)
    long_moving_avg = moving_average(ticker, 'day', 200)
    closing_price = rh.stocks.get_stock_quote_by_symbol(company)['last_trade_price'].astype(float)
    num_shares = float(trade_size / price)

    if short_moving_avg.iloc[-1] > long_moving_avg.iloc[-1] and current_price > closing_price:
        rh.orders.order_buy_market(company, num_shares)
        print('bought')
    elif short_moving_avg.iloc[-1] < long_moving_avg.iloc[-1] and current_price < closing_price:
        rh.orders.order_sell_market(company, num_shares)
        print('not')

    time.sleep(3)

def backtest_trader(start_date, end_date):
    # implement backtest trading to check how well our trading strat would've done in the past
    portfolio_value = get_current_portfolio()
    trade_size = portfolio_value * 0.01

    for company in sp500: # get moving averages for companies in sp500
        past_prices = pd.DataFrame(rh.stocks.get_stock_historicals(company, span = 'year', interval = 'day'))
        past_prices['close_price'] = past_prices['close_price'].astype(float)

        filter = (past_prices['begins_at'] >= start_date) & (past_prices['begins_at'] <= end_date)
        backtest_data = past_prices.loc[filter]

        for index, row in backtest_data.iterrows():
            current_price = row['close_price']
            trade(symbol, trade_size, current_price)

        time.sleep(3)


if '__name__' == '__main__':
    # runneth thine pockets wench; this might make me poor
    start_date = '2022-01-01'
    end_date = '2023-06-01'

    backtest_trader(start_date, end_date)