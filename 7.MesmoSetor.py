#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 19:03:29 2019

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
def transport_tickers_save():
    tickers = ['TPIS3','JSLG3','GOLL4','LUXM4','RLOG3','TGMA3','LOGN3','ECOR3','CCRO3','STBP3','RAIL3']
    tickers.sort()
    with open ("transporte.pickle","wb") as f:
        pickle.dump(tickers,f)
        print(tickers,'ta dando certo mzra')
    
    return tickers
        
#save_B3_tickers()

def get_data_from_yahoo(reload_b3 = False):
    if reload_b3:
        tickers = transport_tickers_save()
    else:
        with open("transporte.pickle", "rb") as f:
            tickers = pickle.load(f)
    
    if not os.path.exists('transporte'):
        os.makedirs('transporte')
    
    start = dt.datetime(2011,4,1)
    end = dt.datetime(2019,12,27)
    
    for ticker in tickers:
        print(ticker)
        df = pd.DataFrame()
        if not os.path.exists('transporte/{}.csv'.format(ticker)):
            try:
                #tem que botar pra ele nao salvar os arquivos vazios
                df = web.DataReader(ticker + '.SA','yahoo',start,end)
            except:
                print('No data for {}'.format(ticker))
                
            df.to_csv('transporte/{}.csv'.format(ticker))
        else:
            print('Already have {}'.format(ticker))
            
def compile_data():
    with open("transporte.pickle","rb") as f:
        tickers = pickle.load(f)
        
    main_df = pd.DataFrame()
        
    for count, ticker in enumerate(tickers):
        try:
            df = pd.read_csv('transporte/{}.csv'.format(ticker))
            df.set_index('Date', inplace = True)
            df['ticker'] = ticker
        except:
            print('no data for {}'.format(ticker))
            continue
        #df.rename(columns = {'Adj Close':ticker}, inplace = True)
        #df.drop(['Open','High','Low','Close','Volume'],1,inplace = True)
        if main_df.empty:
            main_df = df
        else:
            #main_df = main_df.join(df,how = 'outer')
            main_df = main_df.append(df)
        if count % 10 == 0:
            print(count)
            
    print(main_df.head())
    main_df.to_csv('transporte.csv')

def get_data_from_advfn_fundamentals(reload_fund = False):
    web = ['ccr-on-CCRO3','ecorodovias-on-ECOR3','gol-pn-GOLL4','jsl-on-JSLG3','log-in-logistica-intermo-on-LOGN3','trevisa-pn-LUXM4','rumo-on-RAIL3','cosan-log-on-RLOG3','santos-brp-on-STBP3','tegma-on-TGMA3','triunfo-part-on-TPIS3']
    web = ['ccr-on-CCRO3']
    trimestres = ['/primeiro-trimestre','/segundo-trimestre','/terceiro-trimestre','/quarto-trimestre']
    
    with open("transporte.pickle","rb") as f:
        tickers = pickle.load(f) 
    #url = 'https://br.advfn.com/bolsa-de-valores/bovespa/triunfo-part-on-TPIS3/fundamentos/individualizado/2019/terceiro-trimestre'
    """
    https://br.advfn.com/bolsa-de-valores/bovespa/triunfo-part-on-TPIS3/fundamentos/individualizado/2019/primeiro-trimestre
    segue-se a ordem da url de cima, toma-se ela como exemplo
    """
    url1 = 'https://br.advfn.com/bolsa-de-valores/bovespa/'
    url2 = '/fundamentos/individualizado/'
    
    df = pd.read_csv('transporte.csv',index_col = 0)
    
    ano = 2011
    
    for name,ticker in zip(web,tickers):
        for i in range(9):
            for tri in trimestres:
                site = url1 + name + url2 + str(ano) + tri
                #print(site)
                print(ticker)
                resp = requests.get(site)
                
                dfs = pd.read_html(resp.text)
                if i == 0 and tri == '/primeiro-trimestre':
                    try:
                        valor_de_mercado = dfs[0].iloc[:,0:2]
                        resultados = dfs[1].iloc[:,0:2]
                        patrimonio = dfs[2].iloc[:,0:2]
                        caixa = dfs[3].iloc[:,0:2]
                        divida = dfs[4].iloc[:,0:2]
                        liquidezNsolvencia = dfs[5].iloc[:,0:2]
                        fluxo_de_caixa = dfs[6].iloc[:,0:2]
                        investimentos = dfs[7].iloc[:,0:2]
                        dividendos = dfs[8].iloc[:,0:2]
                    except:
                        print('end of data')
                else :
                    try:
                        valor_de_mercado = valor_de_mercado.append(dfs[0].iloc[:,1].values)
                        resultados = resultados.append(dfs[1].iloc[:,0:2])
                        patrimonio = patrimonio.append(dfs[2].iloc[:,0:2])
                        caixa = caixa.append(dfs[3].iloc[:,0:2])
                        divida = divida.append(dfs[4].iloc[:,0:2])
                        liquidezNsolvencia = liquidezNsolvencia.append(dfs[5].iloc[:,0:2])
                        fluxo_de_caixa = fluxo_de_caixa.append(dfs[6].iloc[:,0:2])
                        investimentos = investimentos.append(dfs[7].iloc[:,0:2])
                        dividendos = dividendos.append(dfs[8].iloc[:,0:2])
                    except:
                        print('end of data')
                
            ano = ano + 1
            
    
get_data_from_yahoo(reload_b3=True)
compile_data()
dataset = pd.read_csv('transporte.csv',index_col = 0)
