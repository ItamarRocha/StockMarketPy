#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 21:35:34 2020

@author: itamar
"""


import pandas as pd
from fbprophet import Prophet


df = pd.read_csv("stock_dfs/JSLG3.csv")

df.info()

df.isnull().sum()

df.Date = pd.to_datetime(df.Date)

df = df.set_index('Date').sort_index()

vol = df['Volume']

df = df['Close']

"""
#plotar anual
fig,ax = plt.subplots(figsize = (10,5))
df.plot(ax=ax)
plt.show()

# plotar gráfico semanal
fig, ax = plt.subplots(figsize=(10,5))
vol.plot(ax=ax)
plt.show()
"""

df = df.reset_index().rename(columns = {'Date': 'ds','Close': 'y'})

#Forecasting
model = Prophet()
model.add_country_holidays(country_name= 'BR')
model.fit(df)

future = model.make_future_dataframe(periods = 365)
forecast = model.predict(future)

model.plot(forecast,xlabel = 'Date',ylabel = 'Close')

model.plot_components(forecast);
