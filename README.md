# StockMarketPy
[![author](https://img.shields.io/badge/author-ItamarRocha-black.svg)](https://github.com/ItamarRocha) 
![Logo](images/lmf-logo.png)

> Repository to learn the basics of algo trading and IA in (Brazilian stock market)

## Table of contents
- [Setup](#Setup)
- [Clone](#Clone)
- [Description](#Description)
- [License](#License)

### Setup
> all libraries needed to manipulate the data and acess databases
```shell
pip install pandas
pip install pandas_datareader
pip install pickle
pip install datetime
pip install bs4
pip install matplotlib
pip install mpl_finance
```
### You may find the equivalent tickers of brazilian stocks in this site 
 https://finance.yahoo.com/quote/JSLG3.SA?p=JSLG3.SA&.tsrc=fin-srch

### Clone

- Clone this repo to your local machine using https://github.com/ItamarRocha/Torneio-de-carteiras-LMF

### Description

* #### 1.serchNplot.py
This script is responsible for plotting graphs using only matplotlib

* #### 2.tickergraph.py
Plots the time series data of a stock in candlestick format, using mpl_finance library

* #### 3.gettingTickers.py
Gets all the tickers of brazilian stock market through this [site](https://br.advfn.com/bolsa-de-valores/bovespa/) using beautiful soup and dumps a pickle archive with the stocks tickers.

* #### 4.GetAllPrices.py
Responsible for gathering the data specified by the tickers in the yahoo finances api. It gets the Min, Max, Open, High, Close and Adj. Close since 01/01/2000 till the day specified in the code and stores the data in a folder named stock_dfs.

* #### 5.puttingAlltogether.py
Gathers all the stocks closing prices into one dataframe.

* #### 6.Correlation.py
After executing the last script, it plots the correlation between each stock


### License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](http://opensource.org/licenses/mit-license.php)**
