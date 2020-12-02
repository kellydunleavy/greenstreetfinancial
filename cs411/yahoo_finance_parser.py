from lxml import html
import requests


def to_float(value):
    try:
        return float(value)
    except:
        return 0


def parse(ticker):
    # Output Table
    data_table = {}
    # Setting up URL to fetch data
    url = "http://finance.yahoo.com/quote/%s?p=%s" % (ticker, ticker)
    try:
        # Fetching Data and Setting up Parser
        response = requests.get(url)
        parser = html.fromstring(response.text)
        # Obtaining the current price
        header = parser.xpath('//div[contains(@class, "D(ib) Mend(20px)")]//text()')
        data_table['Current Price'] = to_float(header[0])
        # Obtaining the value change and percent change
        changes = header[1].split(' ')
        value_change = changes[0][1:]
        percent_change = changes[1][2:-2]
        data_table['Value Change'] = to_float(value_change)
        data_table['Percent Change'] = to_float(percent_change)

        # Finding the summary table
        summary_table = parser.xpath(
            '//div[contains(@data-test,"summary-table")]//tr')

        for table_data in summary_table:
            # Going through each row and column of the summary table
            raw_table_key = table_data.xpath(
                './/td[1]//text()')
            raw_table_value = table_data.xpath(
                './/td[2]//text()')
            # Reformatting the column values to fit our needs
            table_key = ''.join(raw_table_key).strip()
            table_value = ''.join(raw_table_value).strip()
            table_value = table_value.replace(',', '')
            # Only saving the values that we want
            if table_key in ['Previous Close', 'Open', 'Volume']:
                data_table[table_key] = to_float(table_value)
            # Reformatting the bid and ask size
            elif table_key in ['Bid', 'Ask']:
                amount_size = table_value.split(' ')
                amount = to_float(amount_size[0])
                size = to_float(amount_size[2])
                data_table[table_key + ' Amount'] = amount
                data_table[table_key + ' Size'] = size
            elif table_key == "Day's Range":
                ranges = table_value.split(' ')
                low = to_float(ranges[0])
                high = to_float(ranges[2])
                data_table['Day Low'] = low
                data_table['Day High'] = high

        #Updating database
        try:
            query = r'http://sumuksr2.web.illinois.edu/greenstreetfinancial?password=c@$hM0n3y1999&type=insert&table=Stock&' \
                    r'symbol=' + ticker + '&current_price=' + str(data_table['Current Price']) + \
                    r'&value_change=' + str(data_table['Value Change']) + '&percent_change=' + str(data_table['Percent Change']) \
                    + '&previous_close=' + str(data_table['Previous Close']) + '&open=' + str(data_table['Open']) \
                    + '&volume=' + str(data_table['Volume']) + '&bid_size=' + str(data_table['Bid Size']) + \
                    '&bid_price=' + str(data_table['Bid Amount']) + '&ask_size=' + str(data_table['Ask Size']) + \
                    '&ask_price=' + str(data_table['Ask Amount']) + '&day_high=' + str(data_table['Day High']) + \
                    '&day_low=' + str(data_table['Day Low']) + '&sentiment_rating=0.5'

            r = requests.get(query)

        except Exception as E:
            return str(E)

        # Returning the data table
        return data_table

    # Incase any errors arise
    except Exception as E:
        return str(E)