#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 14:57:35 2019

@author: itamar
"""

import numpy as np
import pandas as pd
import pickle
from collections import Counter
from sklearn.model_selection import cross_validate
from sklearn import svm, neighbors
from sklearn.ensemble import RandomForestClassifier, VotingClassifier

def preprocess_data_for_labels(ticker):
    hm_days = 7
    df = pd.read_csv('bovespa.csv',index_col=0)
    tickers = df.columns.values.tolist()
    df.fillna(0,inplace = True)
    dataset = pd.DataFrame()
    for i in range(1,hm_days + 1):
        df['{}_{}d'.format(ticker,i)] = (df[ticker].shift(-i) - df[ticker])/df[ticker]
        
    df.fillna(0,inplace = True)
    return tickers,df
    

def buy_sell_hold(*args):
    cols = [c for c in args]
    requirement = 0.02
    for col in cols:
        if col > requirement:
            return 1
        if col < -requirement:
            return -1
    return 0


def extract_featurets(ticker):
    dataset = pd.DataFrame()
    tickers, df = preprocess_data_for_labels(ticker)
    df['{}_target'.format(ticker)] = list(map(buy_sell_hold,
                                          df['{}_1d'.format(ticker)],
                                          df['{}_2d'.format(ticker)],
                                          df['{}_3d'.format(ticker)],
                                          df['{}_4d'.format(ticker)],
                                          df['{}_5d'.format(ticker)],
                                          df['{}_6d'.format(ticker)],
                                          df['{}_7d'.format(ticker)]))
    
    vals = df['{}_target'.format(ticker)].values.tolist()
    str_vals = [str(i) for i in vals]
    print('Data spread:' , Counter(str_vals))
    
    df.fillna(0,inplace = True)
    df = df.replace([np.inf, -np.inf], np.nan)
    df.dropna(inplace = True)
    
    bov = pd.read_csv('bovespa.csv',index_col=0)
    
    df_vals = df[[ticker for ticker in tickers]].pct_change()
    df_vals = df_vals.replace([np.inf, -np.inf], 0)
    df_vals.fillna(0, inplace = True)
    
    X = df_vals.values
    y = df['{}_target'.format(ticker)].values
    
    return X,y,df

ticker = 'JSLG3'
X,y,df = extract_featurets(ticker = 'JSLG3')
    
    