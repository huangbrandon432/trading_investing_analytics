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
