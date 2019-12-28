#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 19:35:13 2019

@author: itamar
"""
"""
Próximos passos : adicionar todos os dias do ano
de forma que de pra manipular os trimestres de forma exata
depois adicionar os dados fundamentalistas
testar metodos com todos os dias e com apenas alguns
"""
import numpy as np
import pandas as pd
import pickle
from collections import Counter
from sklearn.model_selection import cross_validate
from sklearn import svm, neighbors
from sklearn.ensemble import RandomForestClassifier, VotingClassifier

def get_data_from_advfn_fundamentals(reload_fund = False):
    web = ['ccr-on-CCRO3','ecorodovias-on-ECOR3','gol-pn-GOLL4','jsl-on-JSLG3','log-in-logistica-intermo-on-LOGN3','trevisa-pn-LUXM4','rumo-on-RAIL3','cosan-log-on-RLOG3','santos-brp-on-STBP3','tegma-on-TGMA3','triunfo-part-on-TPIS3']
    
    trimestres = ['/quarto-trimestre','/terceiro-trimestre','/segundo-trimestre','/primeiro-trimestre']
    #url = 'https://br.advfn.com/bolsa-de-valores/bovespa/triunfo-part-on-TPIS3/fundamentos/individualizado/2019/terceiro-trimestre'
    """
    
    https://br.advfn.com/bolsa-de-valores/bovespa/triunfo-part-on-TPIS3/fundamentos/individualizado/2019/primeiro-trimestre
    segue-se a ordem da url de cima, toma-se ela como exemplo
    """
    url1 = 'https://br.advfn.com/bolsa-de-valores/bovespa/'
    url2 = '/fundamentos/individualizado/'
    
    
    with open("transporte.pickle", "rb") as f:
        tickers = pickle.load(f)
    
    for ticker in tickers:
        df = pd.read_csv('stock_dfs/{}.csv'.format(ticker),index_col = 0)
        print(ticker)
    ano = 2019
    
    for name in web:
        for i in range(18):
            for tri in trimestres:
                site = url1 + name + url2 + str(ano) + tri
                print(site)
                
                resp = requests.get(site)
                
                dfs = pd.read_html(resp.text)
                try:
                    valor_de_mercado = dfs[0]
                    resultados = dfs[1]
                    patrimonio = dfs[2]
                    caixa = dfs[3]
                    divida = dfs[4]
                    liquidezNsolvencia = dfs[5]
                    fluxo_de_caixa = dfs[6]
                    investimentos = dfs[7]
                    dividendos = dfs[8]
                except:
                    print('end of data')
                
                
            ano = ano - 1
            
    
df = pd.read_csv('transporte.csv',index_col = 0)
df.index = pd.to_datetime(df.index,yearfirst = True)
df[df == 0] = np.nan
df = df.resample("d").fillna(method = 'ffill')
df.fillna(method = 'ffill',inplace = True)

tickers = df.columns.values.tolist()
tickers.pop(0)

for ticker in tickers:
    df['{}_90d'.format(ticker)] = (df[ticker].shift(-91) - df[ticker])/df[ticker]

df['Qtr'] = (df.index.month - 1)//3 + 1
