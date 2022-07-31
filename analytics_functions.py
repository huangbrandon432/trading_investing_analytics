import pandas as pd
import webbrowser
import robin_stocks.robinhood as r
from IPython.display import Markdown
import yfinance as yf
from datetime import date, timedelta, datetime
import datapackage

def printmd(string):
    display(Markdown(string))



def get_share_stats_and_financials(ticker):

    link = "https://finance.yahoo.com/quote/"+ticker+'/key-statistics?p='+ticker
    link2 = "https://finance.yahoo.com/quote/"+ticker+"/financials?p="+ticker

    webbrowser.open_new_tab(link)
    webbrowser.open_new_tab(link2)


def swaggy_stocks():

    swaggy_stocks_link = "https://swaggystocks.com/dashboard/wallstreetbets/ticker-sentiment"

    webbrowser.open_new_tab(swaggy_stocks_link)


def get_options_chain(ticker):

    options_chain_link = "https://finance.yahoo.com/quote/"+ticker+"/options/"

    webbrowser.open_new_tab(options_chain_link)

def get_top_shorted_stocks():

    short_interest_stocks_link = "https://www.marketwatch.com/tools/screener/short-interest"

    webbrowser.open_new_tab(short_interest_stocks_link)




def preprocess_rh_stock_orders(file):


    stock_orders_df = pd.read_csv(file)
    stock_orders_df['date'] = stock_orders_df['date'].replace('T(.*)', '', regex=True)
    stock_orders_df['date'] = pd.to_datetime(stock_orders_df['date'], format = '%Y-%m-%d')

    stock_orders_df = stock_orders_df.iloc[::-1].reset_index(drop=True)


    #accounting for stock splits
    for i in range(len(stock_orders_df)):

        transac_date = stock_orders_df.loc[i, 'date']
        symbol = stock_orders_df.loc[i, 'symbol']

        if symbol == 'SOXL' and  transac_date < pd.to_datetime('2021-03-02'):
            stock_orders_df.loc[i, 'average_price'] /= 15
            stock_orders_df.loc[i, 'quantity'] *= 15

        if symbol == 'TECL' and transac_date < pd.to_datetime('2021-03-02'):
            stock_orders_df.loc[i, 'average_price'] /= 10
            stock_orders_df.loc[i, 'quantity'] *= 10

        if symbol == 'AAPL' and transac_date < pd.to_datetime('2020-08-28'):
            stock_orders_df.loc[i, 'average_price'] /= 4
            stock_orders_df.loc[i, 'quantity'] *= 4

        if symbol == 'TSLA' and transac_date < pd.to_datetime('2020-08-31'):
            stock_orders_df.loc[i, 'average_price'] /= 5
            stock_orders_df.loc[i, 'quantity'] *= 5


    stock_orders_df['total'] = stock_orders_df['quantity']*stock_orders_df['average_price']
    return stock_orders_df



def examine_trades(self):

    total_gain = 0
    total_loss = 0
    trades = []

    trading_dict = {}
    net_gain_loss = 0

    for i in range(len(stock_orders_df)):

        side = stock_orders_df.loc[i, 'side']
        symbol = stock_orders_df.loc[i, 'symbol']
        date = stock_orders_df.loc[i, 'date'].strftime('%Y-%m-%d')
        quantity = stock_orders_df.loc[i, 'quantity']
        avg_price = stock_orders_df.loc[i, 'average_price']
        total = round(stock_orders_df.loc[i, 'total'],2)


        if side == 'buy':

            if symbol+'_avgprice' in trading_dict:
                cur_total = trading_dict[symbol+'_quantity']*trading_dict[symbol+'_avgprice']
                new_total = cur_total + quantity * avg_price
                trading_dict[symbol+'_quantity'] += quantity
                trading_dict[symbol+'_avgprice'] = new_total/trading_dict[symbol+'_quantity']

            else:
                trading_dict[symbol+'_avgprice'] = avg_price
                trading_dict[symbol+'_quantity'] = quantity


            cur_avg_price = round(trading_dict[symbol+'_avgprice'],2)
            cur_quantity = round(trading_dict[symbol+'_quantity'],2)

            trades.append([side, symbol, date, round(quantity, 2), round(avg_price, 2), cur_quantity, cur_avg_price, total, 0, str(0) + '%', net_gain_loss, ''])



        #if sell
        if side == 'sell':

            if symbol+'_avgprice' in trading_dict:


                gain = round((avg_price - trading_dict[symbol+'_avgprice']) * quantity,2)
                perc_gain = round((avg_price - trading_dict[symbol+'_avgprice'])/trading_dict[symbol+'_avgprice']*100,2)


                if gain >= 0:
                    total_gain += gain

                else:
                    total_loss += gain


                trading_dict[symbol+'_quantity'] -= quantity

                net_gain_loss = round(total_gain + total_loss,2)
                cur_avg_price = round(trading_dict[symbol+'_avgprice'],2)
                cur_quantity = round(trading_dict[symbol+'_quantity'],2)

                trades.append([side, symbol, date, round(quantity, 2), round(avg_price, 2), cur_quantity, cur_avg_price, total, gain, str(perc_gain) + '%', net_gain_loss, ''])



                #if holding = 0, pop symbol avgprice and quantity
                if trading_dict[symbol+'_quantity'] == 0:
                    trading_dict.pop(symbol+'_avgprice')
                    trading_dict.pop(symbol+'_quantity')

            else:

                gain = round(avg_price * quantity,2)
                total_gain += gain

                net_gain_loss = round(total_gain + total_loss,2)

                trades.append([side, symbol, date, round(quantity, 2), round(avg_price, 2), None, None, total, gain, str(0) + '%', net_gain_loss, 'Yes'])


    trades_df = pd.DataFrame(trades, columns = ['Side', 'Symbol', 'Date', 'Quantity', 'Avg_Price', 'Cur Quantity', 'Cur_Avg_Cost', 'Total', 'Gain', '% Gain', 'Net Gain/Loss', 'Free/Acquired Stock'])

    gains_df = trades_df[(trades_df['Gain'] >= 0) & (trades_df['Side'] == 'sell')].sort_values('Gain', ascending = False).reset_index(drop=True)
    losses_df = trades_df[(trades_df['Gain'] < 0) & (trades_df['Side'] == 'sell')].sort_values('Gain').reset_index(drop=True)


class Stocks:
    def __init__(self, stock_orders_df):

        self.stock_orders_df = stock_orders_df

    def examine_trades(self):

        self.total_gain = 0
        self.total_loss = 0
        self.trades = []

        trading_dict = {}
        net_gain_loss = 0

        for i in range(len(self.stock_orders_df)):

            side = self.stock_orders_df.loc[i, 'side']
            symbol = self.stock_orders_df.loc[i, 'symbol']
            date = self.stock_orders_df.loc[i, 'date'].strftime('%Y-%m-%d')
            quantity = self.stock_orders_df.loc[i, 'quantity']
            avg_price = self.stock_orders_df.loc[i, 'average_price']
            total = round(self.stock_orders_df.loc[i, 'total'],2)


            if side == 'buy':

                if symbol+'_avgprice' in trading_dict:
                    cur_total = trading_dict[symbol+'_quantity']*trading_dict[symbol+'_avgprice']
                    new_total = cur_total + quantity * avg_price
                    trading_dict[symbol+'_quantity'] += quantity
                    trading_dict[symbol+'_avgprice'] = new_total/trading_dict[symbol+'_quantity']

                else:
                    trading_dict[symbol+'_avgprice'] = avg_price
                    trading_dict[symbol+'_quantity'] = quantity


                cur_avg_price = round(trading_dict[symbol+'_avgprice'],2)
                cur_quantity = round(trading_dict[symbol+'_quantity'],2)

                self.trades.append([side, symbol, date, round(quantity, 2), round(avg_price, 2), cur_quantity, cur_avg_price, total, 0, str(0) + '%', net_gain_loss, ''])



            #if sell
            if side == 'sell':

                if symbol+'_avgprice' in trading_dict:


                    gain = round((avg_price - trading_dict[symbol+'_avgprice']) * quantity,2)
                    perc_gain = round((avg_price - trading_dict[symbol+'_avgprice'])/trading_dict[symbol+'_avgprice']*100,2)


                    if gain >= 0:
                        self.total_gain += gain

                    else:
                        self.total_loss += gain


                    trading_dict[symbol+'_quantity'] -= quantity

                    net_gain_loss = round(self.total_gain + self.total_loss,2)
                    cur_avg_price = round(trading_dict[symbol+'_avgprice'],2)
                    cur_quantity = round(trading_dict[symbol+'_quantity'],2)

                    self.trades.append([side, symbol, date, round(quantity, 2), round(avg_price, 2), cur_quantity, cur_avg_price, total, gain, str(perc_gain) + '%', net_gain_loss, ''])



                    #if holding = 0, pop symbol avgprice and quantity
                    if trading_dict[symbol+'_quantity'] == 0:
                        trading_dict.pop(symbol+'_avgprice')
                        trading_dict.pop(symbol+'_quantity')

                else:

                    gain = round(avg_price * quantity,2)
                    self.total_gain += gain

                    net_gain_loss = round(self.total_gain + self.total_loss,2)

                    self.trades.append([side, symbol, date, round(quantity, 2), round(avg_price, 2), None, None, total, gain, str(0) + '%', net_gain_loss, 'Yes'])


        self.trades_df = pd.DataFrame(self.trades, columns = ['Side', 'Symbol', 'Date', 'Quantity', 'Avg_Price', 'Cur Quantity', 'Cur_Avg_Cost', 'Total', 'Gain', '% Gain', 'Net Gain/Loss', 'Free/Acquired Stock'])

        self.gains_df = self.trades_df[(self.trades_df['Gain'] >= 0) & (self.trades_df['Side'] == 'sell')].sort_values('Gain', ascending = False).reset_index(drop=True)
        self.losses_df = self.trades_df[(self.trades_df['Gain'] < 0) & (self.trades_df['Side'] == 'sell')].sort_values('Gain').reset_index(drop=True)



    def add_price_diff(self):
        time_start = time.time()

        if self.crypto == 'no':

            stocks_sold = list(set(self.trades_df[self.trades_df['Side'] == 'sell']['Symbol']))

            ticker_cur_price = []

            for i in stocks_sold:
                try:
                    ticker = yf.Ticker(i)
                    close = round(ticker.history(period = "1d").reset_index(drop=True).loc[0, 'Close'],2)

                    ticker_cur_price.append((i, close, 'sell'))

                except:
                    pass

            ticker_cur_price = pd.DataFrame(ticker_cur_price, columns =['Symbol', 'Current Price', 'Side'])


            self.trades_df_with_price_diff = self.trades_df.merge(ticker_cur_price, how = 'left', on = ['Symbol', 'Side'])

            for i in range(len(self.trades_df_with_price_diff)):

                transac_date = pd.to_datetime(self.trades_df_with_price_diff.loc[i, 'Date'])
                symbol = self.trades_df_with_price_diff.loc[i, 'Symbol']

                if symbol == 'SOXL' and transac_date < pd.to_datetime('2021-03-02'):
                    self.trades_df_with_price_diff.loc[i, 'Current Price'] *= 15

                if symbol == 'TECL' and transac_date < pd.to_datetime('2021-03-02'):
                    self.trades_df_with_price_diff.loc[i, 'Current Price'] *= 10

                if symbol == 'AAPL' and transac_date < pd.to_datetime('2020-08-28'):
                    self.trades_df_with_price_diff.loc[i, 'Current Price'] *= 4

                if symbol == 'TSLA' and transac_date < pd.to_datetime('2020-08-31'):
                    self.trades_df_with_price_diff.loc[i, 'Current Price'] *= 5

        else:
            crypto_sold = list(set(self.trades_df[self.trades_df['Side'] == 'sell']['Symbol']))

            crypto_cur_price = []

            for i in crypto_sold:
                try:
                    crypto_market_price = float(r.crypto.get_crypto_quote(i, info='mark_price'))

                    crypto_cur_price.append((i, crypto_market_price, 'sell'))

                except:
                    pass

            crypto_cur_price = pd.DataFrame(crypto_cur_price, columns =['Symbol', 'Current Price', 'Side'])


            self.trades_df_with_price_diff = self.trades_df.merge(crypto_cur_price, how = 'left', on = ['Symbol', 'Side'])



        self.trades_df_with_price_diff['Price Sold & Curr Price % Diff'] = round((self.trades_df_with_price_diff['Current Price'] - self.trades_df_with_price_diff["Avg_Price"])/self.trades_df_with_price_diff["Avg_Price"] * 100, 2)
        self.trades_df_with_price_diff['Avg Cost & Curr Price % Diff'] = round((self.trades_df_with_price_diff['Current Price'] - self.trades_df_with_price_diff["Cur_Avg_Cost"])/self.trades_df_with_price_diff["Cur_Avg_Cost"] * 100, 2)

        self.trades_df_with_price_diff['Current Price'].fillna('', inplace=True)
        self.trades_df_with_price_diff['Price Sold & Curr Price % Diff'].fillna('', inplace=True)
        self.trades_df_with_price_diff['Avg Cost & Curr Price % Diff'].fillna('', inplace=True)

        self.trades_df_with_price_diff['Price Sold & Curr Price % Diff'] = self.trades_df_with_price_diff['Price Sold & Curr Price % Diff'].apply(lambda x: str(x) + '%' if x != '' else '')
        self.trades_df_with_price_diff['Avg Cost & Curr Price % Diff'] = self.trades_df_with_price_diff['Avg Cost & Curr Price % Diff'].apply(lambda x: str(x) + '%' if x != '' else '')



        self.gains_df_with_price_diff = self.trades_df_with_price_diff[(self.trades_df_with_price_diff['Gain'] >= 0) & (self.trades_df_with_price_diff['Side'] == 'sell')].sort_values('Gain', ascending = False).reset_index(drop=True)
        self.losses_df_with_price_diff = self.trades_df_with_price_diff[(self.trades_df_with_price_diff['Gain'] < 0) & (self.trades_df_with_price_diff['Side'] == 'sell')].sort_values('Gain').reset_index(drop=True)

        print()
        time_end = time.time()
        print('Total runtime: ', round(time_end - time_start,2) , 's')

class Watchlists:

    def __init__(self):

        self.watchlists_data = r.account.get_all_watchlists(info=None)
        self.watchlists = []

        for i in self.watchlists_data['results']:
            self.watchlists.append(i['display_name'])

        print(f'Watchlists: \n {self.watchlists}')


    def print_watchlist_tickers(self, watchlist_name = ''):

        symbols_in_investing_trading = [i['symbol'] for i in r.account.get_watchlist_by_name(name = watchlist_name, info=None)['results']]

        print(f'{watchlist_name}: \n{symbols_in_investing_trading}')


    def get_watchlist_tickers(self, watchlist_name = ''):

        symbols_in_investing_trading = [i['symbol'] for i in r.account.get_watchlist_by_name(name = watchlist_name, info=None)['results']]

        return symbols_in_investing_trading


    def delete_from_watchlist(self, watchlist_name = '', symbols = []):
        r.account.delete_symbols_from_watchlist(inputSymbols = symbols, name = watchlist_name)

    def add_to_watchlist(self, watchlist_name = '', symbols = []):
        r.account.post_symbols_to_watchlist(inputSymbols = symbols, name = watchlist_name)

    def check_if_in_watchlist(self, ticker = '', watchlist = ''):

        symbols = [i['symbol'] for i in r.account.get_watchlist_by_name(name = watchlist, info=None)['results']]

        if ticker in symbols:
            print(True)
        else:
            print(False)

    def get_upcoming_earnings(self, watchlists = [], days_away_threshold = 21):
        for i in watchlists:

            print('Watchlist: ', i)
            print()

            watchlist = r.account.get_watchlist_by_name(name=i,info=None)['results']
            watchlist = [watchlist[j]['symbol'] for j in range(len(watchlist))]

            for x in watchlist:

                if x in ['BTC', 'LTC', 'ETH', 'DOGE', 'ETC']:
                    continue

                ticker = yf.Ticker(x)


                try:
                    events = ticker.calendar.T

                except:
                    continue

                if events.empty:
                    continue

                if (events['Earnings Date'].iloc[0] > date.today()) and (events['Earnings Date'].iloc[0] < (date.today() + timedelta(days_away_threshold))):

                    #only print ticker with upcoming earnings
                    print(x)

                    earnings_date = events['Earnings Date'].apply(lambda x: x.strftime("%Y-%m-%d")).values
                    print('Next Earnings Date(s):', earnings_date, '*Soon*')
                    print()


            print()


def check_if_in_sp500(symbol = ''):

    data_url = 'https://datahub.io/core/s-and-p-500-companies/datapackage.json'

    # load Data Package into storage
    package = datapackage.Package(data_url)

    # load only tabular data
    resources = package.resources
    for resource in resources:
        if resource.tabular:
            sp500 = pd.read_csv(resource.descriptor['path'])

    if symbol in sp500['Symbol'].values:
        print(True)
    else:
        print(False)



def filter_stocks_by_movement(watchlist_names = [], period = '1mo', point_of_reference_days = -10, return_threshold = 0.1, show_yesterday = 'no'):
    #valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
    printmd(f'Past {point_of_reference_days*-1} days')
    scanned_symbols = []
    symbols_meet_threshold_scanned = []
    momentum_stocks = {}
    printed_dates = 0

    total_num_of_symbols = 0
    total_symbols_threshold = 0

    for j in watchlist_names:
        printmd('**'+j+'**')

        try:
            symbols = [i['symbol'] for i in r.account.get_watchlist_by_name(name = j, info=None)['results']]
        except:
            continue

        num_of_symbols = len(symbols)
        total_num_of_symbols += num_of_symbols
        symbols_threshold = 0


        for i in symbols:
            if i in ['XRP', 'BTC', 'ETH', 'LTC', 'DOGE', 'BSV']:
                i += '-USD'

            if i in scanned_symbols:
                if i in symbols_meet_threshold_scanned:
                    symbols_threshold += 1
                continue

            else:
                scanned_symbols.append(i)
                try:
                    ticker_obj = yf.Ticker(i)
                    ticker_hist = ticker_obj.history(period = period)
                    printmd(f'Last date in data: {ticker_hist.index[-1]}')
                    current_price = ticker_hist.Close[-1]

                except:
                    continue


                try:
                    reference_price = ticker_hist.Close[point_of_reference_days]
                    if printed_dates == 0:
                        printmd(f'From {ticker_hist.index[point_of_reference_days].strftime("%Y-%m-%d")} to {ticker_hist.index[-1].strftime("%Y-%m-%d")}')
                        printed_dates = 1
                except:
                    reference_price = ticker_hist.Close[0]

                try:
                    if show_yesterday == 'yes':
                        yesterday_price = ticker_hist.Close[-2]
                        two_days_ago_price = ticker_hist.Close[-3]
                        yesterday_price_change = round((yesterday_price - two_days_ago_price)*100 / yesterday_price, 2)

                except:
                    pass


                price_change = round((current_price - reference_price)*100 / reference_price, 2)

                print_string = ''

                if return_threshold > 0:

                    if price_change >= (return_threshold*100):
                        print_string += str(i) + '- Change: ' + str(price_change) + '%'
                        # printmd(f'{i} - Change: {str(price_change)}%')
                        momentum_stocks.update({i: str(price_change) + '% ' + 'return'})
                        if show_yesterday == 'yes':
                            print_string += ', ' + 'Yesterday Change: ' + str(yesterday_price_change) + '%'
                            # printmd(f'Yesterday Change: {str(yesterday_price_change)}%')
                        symbols_meet_threshold_scanned.append(i)
                        printmd(print_string)
                        symbols_threshold += 1
                        total_symbols_threshold += 1

                else:
                    if price_change <= (return_threshold*100):
                        print_string += str(i) + '- Change: ' + str(price_change) + '%'
                        # printmd(f'{i} - Return: {str(price_change)}%')
                        momentum_stocks.update({i: str(price_change) + '% ' + 'return'})
                        if show_yesterday == 'yes':
                            print_string += ', ' + 'Yesterday Change: ' + str(yesterday_price_change) + '%'
                            # printmd(f'Yesterday Change: {str(yesterday_price_change)}%')
                        symbols_meet_threshold_scanned.append(i)
                        printmd(print_string)
                        symbols_threshold += 1
                        total_symbols_threshold += 1

        symbols_perc = round(symbols_threshold/num_of_symbols*100,2)

        printmd(f'Perc of symbols: {symbols_perc}%')
        print()

    print(momentum_stocks)
    total_symbols_perc = round(total_symbols_threshold/total_num_of_symbols*100,2)
    printmd(f'Perc of total symbols: {total_symbols_perc}%')

def get_stock_movements(tickers = [], period = '1mo', point_of_reference_days = -10):
    #valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
    scanned_symbols = []
    printed_dates = 0


    for i in tickers:
        if i in ['XRP', 'BTC', 'ETH', 'LTC', 'DOGE', 'BSV']:
            i += '-USD'
        if i in scanned_symbols:
            continue
        else:
            scanned_symbols.append(i)
            try:
                ticker_obj = yf.Ticker(i)
                ticker_hist = ticker_obj.history(period = period)
                current_price = ticker_hist.Close[-1]

            except:
                continue

            try:
                reference_price = ticker_hist.Close[point_of_reference_days]
                if printed_dates == 0:
                    printmd(f'From {ticker_hist.index[point_of_reference_days]} to {ticker_hist.index[-1]}')
                    printed_dates = 1
            except:
                reference_price = ticker_hist.Close[0]

            return_perc = round((current_price - reference_price)*100 / reference_price,2)



            printmd(f'{i}: {return_perc}%')


def create_generator(dataframe = None, date_after = '2021-01-01', date_before = None, symbols = None):
    if date_after and not date_before:
        generator = (i for i in dataframe[dataframe['date'] >= date_after].symbol.unique())

    elif not date_after and date_before:
        generator = (i for i in dataframe[dataframe['date'] <= date_before].symbol.unique())

    elif date_after and date_before:
        generator = (i for i in dataframe[(dataframe['date'] <= date_before) & (dataframe['date'] >= date_after)].symbol.unique())

    elif symbols:
        generator = (i for i in symbols)
    else:
        generator = (i for i in dataframe.symbol.unique())

    return generator
