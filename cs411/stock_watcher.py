import yahoo_finance_parser
from datetime import datetime
import sys
import time
from time import ctime


def price_dip(open_price, current_price):
    """
    The purpose of this function is to check whether the price dip is in action
    :param open_price: the open price of the stock
    :param current_price: the current price of the stock
    :return: boolean whether stock is experiencing a dip
    """
    percent_drop = (open_price - current_price) / open_price
    if percent_drop >= .3:
        return True
    else:
        return False


def volume_surge(volumes):
    """
    The purpose of this function is to check whether there is a surge in volume
    :param volumes: list with minimum size 3 of consecutive volumes
    :return: boolean whether stock experienced a surge in volume
    """
    # Breaking if not enough volumes
    if len(volumes) < 3:
        return False
    if volumes[-3] == 0 or volumes[-1] == 0:
        return False
    # Calculating percentage increase of volume
    surge = volumes[-2] - volumes[-3] / volumes[-3]
    # Calculating if the surge is over
    base = abs(volumes[-3] - volumes[-1] / volumes[-1])
    # If there is more than 100% surge then return True
    if surge > 1 and base < 0.2:
        return True
    else:
        return False


def higher_bid(bid_price, ask_price):
    """
    The purpose of this function is to check whether bid price is higher than ask price
    :param bid_price: the bid price
    :param ask_price: the float price
    :return: boolean whether the bid price is greater than ask price
    """
    if bid_price > ask_price:
        return True
    else:
        return False


def buy(ticker, stock_data):
    """
    The purpose of this function is to start the buy/sell procedure once pattern matches
    :param ticker: the stock symbol
    :param stock_data: the data of stock price and volume
    :return: None
    """
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    f = open(ticker + ".txt", "a")
    f.write(ticker + ': $' + str(stock_data['Current Price']) + " at " + str(current_time))
    f.close()
    print(ticker + ': $' + str(stock_data['Current Price']) + " at " + str(current_time))


def stock_watcher(ticker):
    """
    The purpose of this function is to continuously watch the stock to check for dip buy conditions
    :param ticker: the stock symbol
    :return: None
    """
    print('Watching: ' + ticker)
    # List of historic volumes
    volumes = [0]
    volume_changes = [0]
    # Loop to continuously check
    while True:
        # Obtaining live stock data
        stock_data = yahoo_finance_parser.parse(ticker)
        print(stock_data)

        # If error fetching values then exist
        if stock_data == -1:
            return -1
        # Keeping volumes list small to save memory
        if len(volumes) >= 5:
            volumes.pop(0)
        if len(volume_changes) >= 5:
            volume_changes.pop(0)
        try:
            # Saving the historic volume
            volume_changes.append(float(stock_data['Volume']) - float(volumes[-1]))
            volumes.append(float(stock_data['Volume']))
            # Checking for dip buy conditions
            dip = price_dip(stock_data['Open'], stock_data['Current Price'])
            surge = volume_surge(volume_changes)
            h_bid = higher_bid(stock_data['Bid Amount'], stock_data['Ask Amount'])
            # Logging Purposes
            if dip or surge or h_bid:
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                f = open(ticker + ".txt", "a")
                f.write(ticker + ': ' + str(dip) + ', ' + str(surge) + ', ' + str(h_bid) + " at " + str(current_time))
                f.close()

            # Triggering buy if all conditions work
            if dip and surge and h_bid:
                buy(ticker, stock_data)
        except:
            print('ERROR')
            stock_watcher(ticker)


if __name__ == "__main__":
    stock_watcher(sys.argv[1])
