#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 08:52:00 2019

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
from sklearn import preprocessing
#First of all you need to find a site with the table list of the b3 companies
style.use('ggplot')
def tickers_func(sector):
    if sector == 'transporte':
        web = ['ccr-on-CCRO3','ecorodovias-on-ECOR3','gol-pn-GOLL4','jsl-on-JSLG3','log-in-logistica-intermo-on-LOGN3','trevisa-pn-LUXM4','santos-brp-on-STBP3','tegma-on-TGMA3','triunfo-part-on-TPIS3']
    elif sector == 'construção':
        web = ['cyrela-realt-on-CYRE3','even-on-EVEN3','eztec-on-EZTC3','gafisa-on-GFSA3','helbor-on-HBOR3','jhsf-part-on-JHSF3','mrv-on-MRVE3','tecnisa-on-TCSA3','tenda-on-TEND3','trisul-on-TRIS3']
    tickers = []
    for name in web:
        tickers.append(name[-5:])
    tickers.sort()
    print(tickers)
    with open ("{}.pickle".format(sector),"wb") as f:
        pickle.dump(tickers,f)
    
    return tickers,web
    
def tickers_save(sector):
    url = 'https://www.fundamentus.com.br/resultado.php?setor='
    if sector == 'construção':
        url = url + 13
    elif sector == 'transporte':
        url = url + 14
    resp = requests.get(url)
    dfs = pd.read_html(resp.text,index_col = 0)
    tickers = dfs[0].index.values
    tickers.sort()
    with open ("{}.pickle".format(sector),"wb") as f:
        pickle.dump(tickers,f)
    
    return tickers

def get_data_from_yahoo(sector,reload_b3 = False):
    if reload_b3:
        tickers = tickers_save(sector)
    else:
        with open("{}.pickle".format(sector), "rb") as f:
            tickers = pickle.load(f)
    
    if not os.path.exists(sector):
        os.makedirs(sector)
    
    start = dt.datetime(2011,4,1)
    end = dt.datetime(2019,12,30)
    
    for ticker in tickers:
        print(ticker)
        df = pd.DataFrame()
        if not os.path.exists('{}/{}.csv'.format(sector,ticker)):
            try:
                #tem que botar pra ele nao salvar os arquivos vazios
                #ticker = '^BVSP'
                df = web.DataReader(ticker + '.SA','yahoo',start,end)
            except:
                print('No data for {}'.format(ticker))
                
            df.to_csv('{}/{}.csv'.format(sector,ticker))
        else:
            print('Already have {}'.format(ticker))
   
def get_b3():
    start = dt.datetime(2011,4,1)
    end = dt.datetime(2019,12,30)
    df = pd.DataFrame()
    df = web.DataReader('EZTC3.SA','yahoo',start,end)
    
            
def compiled_dataframe(sector,save = False):
    tickers,web = tickers_func(sector)
    trimestres = ['/primeiro-trimestre','/segundo-trimestre','/terceiro-trimestre','/quarto-trimestre']
    
    #with open("{}.pickle".format(sector),"rb") as f:
    #    tickers = pickle.load(f) 
    
    #url = 'https://br.advfn.com/bolsa-de-valores/bovespa/triunfo-part-on-TPIS3/fundamentos/individualizado/2019/terceiro-trimestre'
    """
    https://br.advfn.com/bolsa-de-valores/bovespa/triunfo-part-on-TPIS3/fundamentos/individualizado/2019/primeiro-trimestre
    segue-se a ordem da url de cima, toma-se ela como exemplo
    """
    url1 = 'https://br.advfn.com/bolsa-de-valores/bovespa/'
    url2 = '/fundamentos/individualizado/'
    
    #df = pd.read_csv('transporte.csv',index_col = 0)
    #dataset_final = pd.DataFrame()
    #name = 'rumo-on-RAIL3'
    main_df = pd.DataFrame()
    #ticker = 'RAIL3'
    #tickers = ['CCRO3']
    #web =  ['ccr-on-CCRO3']
    for ticker, name in zip(tickers,web):
        try:
            df = pd.read_csv('{}/{}.csv'.format(sector,ticker),index_col=0)
            df.index = pd.to_datetime(df.index,yearfirst = True)
            df[df == 0] = np.nan
            df = df.resample("d").fillna(method = 'ffill')
            df.fillna(method = 'ffill',inplace = True)
            
            df['Qtr'] = (df.index.month - 1)//3 + 1
            #df.set_index('Date', inplace = True)
            #df1 = pd.Index(['ULTIMO'])
            #df = df.append(pd.DataFrame(index = df1))
            
            df['Close'] = df['Close'].shift(1)
            df['Adj Close'] = df['Adj Close'].shift(1)
            df['Volume'] = df['Volume'].shift(1)
            df['Open'] = df['Open'].shift(1)
            df['High'] = df['High'].shift(1)
            df['Low'] = df['Low'].shift(1)
            df['ticker'] = ticker
            df['180d'] = (df['Close'].shift(-180) - df['Close'])/df['Close']
            
            ano = 2011
            for i in range(9):
                for tri in trimestres:
                    site = url1 + name + url2 + str(ano) + tri
                    #print(site)
                    print(ticker, tri,ano,site)
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
                            print('PRIMEIRO STOP POINT')
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
                            print('SEGUNDO')
                    
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
                    result = str(int(time[3:7]) + 1) + '-01-01'
                dataset_final = dataset_final.rename(index = {time:result})
            new = '2019-12-30'
            dataset_final.loc[new] = dataset_final.loc[result]
                    
            """
comentário sobre essa parte que pode ser um tanto confusa, pelo menos pra mim enquanto programo e tento perce
ber a lógica dos dados. Antes estava a data do que corresponderia ao lançamento dos novos dados trimestrais isto
é, do trimestre seguinte. Ou seja. o primeiro trimestre estaria como 04-01.
Contudo, ao usarmos o ffill ele preenche tudo com o mais na frente
 ex:-
    -
    -3
nesse caso tudo seria preenchido com 3. Assim, como queremos usar esses dados na previsão vamos alterar
de forma que o trimestre utilize os dados do balanço do trimestre anterior.
Na prática é mais intuitivo.
            """
                
            dataset_final.index = pd.to_datetime(dataset_final.index,yearfirst = True)
            dataset_final[dataset_final == 0] = np.nan
            dataset_final = dataset_final.resample("d").fillna(method = 'ffill')
            dataset_final.fillna(method = 'ffill',inplace = True)
        except:
            print('terceiro {}'.format(ticker))
            continue
        #df.rename(columns = {'Adj Close':ticker}, inplace = True)
        #df.drop(['Open','High','Low','Close','Volume'],1,inplace = True)
        if main_df.empty:
            main_df = df
            main_df = main_df.join(dataset_final)
        else:
            #main_df = main_df.join(df,how = 'outer')
            df = df.join(dataset_final)
            main_df = main_df.append(df)
    if save == True:
        main_df.to_csv('{}.csv'.format(sector))
    return main_df

           
def daily_Compiled_dataframe(sector,save = False):
    #ticker = 'HBOR3'
    #name = 'helbor-on-HBOR3'
    #sector = 'construção'
    #save = True
    
    tickers,web = tickers_func(sector)
    trimestres = ['/primeiro-trimestre','/segundo-trimestre','/terceiro-trimestre','/quarto-trimestre']
   
    #url = 'https://br.advfn.com/bolsa-de-valores/bovespa/triunfo-part-on-TPIS3/fundamentos/individualizado/2019/terceiro-trimestre'
    """
    https://br.advfn.com/bolsa-de-valores/bovespa/triunfo-part-on-TPIS3/fundamentos/individualizado/2019/primeiro-trimestre
    segue-se a ordem da url de cima, toma-se ela como exemplo
    """
    url1 = 'https://br.advfn.com/bolsa-de-valores/bovespa/'
    url2 = '/fundamentos/individualizado/'
    
    main_df = pd.DataFrame()
    ibov = pd.read_csv("^BVSP.csv".format(sector),index_col = 0)
    ibov.index = pd.to_datetime(ibov.index,yearfirst = True)
    ibov[ibov == 0] = np.nan
    ibov = ibov.resample("d").fillna(method = 'ffill')
    ibov.fillna(method = 'ffill',inplace = True)
    ibov['ibov'] = ibov['Close']
    ibov = ibov.drop(columns =ibov.columns[0:6])
    
    #name = 'eztec-on-EZTC3'
    for ticker, name in zip(tickers,web):
        #sector = 'construção'
        #ticker = 'EZTC3'
        df = pd.read_csv('{}/{}.csv'.format(sector,ticker),index_col=0)
        df.index = pd.to_datetime(df.index,yearfirst = True)
        df[df == 0] = np.nan
        df = df.resample("d").fillna(method = 'ffill')
        df.fillna(method = 'ffill',inplace = True)
        
        df['Qtr'] = (df.index.month - 1)//3 + 1
        #df.set_index('Date', inplace = True)
        #df1 = pd.Index(['ULTIMO'])
        #df = df.append(pd.DataFrame(index = df1))
        
        df['Close'] = df['Close'].shift(1)
        df['Adj Close'] = df['Adj Close'].shift(1)
        df['Volume'] = df['Volume'].shift(1)
        df['Open'] = df['Open'].shift(1)
        df['High'] = df['High'].shift(1)
        df['Low'] = df['Low'].shift(1)
        df['previous Close'] = df['Close'].shift(1)
        df['ticker'] = ticker
        df['180d'] = df['Close'].shift(-180)
        df['var 180d'] = (df['Close'].shift(-180) - df['Close'])/df['Close']
        df['30d'] = df['Close'].shift(-30)
        
        
        ano = 2011
        for i in range(9):
            for tri in trimestres:
                site = url1 + name + url2 + str(ano) + tri
                #print(site)
                print(ticker, tri,ano,site)
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
                        print('PRIMEIRO STOP POINT')
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
                        print('SEGUNDO')
                
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
                result = str(int(time[3:7]) + 1) + '-01-01'
            dataset_final = dataset_final.rename(index = {time:result})
        new = '2019-12-30'
        dataset_final.loc[new] = dataset_final.loc[result]
                
        
        
        """
comentário sobre essa parte que pode ser um tanto confusa, pelo menos pra mim enquanto programo e tento perce
ber a lógica dos dados. Antes estava a data do que corresponderia ao lançamento dos novos dados trimestrais isto
é, do trimestre seguinte. Ou seja. o primeiro trimestre estaria como 04-01.
Contudo, ao usarmos o ffill ele preenche tudo com o mais na frente
 ex:-
-
-3
nesse caso tudo seria preenchido com 3. Assim, como queremos usar esses dados na previsão vamos alterar
de forma que o trimestre utilize os dados do balanço do trimestre anterior.
Na prática é mais intuitivo.
        """
            
        dataset_final.index = pd.to_datetime(dataset_final.index,yearfirst = True)
        dataset_final[dataset_final == 0] = np.nan
        dataset_final = dataset_final.resample("d").fillna(method = 'ffill')
        dataset_final.fillna(method = 'ffill',inplace = True)
        dataset_final = dataset_final.join(ibov.shift(1))
    
        #print('terceiro\noooooo\n\ ooooodaidahjd\n diadiahjdi\n terceirooosoaosoasoaos {}'.format(ticker))
        #continue
        #df.rename(columns = {'Adj Close':ticker}, inplace = True)
        #df.drop(['Open','High','Low','Close','Volume'],1,inplace = True)
        if main_df.empty:
            main_df = df
            main_df = main_df.join(dataset_final)
        else:
            #main_df = main_df.join(df,how = 'outer')
            df = df.join(dataset_final)
            main_df = main_df.append(df)
    if save == True:
        main_df.to_csv('{}_daily.csv'.format(sector))
    return main_df
   
def daily_preprocessed_dataframe(sector = 'construção'):
    dataset = pd.read_csv("{}_daily.csv".format(sector),index_col = 0 , low_memory = False)
    dataset.drop_duplicates(inplace = True)
    dataset = dataset.dropna(axis=0,subset = dataset.columns[0:4]) # tira adj close close high e open que for 0
    for column in dataset.columns[12:73]: #ajeita as string e converte pra float
        dataset[column] = dataset[column].astype(str).str.replace(".","").str.replace("%","").str.replace(",",".").str.replace("N/D","0").astype(float)
        
    #dataset['ticker'] = dataset['ticker'].astype(str)
    dataset = dataset.reset_index()
    index = dataset['Date']
    dataset.drop(columns = ['Date'],inplace = True)
    #encoder = LabelEncoder()
    #dataset['ticker'] = (pd.DataFrame(encoder.fit_transform(dataset['ticker'])))
    dez = ['Fluxo de Caixa de Financiamentos (FCF)']
    cem = ['Price Sales Ratio (PSR)','Preço / EBIT','Lucro/Prejuízo Líquido','Preço / Lucro (P/L)','Lucro por Ação (LPA)','Preço / Ativo (P/A)','Giro Ativos','EBIT / Ativo','Valor Patrimonial por Ação (VPA)','Preço / Valor Patrimonial por Ação (P/VPA)','Equity Multiplier (EM)','Dívida Bruta / Patrimônio Líquido','Dívida Líquida / EBITDA','Enterprise Value / EBIT (EV/EBIT)','Preço / Ativo Circulante Líquido','Preço / Capital de Giro',]
    mil = ['Liquidez Corrente','Liquidez Imediata']
    
    for obj in dez:
        dataset[obj] = dataset[obj]/10
    for obj in cem:
        dataset[obj] = dataset[obj]/100
    for obj in mil:
        dataset[obj] = dataset[obj]/1000
    
    encoder = preprocessing.LabelEncoder()
    dataset['ticker'] = encoder.fit_transform(dataset['ticker'])
    dummy = pd.get_dummies(dataset['ticker'])
    dummy.columns,trash = tickers_func(sector)
    dataset = dataset.drop(columns = ['ticker'])
    dataset = dataset.join(dummy.drop(columns = [dummy.columns[0]]))
    dataset.set_index(index,inplace = True)
    
    prediction = dataset.loc[dataset['180d'].isnull()== True]
    train_test = dataset.loc[dataset['180d'].isnull()== False]
    prediction.fillna(0,inplace = True)
    train_test.fillna(0,inplace = True)
    
    return train_test,prediction

def preprocessed_dataframe(sector):
    dataset = pd.read_csv("{}.csv".format(sector),index_col = 0 , low_memory = False)
    dataset.drop_duplicates(inplace = True)
    dataset = dataset.dropna(axis=0,subset = dataset.columns[0:4]) # tira adj close close high e open que for 0
    for column in dataset.columns[9:69]: #ajeita as string e converte pra float
        dataset[column] = dataset[column].astype(str).str.replace(".","").str.replace("%","").str.replace(",",".").str.replace("N/D","0").astype(float)
        
    #dataset['ticker'] = dataset['ticker'].astype(str)
    dataset = dataset.reset_index()
    index = dataset['Date']
    dataset.drop(columns = ['Date'],inplace = True)
    #encoder = LabelEncoder()
    #dataset['ticker'] = (pd.DataFrame(encoder.fit_transform(dataset['ticker'])))
    dez = ['Fluxo de Caixa de Financiamentos (FCF)']
    cem = ['Price Sales Ratio (PSR)','Preço / EBIT','Lucro/Prejuízo Líquido','Preço / Lucro (P/L)','Lucro por Ação (LPA)','Preço / Ativo (P/A)','Giro Ativos','EBIT / Ativo','Valor Patrimonial por Ação (VPA)','Preço / Valor Patrimonial por Ação (P/VPA)','Equity Multiplier (EM)','Dívida Bruta / Patrimônio Líquido','Dívida Líquida / EBITDA','Enterprise Value / EBIT (EV/EBIT)','Preço / Ativo Circulante Líquido','Preço / Capital de Giro',]
    mil = ['Liquidez Corrente','Liquidez Imediata']
    
    for obj in dez:
        dataset[obj] = dataset[obj]/10
    for obj in cem:
        dataset[obj] = dataset[obj]/100
    for obj in mil:
        dataset[obj] = dataset[obj]/1000
    
    encoder = preprocessing.LabelEncoder()
    dataset['ticker'] = encoder.fit_transform(dataset['ticker'])
    dummy = pd.get_dummies(dataset['ticker'])
    dummy.columns,trash = tickers_func(sector)
    dataset = dataset.drop(columns = ['ticker'])
    dataset = dataset.join(dummy.drop(columns = [dummy.columns[0]]))
    dataset.set_index(index,inplace = True)
    
    prediction = dataset.loc[dataset['180d'].isnull()== True]
    train_test = dataset.loc[dataset['180d'].isnull()== False]
    prediction.fillna(0,inplace = True)
    train_test.fillna(0,inplace = True)
    """
    Nao funciona pelo tamanho
    ohe = preprocessing.OneHotEncoder(categorical_features = [7])
    dataset = ohe.fit_transform(dataset).toarray()
    """
    
    return train_test,prediction
        
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
#df[df['ticker'] == ticker] = df.join(dataset_final) 
#df = df.join(dataset_final) 

                
#get_data_from_yahoo(sector = 'construção')
#transport_tickers_save()
#df = compiled_dataframe('construção')
#train_test,prediction = preprocessed_dataframe('construção')