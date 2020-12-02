from lxml import html
import requests
from datetime import datetime
from pytz import timezone


def get_dip_rip_watchlist():
    # 30% Movers URL
    #url = r"https://finance.yahoo.com/screener/unsaved/53f39fb4-30fb-4bb7-9247-5fe7ce099a2d"
    # 50% Movers URL
    url = r"https://finance.yahoo.com/screener/unsaved/f9878baf-2df8-4caa-b71c-14e2d2252109"

    # Parsing Results
    response = requests.get(url)
    parser = html.fromstring(response.text)
    # Variable to hold set of final stocks
    watch_list = set()
    # Reading table of stocks from website
    summary_table = parser.xpath('//div[contains(@id,"scr-res-table")]//tr')

    # Looping through each table row to get stock name
    for element in summary_table:
        # Converting HTML to text
        stock_data = element.xpath('.//td[1]//text()')
        # Adding stock name only if it has a value
        if len(stock_data) > 0:
            symbol = stock_data[0]
            watch_list.add(symbol)

    # Returning stock list
    return watch_list


if __name__ == '__main__':
    tz = timezone('US/Eastern')
    print(datetime.now(tz))
    print(get_dip_rip_watchlist())