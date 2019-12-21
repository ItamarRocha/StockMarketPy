#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 10:32:13 2019

@author: itamar
"""

import bs4 as bs
import pickle
import datetime as dt
import pandas as pd
import os
import pandas_datareader as web
import requests
#First of all you need to find a site with the table list of the b3 companies

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
            
            if not ticker.endswith('L') and not ticker.endswith('B'):
                print(ticker)
                tickers.append(ticker)
                
    with open ("bovtickers.pickle","wb") as f:
        pickle.dump(tickers,f)
        print(tickers,'ta dando certo mzra')
    
    return tickers
        
#save_B3_tickers()

def get_data_from_yahoo(reload_b3 = False):
    if reload_b3:
        save_B3_tickers()
    else:
        with open("bovtickers.pickle", "rb") as f:
            tickers = pickle.load(f)
    
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')
    
    start = dt.datetime(2000,1,1)
    end = dt.datetime(2019,12,15)
    
    for ticker in tickers:
        print(ticker)
        df = pd.DataFrame()
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            try:
                df = web.DataReader(ticker + '.SA','yahoo',start,end)
            except:
                print('No data for {}'.format(ticker))
                
            df.to_csv('stock_dfs/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))
            
get_data_from_yahoo()