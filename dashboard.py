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




class Analyze_trades(param.Parameterized):

    select_brokerage=pn.widgets.Select(name = 'Select Brokerage', options = ['Webull', 'Robinhood', 'Charles Schwab'])
    file_input = param.Parameter()
    data = param.DataFrame()

    def __init__(self, **params):
        super().__init__(file_input=pn.widgets.FileInput(accept='.csv,.xlsx,.xls'), **params)
        self.df_pane = pn.pane.DataFrame(width=1000, max_rows = 10)
        self.df_pane2 = pn.pane.DataFrame(width=1000, max_rows = 10)
        self.total_gain = pn.indicators.Number(name='Total Realized Gain', format='${value}', font_size = '30pt')
        self.total_loss = pn.indicators.Number(name='Total Realized Loss', format='${value}', font_size = '30pt')
        self.wins = pn.indicators.Number(name='Wins', format='{value}', font_size = '30pt')
        self.losses = pn.indicators.Number(name='Losses', format='{value}', font_size = '30pt')
        self.win_loss_ratio = pn.indicators.Number(name='Win Loss Ratio', format='{value}', font_size = '30pt')


    @param.depends("file_input.value", 'select_brokerage.value', watch=True)
    def parse_file_input(self):
        value = self.file_input.value
        brokerage = self.select_brokerage.value
        if value and brokerage == 'Robinhood':
            string_io = io.StringIO(value.decode("utf8"))
            self.data = af.preprocess_rh_stock_orders(string_io)
        if value and brokerage == 'Webull':
            string_io = io.StringIO(value.decode("utf8"))
            self.data = af.preprocess_wb_orders(string_io)
        if value and brokerage == 'Charles Schwab':
            string_io = io.StringIO(value.decode("utf8"))
            self.data = af.preprocess_schwab_orders(string_io)
        else:
            print("error")

    @param.depends('data', watch=True)
    def get_df(self):
        self.df_pane.object = self.data

        trades = af.Stocks(self.data)
        trades.examine_trades()

        self.df_pane2.object = trades.trades_df
        self.total_gain.value = round(trades.total_gain)
        self.total_loss.value = round(trades.total_loss)
        self.wins.value = trades.win_count
        self.losses.value = trades.loss_count
        self.win_loss_ratio.value = round(trades.win_count/trades.loss_count, 2)

    def view(self):
        return pn.Column(
            "## Upload and process data",
            self.select_brokerage,
            self.file_input,
            pn.layout.Divider(),
            self.total_gain,
            self.total_loss,
            self.wins,
            self.losses,
            self.win_loss_ratio,
            self.df_pane,
            pn.Spacer(height = 500),
            self.df_pane2,
            name = "Analyze Trades"
        )

analyze_trades_view = Analyze_trades().view()



class ExamineCharts(param.Parameterized):

    file_input = param.Parameter()
    select_stock=pn.widgets.Select(name = 'Select Stock', options = [])
    select_brokerage=pn.widgets.Select(name = 'Select Brokerage', options = ['Webull', 'Robinhood', 'Charles Schwab'])
    select_interval=pn.widgets.Select(name = 'Select Time Interval', options = ['2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo'])
    select_export_type=pn.widgets.Select(name = 'Select Export Type', options = ['Stocks', 'Options'])
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
        else:
            print("error")

    @param.depends('data', watch = True)
    def refresh_symbols(self):
        self.select_stock.options = sorted(list(self.data.symbol.unique()))


    @param.depends('data', 'select_stock.value', 'start_date_input.value', 'end_date_input.value', 'select_interval.value', 'select_export_type.value', watch=True)
    def plotting(self):
        trades = af.Stocks(self.data)
        trades.examine_trades(export_type=self.select_export_type.value)

        if self.select_stock.value:
            self.candlestick_chart.object = tg.plot_buysell_points_candlestick(self.select_stock.value, tradesdf = trades.trades_df, start_date = self.start_date_input.value,
                                                    end_date= self.end_date_input.value, interval = self.select_interval.value)
            
            self.line_chart.object = tg.plot_buysell_points_line(self.select_stock.value, tradesdf = trades.trades_df, start_date = self.start_date_input.value,
                                                    end_date= self.end_date_input.value, interval = self.select_interval.value)

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



tabs = pn.Tabs(get_stock_info, analyze_trades_view, examine_charts_view)
tabs.show()
