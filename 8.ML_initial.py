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
import functions as ms
from collections import Counter
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.model_selection import cross_validate
from sklearn import svm, neighbors
from sklearn.ensemble import RandomForestClassifier, VotingClassifier


dataset , prediction = ms.preprocessed_dataframe()

y = dataset['91d']
X = dataset.drop(columns = ['91d'])
scaler = StandardScaler()
X = scaler.fit_transform(X)

"""
need to use different scaler types and compare
"""
"""
from sklearn.decomposition import PCA
pca = PCA(n_components = 7)
X = pca.fit_transform(X)
explained_variance = pca.explained_variance_ratio_.sum()
"""
from sklearn.model_selection import train_test_split
X_train,X_test, y_train, y_test = train_test_split(X,y,test_size = 0.2,random_state = 0)
"""
from sklearn.tree import DecisionTreeRegressor
regressor = DecisionTreeRegressor()
regressor.fit(X_train,y_train)
y_pred = regressor.predict(X_test)
"""
from sklearn.ensemble import RandomForestRegressor
regressor2 = RandomForestRegressor(n_estimators=100,n_jobs=-1)
regressor2.fit(X_train,y_train)
y_pred2 = regressor2.predict(X_test)

from sklearn.metrics import r2_score, explained_variance_score
#print('Decision tree\n r2_score:',r2_score(y_test,y_pred),'\nvariance : ',explained_variance_score(y_test,y_pred))
print('Random Forest\n r2_score:',r2_score(y_test,y_pred2),'\nvariance : ',explained_variance_score(y_test,y_pred2))

scaler = StandardScaler()
#data_predict = prediction.drop(columns = ['91d'])
#data_predict = scaler.fit_transform(data_predict)

#final_prediction = regressor2.predict(data_predict)