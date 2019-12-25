#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 20:53:23 2019

@author: itamar
"""
import requests
import bs4 as bs
import pickle
import pandas as pd
#url = 'https://www.fundamentus.com.br/resultado.php?setor=27'
url = 'https://br.advfn.com/bolsa-de-valores/bovespa/jslg-on-JSLG3/fundamentos/individualizado/2019/primeiro-trimestre'
resp = requests.get(url)
#print(resp.text)

#soup = bs.BeautifulSoup(resp.text,'lxml')

#print(soup)

# pra conseguir todos os links
#for url in soup.find_all('a'):
#    print(url.get('href')) 

#nav = soup.nav
#for url in nav.find_all('a'):
#    print(url.get('href'))

#body = soup.body
#for paragraph in body.find_all('p'):
#    print(paragraph.text)

#for div in soup.find_all('div',class_ = 'center'):
#    print(div.text)

#for div in soup.find_all('table'):
#    print(div.text)

"""
th -> table header
tr -> table row
td -> table data
"""
#table = soup.table
""" # best method yet
table = soup.find('table')
print(table)

table_rows = table.find_all('tr')

for tr in table_rows:
    td = tr.find_all('td')
    row = [i.text for i in td]
    print(row)

#bom pra pegar tabela do fundamentus
dfs = pd.read_html('https://br.advfn.com/bolsa-de-valores/bovespa/triunfo-part-on-TPIS3/fundamentos/individualizado/2019/primeiro-trimestre')
for df in dfs:
    print(df.head())

dfs = pd.read_html(resp.text,index_col = 0) #quando da bloqueio pela internet usa esse
"""
#pd.read_html()

dfs = pd.read_html(resp.text,index_col = 0)
valor_de_mercado = dfs[0]
resultados = dfs[1]
patrimonio = dfs[2]
caixa = dfs[3]
divida = dfs[4]
liquidezNsolvencia = dfs[5]
fluxo_de_caixa = dfs[6]
investimentos = dfs[7]
dividendos = dfs[8]

dataset = pd.read_csv("transporte.csv",index_col = 0)