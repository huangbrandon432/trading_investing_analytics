from IPython.display import display
import panel as pn
from panel.interact import interact, interactive, fixed, interact_manual
from panel import widgets
import pandas as pd
import numpy as np
import tickers_graphing_module as tg
import legacy_analysis_module as am
import analytics_functions as af
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import importlib
import bokeh
import param
import io
importlib.reload(am)
importlib.reload(tg)
importlib.reload(af)

raw_css = """
.bk-root .bk-tabs-header.bk-above .bk-headers, .bk-root .bk-tabs-header.bk-below .bk-headers{
font-size:16px;
}
"""

pn.extension('plotly', raw_css=[raw_css])




#First Tab
ticker_info_button = pn.widgets.Button(name='Get Ticker Stats and Financials', button_type='primary')
text = pn.widgets.TextInput(name = 'Ticker', value='TSLA')
def b(event):
    af.get_share_stats_and_financials(text.value)

swaggystocks_button = pn.widgets.Button(name='Swaggy Stocks', button_type='primary')
def c(event):
    af.swaggy_stocks()

options_chain_button = pn.widgets.Button(name='Get Options Chain', button_type='primary')
text3 = pn.widgets.TextInput(name = 'Options Chain Ticker', value='TSLA')
def d(event):
    af.get_options_chain(text3.value)

shorted_stocks_button = pn.widgets.Button(name='Top Shorted Stocks', button_type='primary')
def e(event):
    af.get_top_shorted_stocks()


ticker_info_button.on_click(b)
swaggystocks_button.on_click(c)
options_chain_button.on_click(d)
shorted_stocks_button.on_click(e)
get_stock_info = pn.Column(text, ticker_info_button, pn.Spacer(height = 5), swaggystocks_button, pn.Spacer(height = 5), text3, options_chain_button, pn.Spacer(height = 5), shorted_stocks_button, name = 'Get Stock Info')



#Second Tab
class Trades_Stats(param.Parameterized):

    select_brokerage=pn.widgets.Select(name = 'Select Brokerage', options = ['Webull', 'Robinhood', 'Charles Schwab'])
    select_instrument=pn.widgets.Select(name = 'Select Instrument', options = ['Option', 'Stock'])
    select_symbol_to_filter=pn.widgets.Select(name = 'Select Symbol', options = [])
    file_input = param.Parameter()
    data = param.DataFrame()

    def __init__(self, **params):
        super().__init__(file_input=pn.widgets.FileInput(accept='.csv,.xlsx,.xls'), **params)
        self.total_gain = pn.indicators.Number(name='Total Realized Gain', format='${value}', font_size = '30pt')
        self.total_loss = pn.indicators.Number(name='Total Realized Loss', format='${value}', font_size = '30pt')
        self.wins = pn.indicators.Number(name='Wins', format='{value}', font_size = '30pt')
        self.losses = pn.indicators.Number(name='Losses', format='{value}', font_size = '30pt')
        self.win_loss_ratio = pn.indicators.Number(name='Win Loss Ratio', format='{value}', font_size = '30pt')
        self.win_rate = pn.indicators.Number(name='Win Rate', format='{value}', font_size = '30pt')
        self.profit_factor = pn.indicators.Number(name='Profit Factor', format='{value}', font_size = '30pt')
        self.max_trade_loss = pn.indicators.Number(name='Max Trade Loss', format='${value}', font_size = '30pt')
        self.max_trade_gain = pn.indicators.Number(name='Max Trade Gain', format='${value}', font_size = '30pt')
        self.trades_df_pane = pn.widgets.DataFrame(name = 'Orders', width=1200, height = 1000)
        self.top_trades_df_pane = pn.widgets.DataFrame(name = 'Top Trades', width=1200, height = 400)
        self.bottom_trades_df_pane = pn.widgets.DataFrame(name = 'Bottom Trades', width=1200, height = 400)
        self.filtered_trades_df_pane = pn.widgets.DataFrame(name = 'Filtered Trades', width=1200, height = 400)


    @param.depends("file_input.value", 'select_brokerage.value', 'select_instrument.value', watch=True)
    def parse_file_input(self):
        value = self.file_input.value
        brokerage = self.select_brokerage.value
        if value and brokerage == 'Robinhood':
            string_io = io.StringIO(value.decode("utf8"))
            self.data = af.preprocess_rh_stock_orders(string_io)
        if value and brokerage == 'Webull':
            string_io = io.StringIO(value.decode("utf8"))
            self.data = af.preprocess_wb_orders_stats(string_io, instrument_type = self.select_instrument.value)
        if value and brokerage == 'Charles Schwab':
            string_io = io.StringIO(value.decode("utf8"))
            self.data = af.preprocess_schwab_orders(string_io)

    @param.depends('data', watch = True)
    def refresh_filter_symbols(self):
        self.select_symbol_to_filter.options = sorted(list(self.data['symbol'].unique()))

    @param.depends('data', 'select_instrument.value', 'select_symbol_to_filter.value', watch=True)
    def get_df(self):
        if self.select_instrument.value == 'Option':
            trades = af.Options(self.data)
        elif self.select_instrument.value == 'Stock':
            trades = af.Stocks(self.data)

        trades.examine_trades()
        trades.trades_df.index.name = 'Trade #'
        self.total_gain.value = round(trades.total_gain)
        self.total_loss.value = round(trades.total_loss)
        self.wins.value = trades.win_count
        self.losses.value = trades.loss_count
        self.win_loss_ratio.value = round(trades.win_count/trades.loss_count, 2)
        self.win_rate.value = round(trades.win_count/(trades.win_count + trades.loss_count), 2)
        self.profit_factor.value = round(trades.total_gain/trades.total_loss, 2)*-1
        self.max_trade_loss.value = round(trades.trades_df['Gain'].min())
        self.max_trade_gain.value = round(trades.trades_df['Gain'].max())
        self.trades_df_pane.value = trades.trades_df
        self.top_trades_df_pane.value = trades.trades_df[trades.trades_df['Gain'] > 0].sort_values(by = 'Gain', ascending = False).head(20)
        self.bottom_trades_df_pane.value = trades.trades_df[trades.trades_df['Gain'] < 0].sort_values(by = 'Gain', ascending = True).head(20)
        self.filtered_trades_df_pane.value = trades.trades_df[trades.trades_df['Symbol'] == self.select_symbol_to_filter.value]



    def view(self):
        return pn.Column(
            "## Upload and process data",
            self.select_brokerage,
            self.select_instrument,
            self.file_input,
            pn.layout.Divider(),
            self.total_gain,
            self.total_loss,
            self.wins,
            self.losses,
            self.win_rate,
            self.win_loss_ratio,
            self.profit_factor,
            self.max_trade_loss,
            self.max_trade_gain,
            pn.Spacer(height = 50),
            "## Trades",
            self.trades_df_pane,
            pn.Spacer(height = 30),
            "## Top Performing Trades",
            self.top_trades_df_pane,
            pn.Spacer(height = 30),
            "## Bottom Performing Trades",
            self.bottom_trades_df_pane,
            pn.Spacer(height = 30),
            "## Filtered Trades",
            self.select_symbol_to_filter,
            self.filtered_trades_df_pane,
            name = "Trades Stats"
        )

trades_stats_view = Trades_Stats().view()



#Third Tab
class ExamineCharts(param.Parameterized):

    file_input = param.Parameter()

    select_stock=pn.widgets.Select(name = 'Select Stock', options = [])
    select_brokerage=pn.widgets.Select(name = 'Select Brokerage', options = ['Webull', 'Robinhood', 'Charles Schwab'])
    select_interval=pn.widgets.Select(name = 'Select Time Interval', options = ['2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo'])
    select_export_type=pn.widgets.Select(name = 'Select Export Type', options = ['Stock', 'Option'])

    data = param.DataFrame()

    line_chart = pn.pane.Plotly()
    candlestick_chart = pn.pane.Plotly()

    start_date_input = pn.widgets.TextInput(name='Start Date', placeholder='Enter start date')
    end_date_input = pn.widgets.TextInput(name='End Date', placeholder='Enter end date')

    def __init__(self, **params):
        super().__init__(file_input=pn.widgets.FileInput(accept='.csv,.xlsx,.xls'), **params)


    @param.depends("file_input.value", 'select_brokerage.value', 'select_interval.value', 'select_export_type.value', watch=True)
    def parse_file_input(self):
        value = self.file_input.value
        brokerage = self.select_brokerage.value
        interval = self.select_interval.value
        export_type = self.select_export_type.value

        if value and brokerage == 'Robinhood':
            string_io = io.StringIO(value.decode("utf8"))
            self.data = af.preprocess_rh_stock_orders(string_io)
        if value and brokerage == 'Webull':
            string_io = io.StringIO(value.decode("utf8"))
            self.data = af.preprocess_wb_orders(string_io, interval = interval, export_type = export_type)
        if value and brokerage == 'Charles Schwab':
            string_io = io.StringIO(value.decode("utf8"))
            self.data = af.preprocess_schwab_orders(string_io)

    @param.depends('data', watch = True)
    def refresh_symbols(self):
        self.select_stock.options = sorted(list(self.data.symbol.unique()))


    @param.depends('data', 'select_stock.value', 'start_date_input.value', 'end_date_input.value', 'select_interval.value', 'select_export_type.value', watch=True)
    def plotting(self):
        trades = af.Stocks(self.data)
        trades.examine_trades(export_type=self.select_export_type.value)

        if self.select_stock.value:
            self.candlestick_chart.object = tg.plot_buysell_points_candlestick(self.select_stock.value, tradesdf = trades.trades_df, start_date = self.start_date_input.value,
                                                    end_date= self.end_date_input.value, interval = self.select_interval.value, instrument=self.select_export_type.value)
            
            self.line_chart.object = tg.plot_buysell_points_line(self.select_stock.value, tradesdf = trades.trades_df, start_date = self.start_date_input.value,
                                                    end_date= self.end_date_input.value, interval = self.select_interval.value, instrument=self.select_export_type.value)

        else:
            print('select stock')


    def view(self):
        return pn.Column(
            "## Examine Charts",
            self.select_brokerage,
            self.file_input,
            self.select_export_type,
            self.select_stock,
            self.select_interval,
            self.start_date_input,
            self.end_date_input,
            pn.layout.Divider(),
            self.candlestick_chart,
            pn.Spacer(height = 150),
            self.line_chart,
            name = "Examine Charts"
        )

examine_charts_view = ExamineCharts().view()




#Putting them all together
tabs = pn.Tabs(get_stock_info, trades_stats_view, examine_charts_view)
tabs.show()
