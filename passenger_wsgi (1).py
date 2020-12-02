import os
import sys
import json
from cgi import parse_qs, escape
import mysql.connector as mysql
import pymongo
import urllib

sys.path.insert(0, os.path.dirname(__file__))

# You can ignore this function, this is for the website config
def application(environ, start_response):

    d = parse_qs(environ['QUERY_STRING'])

    start_response('200 OK', [('Content-Type', 'application/json')])
    if len(d) > 0:
        message = parser(d)
    else:
        message = start_page()
    return [message.encode()]

# This is where all the endpoints start
def parser(param):

    # Getting the password for the query sent by client
    password = param.get('password', ['None'])[0]

    # Connecting to the sql db
    try:
        db = mysql.connect(
            host = "localhost",
            user = "sumuksr2_greenstreetfinancial",
            passwd = password,
            database = "sumuksr2_greenstreetfinancial"
        )

        cursor = db.cursor()

    except Exception as E:
        return str(E)

    # Connecting to the mongo db
    try:
        client = pymongo.MongoClient("mongodb+srv://greenstreetfinancial:"+urllib.parse.quote(password)+"@cluster0.baluh.mongodb.net/cs411_finalproject?retryWrites=true&w=majority")
        mongo_db = client['cs411_finalproject']
    except Exception as e:
        return str(e)

    # Getting the type of query requested
    query_type = param.get('type', ['None'])[0]

    # If it is a sql insert the following will happen
    if query_type == 'insert':

        # Getting which table client wants to insert to
        table = param.get('table', ['None'])[0]

        if table == 'User':
            userID = param.get('userID', ['None'])[0]
            portfolio_value = param.get('portfolio_value', ['None'])[0]
            query = "INSERT INTO User (userID, portfolio_value) VALUES (%s, %s)"
            values = (userID, portfolio_value)
            try:
                cursor.execute(query, values)
                db.commit()
                return "1"
            except Exception as E:
                return str(E)

        if table == 'DipRipPattern':
            symbol = param.get('symbol', ['None'])[0]
            price = param.get('price', ['None'])[0]
            volume_traded = param.get('volume_traded', ['None'])[0]
            percent_change = param.get('percent_change', ['None'])[0]
            threshold = param.get('threshold', ['None'])[0]
            query = "INSERT INTO DipRipPattern (symbol, price, volume_traded, percent_change, threshold) VALUES (%s, %s, %s, %s, %s)"
            values = (symbol, price, volume_traded, percent_change, threshold)
            try:
                cursor.execute(query, values)
                db.commit()
                return "1"
            except Exception as E:
                return "-1"

        if table == 'Watchlist':
            symbol = param.get('symbol', ['None'])[0]
            userID = param.get('userID', ['None'])[0]
            pattern_type = param.get('pattern_type', ['None'])[0]
            query = "INSERT INTO Watchlist (symbol, userID, pattern_type) VALUES (%s, %s, %s)"
            values = (symbol, userID, pattern_type)
            try:
                cursor.execute(query, values)
                db.commit()
                return "1"
            except Exception as E:
                return str(E)

        if table == 'DipBuyPattern':
            symbol = param.get('symbol', ['None'])[0]
            bid_ask_ratio = param.get('bid_ask_ratio', ['None'])[0]
            volume_change = param.get('volume_change', ['None'])[0]
            price_drop = param.get('price_drop', ['None'])[0]
            query = "INSERT INTO DipBuyPattern (symbol, bid_ask_ratio, volume_change, price_drop) VALUES (%s, %s, %s, %s)"
            values = (symbol, bid_ask_ratio, volume_change, price_drop)
            try:
                cursor.execute(query, values)
                db.commit()
                return "1"
            except Exception as E:
                return "-1"

        if table == 'Stock':
            symbol = param.get('symbol', ['None'])[0]
            current_price = param.get('current_price', ['None'])[0]
            value_change = param.get('value_change', ['None'])[0]
            percent_change = param.get('percent_change', ['None'])[0]
            previous_close = param.get('previous_close', ['None'])[0]
            open_ = param.get('open', ['None'])[0]
            volume = param.get('volume', ['None'])[0]
            bid_size = param.get('bid_size', ['None'])[0]
            bid_price = param.get('bid_price', ['None'])[0]
            ask_size = param.get('ask_size', ['None'])[0]
            ask_price = param.get('ask_price', ['None'])[0]
            day_high = param.get('day_high', ['None'])[0]
            day_low = param.get('day_low', ['None'])[0]
            sentiment_rating = param.get('sentiment_rating', ['None'])[0]
            query = "INSERT INTO Stock (symbol, current_price, value_change, percent_change, previous_close, open, volume, bid_size, bid_price, ask_size, ask_price, day_high, day_low, sentiment_rating) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (symbol, current_price, value_change, percent_change, previous_close, open_, volume, bid_size, bid_price, ask_size, ask_price, day_high, day_low, sentiment_rating)
            try:
                cursor.execute(query, values)
                db.commit()
                return "1"
            except Exception as E:
                return str(E)

    # If the query is an update query, the following will happen
    if query_type == 'update':

        # Getting the table they want to update to
        table = param.get('table', ['None'])[0]

        if table == 'User':
            update_table = {}
            update_table['userID'] = param.get('userID', ['UNCHANGED'])[0]
            update_table['portfolio_value'] = param.get('portfolio_value', ['UNCHANGED'])[0]
            index = param.get('index', ['None'])[0]

            update_values = ''
            for parameter in update_table:
                if  update_table[parameter] != 'UNCHANGED' and parameter != index:
                    update_values = update_values + parameter + ' = ' + update_table[parameter] + ', '
            update_values = update_values[:-2]
            query = "UPDATE User SET " + update_values + " WHERE " + index + " = " + update_table[index]
            try:
                cursor.execute(query)
                db.commit()
                return "1"
            except Exception as E:
                return "-1"

        if table == 'DipRipPattern':
            update_table = {}
            update_table['symbol'] = param.get('symbol', ['UNCHANGED'])[0]
            update_table['price'] = param.get('price', ['UNCHANGED'])[0]
            update_table['volume_traded'] = param.get('volume_traded', ['UNCHANGED'])[0]
            update_table['percent_change'] = param.get('percent_change', ['UNCHANGED'])[0]
            update_table['threshold'] = param.get('threshold', ['UNCHANGED'])[0]
            index = param.get('index', ['None'])[0]

            update_values = ''
            for parameter in update_table:
                if  update_table[parameter] != 'UNCHANGED' and parameter != index:
                    update_values = update_values + parameter + ' = ' + update_table[parameter] + ', '
            update_values = update_values[:-2]
            query = "UPDATE DipRipPattern SET " + update_values + " WHERE " + index + " = " + update_table[index]

            try:
                cursor.execute(query)
                db.commit()
                return "1"
            except Exception as E:
                return "-1"

        if table == 'Watchlist':
            update_table = {}
            update_table['symbol'] = param.get('symbol', ['UNCHANGED'])[0]
            update_table['userID'] = param.get('userID', ['UNCHANGED'])[0]
            update_table['pattern_type'] = param.get('pattern_type', ['UNCHANGED'])[0]
            index = param.get('index', ['None'])[0]

            update_values = ''
            for parameter in update_table:
                if  update_table[parameter] != 'UNCHANGED' and parameter != index:
                    update_values = update_values + parameter + ' = ' + update_table[parameter] + ', '
            update_values = update_values[:-2]
            query = "UPDATE Watchlist SET " + update_values + " WHERE " + index + " = " + update_table[index]
            try:
                cursor.execute(query)
                db.commit()
                return "1"
            except Exception as E:
                return str(E)

        if table == 'DipBuyPattern':
            update_table = {}
            update_table['symbol'] = param.get('symbol', ['UNCHANGED'])[0]
            update_table['bid_ask_ratio'] = param.get('bid_ask_ratio', ['UNCHANGED'])[0]
            update_table['volume_change'] = param.get('volume_change', ['UNCHANGED'])[0]
            update_table['price_drop'] = param.get('price_drop', ['UNCHANGED'])[0]
            index = param.get('index', ['None'])[0]

            update_values = ''
            for parameter in update_table:
                if  update_table[parameter] != 'UNCHANGED' and parameter != index:
                    update_values = update_values + parameter + ' = ' + update_table[parameter] + ', '
            update_values = update_values[:-2]
            query = "UPDATE DipBuyPattern SET " + update_values + " WHERE " + index + " = " + update_table[index]
            try:
                cursor.execute(query)
                db.commit()
                return "1"
            except Exception as E:
                return "-1"

        if table == 'Stock':
            update_table = {}
            update_table['symbol'] = param.get('symbol', ['UNCHANGED'])[0]
            update_table['current_price'] = param.get('current_price', ['UNCHANGED'])[0]
            update_table['value_change'] = param.get('value_change', ['UNCHANGED'])[0]
            update_table['percent_change'] = param.get('percent_change', ['UNCHANGED'])[0]
            update_table['previous_close'] = param.get('previous_close', ['UNCHANGED'])[0]
            update_table['open'] = param.get('open', ['UNCHANGED'])[0]
            update_table['volume'] = param.get('volume', ['UNCHANGED'])[0]
            update_table['bid_size'] = param.get('bid_size', ['UNCHANGED'])[0]
            update_table['bid_price'] = param.get('bid_price', ['UNCHANGED'])[0]
            update_table['ask_size'] = param.get('ask_size', ['UNCHANGED'])[0]
            update_table['ask_price'] = param.get('ask_price', ['UNCHANGED'])[0]
            update_table['day_high'] = param.get('day_high', ['UNCHANGED'])[0]
            update_table['day_low'] = param.get('day_low', ['UNCHANGED'])[0]
            update_table['sentiment_rating'] = param.get('sentiment_rating', ['UNCHANGED'])[0]
            index = param.get('index', ['None'])[0]

            update_values = ''
            for parameter in update_table:
                if  update_table[parameter] != 'UNCHANGED' and parameter != index:
                    update_values = update_values + parameter + ' = ' + update_table[parameter] + ', '
            update_values = update_values[:-2]
            query = "UPDATE Stock SET " + update_values + " WHERE " + index + " = " + update_table[index]
            try:
                cursor.execute(query)
                db.commit()
                return "1"
            except Exception as E:
                return str(E)

    # This returns a specific stock's information
    if query_type == 'get_stock_info':

        symbol = param.get('symbol', ['None'])[0]
        query = "SELECT * FROM Stock WHERE symbol = " + symbol
        try:
            cursor.execute(query)
            records = cursor.fetchall()
            field_names = [i[0] for i in cursor.description]
            #records.insert(0, field_names)
            temp = {}
            for j in range(0, len(field_names)):
                temp[field_names[j]] = records[0][j]
            return json.dumps(temp)
        except:
            return "-1"

    # This returns all the values in the Dip Buy Table
    if query_type == 'get_dip_buy_list':

        query = "SELECT * FROM DipBuyPattern"
        try:
            cursor.execute(query)
            records = cursor.fetchall()
            field_names = [i[0] for i in cursor.description]
            #records.insert(0, field_names)
            output = []
            for i in records:
                temp = {}
                for j in range(0, len(field_names)):
                    temp[field_names[j]] = i[j]
                output.append(temp)
            return json.dumps(output)
        except Exception as E:
            return str(E)

    # This returns all the values in the Dip Rip Table
    if query_type == 'get_dip_rip_list':

        query = "SELECT * FROM DipRipPattern"
        try:
            cursor.execute(query)
            records = cursor.fetchall()
            field_names = [i[0] for i in cursor.description]
            #records.insert(0, field_names)
            output = []
            for i in records:
                temp = {}
                for j in range(0, len(field_names)):
                    temp[field_names[j]] = i[j]
                output.append(temp)
            return json.dumps(output)
        except Exception as E:
            return str(E)

    # This gets a certain user's information
    if query_type == 'get_user_info':

        userID = param.get('userID', ['None'])[0]
        query = "SELECT * FROM User WHERE userID = '" + userID + "'"
        try:
            cursor.execute(query)
            records = cursor.fetchall()
            field_names = [i[0] for i in cursor.description]
            #records.insert(0, field_names)
            output = []
            for i in records:
                temp = {}
                for j in range(0, len(field_names)):
                    temp[field_names[j]] = i[j]
                output.append(temp)
            return json.dumps(output)
        except:
            return "-1"

    # This obtains all information in the watchlist
    if query_type == 'get_watchlist':

        userID = param.get('userID', ['None'])[0]
        query = "SELECT * FROM Watchlist WHERE userID = " + userID
        try:
            cursor.execute(query)
            records = cursor.fetchall()
            field_names = [i[0] for i in cursor.description]
            #records.insert(0, field_names)
            output = []
            for i in records:
                temp = {}
                for j in range(0, len(field_names)):
                    temp[field_names[j]] = i[j]
                output.append(temp)
            return json.dumps(output)
        except Exception as E:
            return -1

    # This returns all values in the Stock table
    if query_type == 'get_stocks':

        query = "SELECT * FROM Stock"
        try:
            cursor.execute(query)
            records = cursor.fetchall()
            field_names = [i[0] for i in cursor.description]
            #records.insert(0, field_names)
            output = []
            for i in records:
                temp = {}
                for j in range(0, len(field_names)):
                    temp[field_names[j]] = i[j]
                output.append(temp)
            return json.dumps(output)
        except Exception as E:
            return -1

    # This is the search bar page endpoind
    if query_type == 'advanced_filter':

        current_price = param.get('current_price', ['0'])[0]
        volume = param.get('volume', ['0'])[0]
        sentiment_rating = param.get('sentiment_rating', ['0'])[0]

        query = "SELECT Stock.symbol, Stock.current_price, Stock.volume, Stock.day_high, Stock.day_low FROM Stock JOIN DipRipPattern ON Stock.symbol = DipRipPattern.symbol JOIN DipBuyPattern ON Stock.symbol = DipBuyPattern.symbol WHERE Stock.current_price >= "+current_price+" AND Stock.volume > "+volume+" AND sentiment_rating >=" + sentiment_rating
        try:
            cursor.execute(query)
            records = cursor.fetchall()
            field_names = [i[0] for i in cursor.description]
            #records.insert(0, field_names)
            output = []
            for i in records:
                temp = {}
                for j in range(0, len(field_names)):
                    temp[field_names[j]] = i[j]
                output.append(temp)
            return json.dumps(output)
        except Exception as E:
            return -1

    # If someone wants to send through a custom query, they can use this
    if query_type == 'custom':

        query = param.get('query', ['None'])[0]
        if 'DELETE' in query:
            return "-1"
        try:
            cursor.execute(query)
            if 'SELECT' in query:
                records = cursor.fetchall()
                field_names = [i[0] for i in cursor.description]
                #records.insert(0, field_names)
                output = []
                for i in records:
                    temp = {}
                    for j in range(0, len(field_names)):
                        temp[field_names[j]] = i[j]
                    output.append(temp)
                return json.dumps(output)
            else:
                return "1"
        except Exception as E:
            return "-1"

    # This is used to insert into the mongo db
    if query_type == 'mongo_insert':

        collection = param.get('collection', ['None'])[0]

        if collection == 'watchlist':
            try:
                details = {}
                details['userID'] = param.get('userID', ['None'])[0]
                details['symbol'] = param.get('symbol', ['None'])[0]
                details['pattern_type'] = param.get('pattern_type', ['None'])[0]
                details['user_note'] = param.get('user_note', ['None'])[0]

                mongo_db['watchlist'].insert_one(details)
                return '1'
            except Exception as E:
                return str(E)

    # This is used to find something in mongo db
    if query_type == 'mongo_find':

        collection = param.get('collection', ['None'])[0]

        if collection == 'watchlist':
            try:
                details = {}
                details['userID'] = param.get('userID', ['None'])[0]

                results = list(mongo_db['watchlist'].find(details))
                output = []
                for result in results:
                    output.append(result)
                return json.dumps(output, default=str)
            except Exception as E:
                return str(E)

    # This is used for updating in mongodb
    if query_type == 'mongo_update':

        collection = param.get('collection', ['None'])[0]

        if collection == 'watchlist':
            try:
                details = {}
                update_values = {}
                details['userID'] = param.get('userID', ['None'])[0]
                details['symbol'] = param.get('symbol', ['None'])[0]
                details['pattern_type'] = param.get('pattern_type', ['None'])[0]
                update_values['user_note'] = param.get('user_note', ['None'])[0]

                mongo_db['watchlist'].update_one(details, {"$set": update_values})
                return "1"
            except Exception as E:
                return str(E)

    # This is for deleting in mongodb
    if query_type == 'mongo_delete':
        collection = param.get('collection', ['None'])[0]

        if collection == 'watchlist':
            try:
                details = {}
                update_values = {}
                details['userID'] = param.get('userID', ['None'])[0]
                details['symbol'] = param.get('symbol', ['None'])[0]
                details['pattern_type'] = param.get('pattern_type', ['None'])[0]

                mongo_db['watchlist'].delete_one(details)
                return "1"
            except Exception as E:
                return str(E)

    return -1


# You can ignore this. This is a prompt for the home page for documentation
def start_page():

    output = " \
Welcome to Endpoints of Green Street Financial Database!\n \
The following shows examples and rules of database API usage:\n\n \
Below is the schema of the database:\n \
DipBuyPattern(symbol, bid_ask_ratio, volume_change, price_drop)\n \
DipRipPattern(symbol, price, volume_traded, percent_change, threshold)\n \
Watchlist(symbol, userID, pattern_type)\n \
User(userID, portfolio_value)\n \
Stock(symbol, current_price, value_change, percent_change, previous_close, open, volume, bid_size, bid_price, ask_size, ask_price, day_high, day_low, sentiment_rating)\n\n\
To insert into a table use the following template:\n \
http://sumuksr2.web.illinois.edu/greenstreetfinancial?password={{PASSWORD}}&type=insert&table={{TABLE NAME}}&{{PARAMETERS}}\n \
In this case, the table name is the name of the table that you want to insert to. Parameters are the attributes and values that you want to insert.\n\n \
An example to insert into Watchlist table would be:\n\
http://sumuksr2.web.illinois.edu/greenstreetfinancial?password={{PASSWORD}}&type=insert&table=Watchlist&symbol=AAPL&userID=johndoe&pattern_type=DIPRIP\n\
This example inserts a new row into Watchlist table in which symbol = AAPL, userID = johndoe, pattern_type = DIPRIP\n\n\
To update a table use the following template:\n\
http://sumuksr2.web.illinois.edu/greenstreetfinancial?password={{PASSWORD}}&type=update&table={{TABLE NAME}}&{{PARAMETERS}}&index={{INDEX OF TABLE}}\n \
In this case, the table name is the name of the table you want to update. Parameters are the attributes and values involved with this change. Index specifies which attribute you are updating on.\n\n\
An example to update the Stock table would be:\n\
http://sumuksr2.web.illinois.edu/greenstreetfinancial?password={{PASSWORD}}&type=update&table=Stock&symbol='AAPL'&current_price=110.10&volume=300234&index=symbol\n\
This example updates the Stock table. Since the index parameter is symbol, we will update current_price to 110.10 and volume to 300234 WHERE symbol = AAPL. PLEASE NOTE the single quotes around the string inputs for this endpoint.\n\n\
To get a Stock's infromation use the following template:\n\
http://sumuksr2.web.illinois.edu/greenstreetfinancial?password={{PASSWORD}}&type=get_stock_info&symbol='{{SYMBOL}}'\n\
In this case, the symbol is the symbol of the stock you want information on. This will return JSON output of stock information.\n\n\
An example to get a Stock's infromation would be:\n\
http://sumuksr2.web.illinois.edu/greenstreetfinancial?password={{PASSWORD}}&type=get_stock_info&symbol='AAPL'\n\
With this example, we will get all the information about AAPL from the Stock table. Please note the single quotes around string input.\n\n\
To get all data in the DipBuyPattern Table use the following template:\n\
http://sumuksr2.web.illinois.edu/greenstreetfinancial?password={{PASSWORD}}&type=get_dip_buy_list\n\
This will return JSON output of information in the DipBuyPattern table.\n\n\
To get all data in the DipRipPattern Table use the following template:\n\
http://sumuksr2.web.illinois.edu/greenstreetfinancial?password={{PASSWORD}}&type=get_dip_rip_list\n\
This will return JSON output of information in the DipRipPattern table.\n\n\
To get all data in the Stock Table use the following template:\n\
http://sumuksr2.web.illinois.edu/greenstreetfinancial?password={{PASSWORD}}&type=get_stocks\n\
This will return JSON output of information in the Stock table.\n\n\
To get a Users's infromation use the following template:\n\
http://sumuksr2.web.illinois.edu/greenstreetfinancial?password={{PASSWORD}}&type=get_user_info&userID='{{userID}}'\n\
In this case, the userID is the userID of the person you want information on. This will return JSON output of user information.\n\n\
An example to get a User's information would be:\
http://sumuksr2.web.illinois.edu/greenstreetfinancial?password={{PASSWORD}}&type=get_user_info&userID='johndoe'\n\
With this example, we will get all the information about johndoe from the User table. Please note the single quotes around string input.\n\n\
To get a Users's Watchlist infromation use the following template:\n\
http://sumuksr2.web.illinois.edu/greenstreetfinancial?password={{PASSWORD}}&type=get_watchlist&userID='{{userID}}'\n\
In this case, the userID is the userID of the person you want watchlist information on. This will return JSON output of user information.\n\n\
An example to get a User's Watchlist information would be:\
http://sumuksr2.web.illinois.edu/greenstreetfinancial?password={{PASSWORD}}&type=get_watchlist&userID='johndoe'\n\
With this example, we will get all the watchlist information about johndoe from the User table. Please note the single quotes around string input.\n\n\
To run a custom SQL query, use the following template:\n\
http://sumuksr2.web.illinois.edu/greenstreetfinancial?password={{PASSWORD}}&type=custom&query={{QUERY}}\n\
In this case, the query is any valid SQL query you want to run. Please note that all delete and remove queries will be blocked.\n\n\
An example to run a custome query would be:\n\
http://sumuksr2.web.illinois.edu/greenstreetfinancial?password={{PASSWORD}}&type=custom&query=SELECT * FROM Watchlist\n\
In this case, the command will reutrn JSON of all items in the Watchlist table.\n\n\n\n\
The MongoDB setup is as below:\n\
Watchlist(userID, symbol, pattern_type, user_note)\n\
History(date, symbol, profit)\n\n\n\
An example to add to watchlist collection would be:\n\
http://sumuksr2.web.illinois.edu/greenstreetfinancial?password=<PASSWORD>&type=mongo_insert&collection=watchlist&userID=demo&symbol=AAPL&pattern_type=DIPRIP&user_note=Hi I like this one.\n\
In this case, the password is the password. Collection is the collection you are inserting to which is watchlist. All others are self-explanatory, please note, there are no extra quotes used for strings anywhere.\n\n\
An example to find from the watchlist collection would be:\n\
http://sumuksr2.web.illinois.edu/greenstreetfinancial?password=<PASSWORD>&type=mongo_find&collection=watchlist&userID=demo\n\
In this case, it will return ALL stocks in a watchlist of userID = demo.\n\n\
An example to update the watchlist collection would be:\n\
http://sumuksr2.web.illinois.edu/greenstreetfinancial?password=<PASSWORD>&type=mongo_update&collection=watchlist&userID=demo&symbol=AAPL&pattern_type=DIPRIP&user_note=Updated User Note LOL.\n\
In this case, it will update the user note for the given userID, symbol, and pattern_type. Please note, this endpoint can only be used to update the note and nothing else.\n\n\
An example to remove a document from the watchlist collection would be:\n\
http://sumuksr2.web.illinois.edu/greenstreetfinancial?password=<PASSWORD>&type=mongo_delete&collection=watchlist&userID=demo&symbol=AAPL&pattern_type=DIPRIP\n\
In this case, it will delete the record which has the provided userID, symbol, and pattern_type.\n\n\
"

    return output
