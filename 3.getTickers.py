#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 09:58:47 2019

@author: itamar
"""
import bs4 as bs
import pickle
import requests
#First of all you need to find a site with the table list of the b3 companies
print(chr(ord('A')+1))

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

if __name__ == "__main__":        
    save_B3_tickers()