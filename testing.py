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
import numpy as np
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
    #ticker = 'CCRO3'
    for count, ticker in enumerate(tickers):
        try:
            df = pd.read_csv('transporte/{}.csv'.format(ticker),index_col=0)
            df.index = pd.to_datetime(df.index,yearfirst = True)
            df[df == 0] = np.nan
            df = df.resample("d").fillna(method = 'ffill')
            df.fillna(method = 'ffill',inplace = True)
            
            df['Qtr'] = (df.index.month - 1)//3 + 1
            #df.set_index('Date', inplace = True)
            df['ticker'] = ticker
            df['90d'.format(ticker)] = (df['Adj Close'].shift(-91) - df['Adj Close'])/df['Adj Close']
        
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
    #dataset_final = pd.DataFrame()
    ano = 2011
    
    for name,ticker in zip(web,tickers):
        for i in range(9):
            for tri in trimestres:
                site = url1 + name + url2 + str(ano) + tri
                #print(site)
                print(ticker, tri)
                resp = requests.get(site)
                
                dfs = pd.read_html(resp.text)
                if i == 0 and tri == '/primeiro-trimestre':
                    try:
                        valor_de_mercado = dfs[0].iloc[:,0:2].T
                        resultados = dfs[1].iloc[:,0:2].T
                        patrimonio = dfs[2].iloc[:,0:2].T
                        caixa = dfs[3].iloc[:,0:2].T
                        divida = dfs[4].iloc[:,0:2].T
                        liquidezNsolvencia = dfs[5].iloc[:,0:2].T
                        fluxo_de_caixa = dfs[6].iloc[:,0:2].T
                        investimentos = dfs[7].iloc[:,0:2].T
                        dividendos = dfs[8].iloc[:,0:2].T
                    except:
                        print('end of data')
                else :
                    try:
                        valor_de_mercado = valor_de_mercado.append(dfs[0].iloc[:,1].T)
                        resultados = resultados.append(dfs[1].iloc[:,1].T)
                        patrimonio = patrimonio.append(dfs[2].iloc[:,1].T)
                        caixa = caixa.append(dfs[3].iloc[:,1].T)
                        divida = divida.append(dfs[4].iloc[:,1].T)
                        liquidezNsolvencia = liquidezNsolvencia.append(dfs[5].iloc[:,1].T)
                        fluxo_de_caixa = fluxo_de_caixa.append(dfs[6].iloc[:,1].T)
                        investimentos = investimentos.append(dfs[7].iloc[:,1].T)
                        dividendos = dividendos.append(dfs[8].iloc[:,1].T)
                    except:
                        print('end of data')
                
            ano = ano + 1
        valor_de_mercado.columns = valor_de_mercado.iloc[0,:]
        valor_de_mercado.drop('Unnamed: 0', inplace = True)
        valor_de_mercado.drop(columns = ['Última Cotação ON','Última Cotação PN'], inplace = True)
        valor_de_mercado.drop(1, inplace = True)
        resultados.columns = resultados.iloc[0,:]
        resultados.drop('Unnamed: 0', inplace = True)
        patrimonio.columns = patrimonio.iloc[0,:]
        patrimonio.drop('Unnamed: 0', inplace = True)
        caixa.columns = caixa.iloc[0,:]
        caixa.drop('Unnamed: 0', inplace = True)
        divida.columns = divida.iloc[0,:]
        divida.drop('Unnamed: 0', inplace = True)
        liquidezNsolvencia.columns =liquidezNsolvencia.iloc[0,:]
        liquidezNsolvencia.drop('Unnamed: 0', inplace = True)
        fluxo_de_caixa.columns = fluxo_de_caixa.iloc[0,:]
        fluxo_de_caixa.drop('Unnamed: 0', inplace = True)
        investimentos.columns = investimentos.iloc[0,:]
        investimentos.drop('Unnamed: 0', inplace = True)
        dividendos.columns = dividendos.iloc[0,:]
        dividendos.drop('Unnamed: 0', inplace = True)
        dataset_final = valor_de_mercado
        dataset_final = dataset_final.join(resultados).join(patrimonio).join(caixa)
        dataset_final = dataset_final.join(divida).join(liquidezNsolvencia).join(fluxo_de_caixa)
        dataset_final = dataset_final.join(investimentos).join(dividendos)
        
        for time in dataset_final.index:
            result = ""
            result = time[3:7]
            if time[0:1] == '1':
                result = result + '-04-01' 
            elif time[0:1] == '2':
                result = result + '-07-01'
            elif time[0:1] == '3':
                result = result + '-10-01'
            elif time[0:1] == '4':
                result = result + '-01-01'
            dataset_final = dataset_final.rename(index = {time:result})
        dataset_final.index = pd.to_datetime(dataset_final.index,yearfirst = True)
        dataset_final[dataset_final == 0] = np.nan
        dataset_final = dataset_final.resample("d").fillna(method = 'ffill')
        dataset_final.fillna(method = 'ffill',inplace = True)
        
        # qtr é 2 mas eu quero colocar o primeiro
        """
        for qtr , year in zip(df['Qtr'], df.index):
            for date,tic in zip(dataset_final.index,tickers):
                print(qtr , year ,"-------", date , tic)
                #try:#if find(str(qtr - 1),date[0:1]) != -1 and find(pd.to_datetime(year).year,date[2:7]) != -1:
                #df[tic == ticker and str(qtr + 1) == date[0:1] and pd.to_datetime(year).year == pd.to_datetime(date[3:7]).year] = df.join(dataset_final.loc[[str(date)]])
                mask = tic == ticker and str(qtr + 1) == date[0:1] and pd.to_datetime(year).year == pd.to_datetime(date[3:7]).year 
                df = (df.append(pd.DataFrame(dataset_final.loc[dataset_final.index == date,['Giro Ativos']])).values)               
        """
        df[df['ticker'] == ticker] = df.join(dataset_final) 
        #df = df.join(dataset_final) 
        """
        junta tudo logo e deixa pra juntar mermo no final .... será???
        """
                
#get_data_from_yahoo(reload_b3=True)
compile_data()
dataset = pd.read_csv('transporte.csv',index_col = 0)

