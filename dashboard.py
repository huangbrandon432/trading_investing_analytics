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
import param
importlib.reload(am)
importlib.reload(tg)
importlib.reload(af)


pn.extension('plotly')

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
dash = pn.Column(text, button, pn.Spacer(height = 5), button2, pn.Spacer(height = 5), text3, button3, pn.Spacer(height = 5), button4)



# plotly_pane = pn.panel(tg.line_chart('ETH-USD', start = '2021-5-1', end = '2021-12-31', moving_avg = 'no', moving_avg_days = 7), name = 'Line Chart')

class LineChart(param.Parameterized):

    ticker = param.String(default="TSLA", doc="Ticker symbol")

    start_date = param.String(default="2021-01-01", doc="Start Date")

    end_date = param.String(default="2022-12-31", doc="End Date")

    moving_average = param.ObjectSelector(default="yes", objects=["yes", "no"])

    moving_average_days = param.Integer(10, bounds=(1, 365))

    @param.depends('ticker', 'start_date', 'end_date', 'moving_average', 'moving_average_days')
    def view(self):
        return pn.panel(tg.line_chart(self.ticker, start = self.start_date, end = self.end_date, moving_avg = self.moving_average, moving_avg_days = self.moving_average_days))

line_chart = LineChart(name='Line Chart')

charts = pn.Column(line_chart.param, line_chart.view, name = 'Charts')

tabs = pn.Tabs(('Get Info', dash), charts)


tabs.show()
