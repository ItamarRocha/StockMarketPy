#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 20:13:03 2019

@author: itamar
"""

import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import pandas as pd
import pandas_datareader.data as web

# site pra pegar os tickers das acoes do ibov https://finance.yahoo.com/quote/JSLG3.SA?p=JSLG3.SA&.tsrc=fin-srch
bov = web.DataReader('XPML13.SA','yahoo',dt.datetime(2019,1,1),dt.datetime(2019,12,15))

bov['100ma'] = bov['Adj Close'].rolling(window = 100, min_periods = 0).mean()

ax1 = plt.subplot2grid((6,1),(0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1),(5,0), rowspan=1, colspan=1,sharex = ax1)

ax1.plot(bov.index,bov['Adj Close'])
ax1.plot(bov.index,bov['100ma'])
ax2.bar(bov.index,bov['Volume'])

plt.show()
bov.tail()
