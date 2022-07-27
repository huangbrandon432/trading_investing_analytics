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
importlib.reload(am)
importlib.reload(tg)
importlib.reload(af)


pn.extension()

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
dash

tabs = pn.Tabs(('Get Info', dash))
tabs.show()
