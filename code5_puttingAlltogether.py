#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 14:12:02 2019

@author: itamar
"""

import bs4 as bs
import pickle
import datetime as dt
import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib import style
import pandas_datareader as web
import requests
#First of all you need to find a site with the table list of the b3 companies
style.use('ggplot')

def save_B3_tickers():
    tickers = []
    for i in range (24):
        site = 'https://br.advfn.com/bolsa-de-valores/bovespa/'
        site = site + chr(ord('A')+i)
        resp = requests.get(site)
        soup = bs.BeautifulSoup(resp.text,'lxml')
        table = soup.find('table',{'class':'atoz-link-bov'})
        for row in table.findAll('tr')[1:]:
            ticker = row.findAll('td')[1].text
            
            if not ticker.endswith('L') and not ticker.endswith('B') and not len(ticker) > 6:
                print(ticker)
                tickers.append(ticker)
                
    with open ("bovtickers.pickle","wb") as f:
        pickle.dump(tickers,f)
        print(tickers)
    
    return tickers

def get_data_from_yahoo(reload_b3 = False):
    real_tickers = []
    if reload_b3:
        tickers = save_B3_tickers()
    else:
        with open("bovtickers.pickle", "rb") as f:
            tickers = pickle.load(f)
    
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')
    
    start = dt.datetime(2000,1,1)
    end = dt.datetime(2019,12,22)
    
    for ticker in tickers:
        print(ticker)
        df = pd.DataFrame()
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            try:
                #tem que botar pra ele nao salvar os arquivos vazios
                print('tentativas ', ticker)
                df = web.DataReader(ticker + '.SA','yahoo',start,end)
                real_tickers.append(ticker)
            except:
                print('No data for {}'.format(ticker))
                
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))
        
    with open ("bovtickers.pickle","wb") as f:
        pickle.dump(real_tickers,f)
        
        
def compile_data():
    with open("bovtickers.pickle","rb") as f:
        tickers = pickle.load(f)
        
    main_df = pd.DataFrame()
        
    for count, ticker in enumerate(tickers):
        try:
            df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
            df.set_index('Date', inplace = True)
        except:
            print('no data for {}'.format(ticker))
            continue
        df.rename(columns = {'Adj Close':ticker}, inplace = True)
        df.drop(['Open','High','Low','Close','Volume'],1,inplace = True)
        
        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df,how = 'outer')
            
        if count % 10 == 0:
            print(count)
            
    print(main_df.head())
    main_df.to_csv('bovespa.csv')

get_data_from_yahoo(reload_b3=True)
compile_data()
dataset = pd.read_csv('bovespa.csv',index_col = 0)
