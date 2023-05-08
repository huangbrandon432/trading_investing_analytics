import panel as pn
from panel.interact import interact, interactive, fixed, interact_manual
from panel import widgets
import pandas as pd
import numpy as np
import tickers_graphing_module as tg
import analysis_module as am
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

button = pn.widgets.Button(name='Get Ticker Stats and Financials', button_type='primary')
text = pn.widgets.TextInput(name = 'Ticker', value='TSLA')
def b(event):
    af.get_share_stats_and_financials(text.value)


button2 = pn.widgets.Button(name='Swaggy Stocks', button_type='primary')
def c(event):
    af.swaggy_stocks()


button3 = pn.widgets.Button(name='Get Options Chain', button_type='primary')
text3 = pn.widgets.TextInput(name = 'Options Chain Ticker', value='TSLA')
def d(event):
    af.get_options_chain(text3.value)


button4 = pn.widgets.Button(name='Top Shorted Stocks', button_type='primary')
def e(event):
    af.get_top_shorted_stocks()



button.on_click(b)
button2.on_click(c)
button3.on_click(d)
button4.on_click(e)
actions = pn.Column(text, button, pn.Spacer(height = 5), button2, pn.Spacer(height = 5), text3, button3, pn.Spacer(height = 5), button4, name = 'Get Info')




class Charts(param.Parameterized):

    ticker = param.String(default="TSLA", doc="Ticker symbol")

    start_date = param.String(default="2021-01-01", doc="Start Date")

    end_date = param.String(default="2022-12-31", doc="End Date")

    moving_average = param.ObjectSelector(default="yes", objects=["yes", "no"])

    moving_average_days = param.Integer(10, bounds=(1, 365))

    @param.depends('ticker', 'start_date', 'end_date', 'moving_average', 'moving_average_days')
    def linechart(self):
        return pn.panel(tg.line_chart(self.ticker, start = self.start_date, end = self.end_date, moving_avg = self.moving_average, moving_avg_days = self.moving_average_days))

    def candlestick(self):
        return pn.panel(tg.candlestick_chart(self.ticker, start = self.start_date, end = self.end_date, moving_avg = self.moving_average, moving_avg_days = self.moving_average_days))


charts_class = Charts(name='Line, Candlestick Charts, and Info')

charts_and_info = pn.Column(charts_class.param, charts_class.linechart, charts_class.candlestick, name = 'Charts and Info')



class Analyze_trades(param.Parameterized):


    file_input = param.Parameter()
    data = param.DataFrame()

    def __init__(self, **params):
        super().__init__(file_input=pn.widgets.FileInput(accept='.csv,.xlsx,.xls'), **params)
        self.df_pane = pn.pane.DataFrame(width=1000, max_rows = 10)
        self.df_pane2 = pn.pane.DataFrame(width=1000, max_rows = 10)
        self.total_gain = pn.indicators.Number(name='Total Realized Gain', format='${value}', font_size = '30pt')
        self.total_loss = pn.indicators.Number(name='Total Realized Loss', format='${value}', font_size = '30pt')

    @param.depends("file_input.value", watch=True)
    def parse_file_input(self):
        value = self.file_input.value
        if value:
            string_io = io.StringIO(value.decode("utf8"))
            self.data = af.preprocess_rh_stock_orders(string_io)

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

    def view(self):
        return pn.Column(
            "## Upload and process data",

            self.file_input,
            pn.layout.Divider(),
            self.total_gain,
            self.total_loss,
            self.df_pane,
            pn.Spacer(height = 500),
            self.df_pane2,
            name = "Analyze Trades"
        )

analyze_trades_view = Analyze_trades().view()



class ExamineCharts(param.Parameterized):

    file_input = param.Parameter()
    select_stock=pn.widgets.Select(name = 'Select Stock', options = [])
    select_brokerage=pn.widgets.Select(name = 'Select Brokerage', options = ['Webull', 'Robinhood'])
    data = param.DataFrame()
    chart = pn.pane.Plotly()
    chart2 = pn.pane.Plotly()
    start_date_input = pn.widgets.TextInput(name='Optional Start Date', placeholder='Enter start date (optional)')
    end_date_input = pn.widgets.TextInput(name='Optional End Date', placeholder='Enter end date (optional)')

    def __init__(self, **params):
        super().__init__(file_input=pn.widgets.FileInput(accept='.csv,.xlsx,.xls'), **params)


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

        else:
            print("error")

    @param.depends('data', watch = True)
    def refresh_symbols(self):
        self.select_stock.options = sorted(list(self.data.symbol.unique()))


    @param.depends('data', 'select_stock.value', 'start_date_input.value', 'end_date_input.value', watch = True)
    def plotting(self):
        trades = af.Stocks(self.data)
        trades.examine_trades()

        if self.select_stock.value:
            self.chart.object = tg.plot_buysell_points_line(self.select_stock.value, tradesdf = trades.trades_df, start_date = self.start_date_input.value,
                                                      end_date= self.end_date_input.value)

            self.chart2.object = tg.plot_buysell_points_candlestick(self.select_stock.value, tradesdf = trades.trades_df, start_date = self.start_date_input.value,
                                                      end_date= self.end_date_input.value)
        else:
            print('select stock')


    def view(self):
        return pn.Column(
            "## Examine Charts",
            self.select_brokerage,
            self.file_input,
            self.select_stock,
            self.start_date_input,
            self.end_date_input,
            pn.layout.Divider(),
            self.chart2,
            pn.Spacer(height = 150),
            self.chart,
            name = "Examine Charts"
        )

examine_charts_view = ExamineCharts().view()



tabs = pn.Tabs(actions, charts_and_info, analyze_trades_view, examine_charts_view)
tabs.show()
