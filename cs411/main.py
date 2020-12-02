import watchlist_generator
import yahoo_finance_parser
import alpaca_trade_api as tradeapi
import requests
import math
from datetime import datetime, time

api = tradeapi.REST('PKT3RH3268XNDLHGAWN7', 'hQ5Ja7pQGHA1DYyBAFtDc2LrGsfc2PdBGnBPbJm1', 'https://paper-api.alpaca.markets', api_version='v2')
traded = set()
while True:
    watchlist = watchlist_generator.get_dip_rip_watchlist()
    #watchlist = ['EURN', 'YDUQY', 'ELKEF', 'JPS', 'DRH', 'LWEL', 'MGPPF', 'CYBQF', 'TRQ', 'SMSMY', 'MEOBF', 'HBM', 'CYBQY', 'ANZFF', 'ASTVF', 'BDJ', 'HAWPF', 'MMSMY', 'EIHDF', 'OUTKY', 'CHPRF', 'CALZF', 'PGEN', 'HCACW', 'SCGPY', 'BGCP', 'RPAI', 'VTKLY', 'PBTHF', 'THBIY', 'INFN', 'PTXKY', 'TAC', 'BRMSY', 'ENLC', 'AMRN', 'SUUIF', 'CWSRF', 'SGHIF', 'CSRLF', 'ISMAF', 'CYRBY', 'FIT', 'HCHDF', 'AAGRY', 'KNCAF', 'MIK', 'YPF', 'GAB', 'SGMO', 'ISMAY', 'NBGIF', 'WACMY', 'NNCSF', 'STBMF', 'BSM', 'FBP', 'MFGP', 'SECCF', 'TWO', 'IRPSY', 'ARGKF', 'IVBXF', 'FBBPF', 'CDE', 'MAC', 'NPKYY', 'DPUKY', 'AETUF', 'LTGHY', 'IAG', 'DSITF', 'PAEKY', 'PREKF', 'BBAJF', 'NAVI', 'SIM', 'CYDY', 'IVTJF', 'GOL', 'RRC', 'MPGPF', 'GRFFF', 'CBAOF', 'CELTF', 'MFA', 'MGY', 'VCMMF', 'MRRTY', 'NWITY', 'WEBJF', 'PGUCY', 'GEAHF', 'PAGP', 'TULLF', 'KPLUY', 'TCNGF', 'FKKFY', 'RGRNF', 'KNCAY']
    #print('Watchlist: ' + str(watchlist))
    for stock in watchlist:
        stock_info = -1
        while stock_info == - 1:
            stock_info = yahoo_finance_parser.parse(stock)
            print(stock_info)
        day_high = stock_info['Day High']
        threshold = math.ceil(round(day_high, 1) * 2.0) / 2.0
        now = datetime.now()
        now_time = now.time()
        if stock not in traded and now_time >= time(9,30) and now_time <= time(16,00):
            try:
                query = 'http://sumuksr2.web.illinois.edu/greenstreetfinancial?password=c@$hM0n3y1999' \
                        '&type=insert&table=DipRipPattern&symbol=' + str(stock) + '&price=' + str(
                    stock_info['Current Price']) + \
                        '&volume_traded=3000000&percent_change=0.5&threshold=' + str(threshold)
                r = requests.get(query)
            except:
                pass
            traded.add(stock)
            symbol = stock
            symbol_bars = api.get_barset(symbol, 'minute', 1).df.iloc[0]
            symbol_price = symbol_bars[symbol]['close']
            api.submit_order(
                symbol=symbol,
                qty=1000,
                side='buy',
                type='stop',
                time_in_force='gtc',
                stop_price=str(threshold),
                order_class='bracket',
                stop_loss={'stop_price': threshold - 0.03,
                           'limit_price': threshold - 0.03},
                take_profit={'limit_price': threshold * 1.05}
            )
        print(stock + ': $' + str(threshold))

