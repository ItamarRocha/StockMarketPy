#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  6 11:46:36 2020

@author: itamar
"""

import bs4 as bs
import pandas_datareader as web
import requests
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito') #private
#options.add_argument('--headless') # doesnt open page

browser = webdriver.Chrome('/home/itamar/Desktop/chromedriver', chrome_options=options)

site = 'http://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/renda-variavel/empresas-listadas.htm'

browser.get(site)

xml = requests.get(site)
soup = bs.BeautifulSoup(xml.text,'lxml')

with open('html.txt',"w") as f:
    f.write(str(soup))
    

elem = browser.find_element_by_class_name("levelwrap level1")