#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 19:35:13 2019

@author: itamar
"""
"""
The arrow of time—If you’re trying to predict the future given the past (for exam-
ple, tomorrow’s weather, stock movements, and so on), you should not ran-
domly shuffle your data before splitting it, because doing so will create a
temporal leak: your model will effectively be trained on data from the future. In
such situations, you should always make sure all data in your test set is posterior
to the data in the training set.

Próximos passos : adicionar todos os dias do ano
de forma que de pra manipular os trimestres de forma exata
depois adicionar os dados fundamentalistas
testar metodos com todos os dias e com apenas alguns
"""
import numpy as np
import pandas as pd
import pickle
#import functions as ms
import testing as ts
from collections import Counter
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.model_selection import cross_validate
from sklearn import svm, neighbors
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn import preprocessing
from keras.models import Sequential
from keras.layers import Dense, LSTM
from sklearn.preprocessing import MinMaxScaler
import xgboost as xgb
main = pd.DataFrame()
#main = ts.test_compiled_dataframe('construção')
train_test , prediction,dataset = ts.test_preprocessed_dataframe('construção')


train_test = train_test.sample(frac=1)

y = train_test['180d']
X = train_test.drop(columns = ['180d'])
scaler = MinMaxScaler(feature_range=(0,1))
X = scaler.fit_transform(X)

date = pd.DataFrame(pd.to_datetime(train_test.index).year - 2011)

X = np.append(X,date,axis = 1 )




from sklearn.model_selection import train_test_split
X_train,X_test, y_train, y_test = train_test_split(X,y,test_size = 0.25)

X_train = X_train.reshape(1,18194,91)
X_test = X_test.reshape(1,6065,91)

model = Sequential()

model.add(LSTM(50, input_shape=(18194,91)))
model.add(Dense(1))

model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(X_train, y_train, batch_size=1, epochs=1)
"""
xgb_model = xgb.XGBRegressor()

xgb_model.fit(X_train, y_train)

y_pred = xgb_model.predict(X_test)

print('Xg\n r2_score:',r2_score(y_test,y_pred),'\nvariance : ',explained_variance_score(y_test,y_pred))

"""
from sklearn.ensemble import RandomForestRegressor
regressor2 = RandomForestRegressor(n_estimators=10,n_jobs=-1)
regressor2.fit(X_train,y_train)
y_pred2 = regressor2.predict(X_test)

from sklearn.metrics import r2_score, explained_variance_score,SCORERS
#print('Decision tree\n r2_score:',r2_score(y_test,y_pred),'\nvariance : ',explained_variance_score(y_test,y_pred))
print('Random Forest\n r2_score:',r2_score(y_test,y_pred2),'\nvariance : ',explained_variance_score(y_test,y_pred2))

from sklearn.model_selection import cross_val_score,cross_val_predict,cross_validate
accuracies = cross_val_score(estimator = regressor2, X = X, y = y, cv = 10,n_jobs=-1,scoring='r2')
accuracies.mean()

#sorted(SCORERS.keys())

scaler = MinMaxScaler(feature_range=(0,1))
#X_prediction = prediction.drop(columns = ['91d'])
X_prediction = prediction.drop(columns = ['180d'])
X_prediction = scaler.fit_transform(X_prediction)
X_prediction = np.append(X_prediction,pd.DataFrame(pd.to_datetime(prediction.index).year - 2011),1 )
y_prediction = regressor2.predict(X_prediction)
#y_prediction = xgb_model.predict(X_prediction)

prediction_final = prediction.drop(columns = prediction.columns[0:82])
#prediction['91d'] = y_prediction
prediction_final['180d'] = y_prediction

true = ts.get_true_values(sector = 'construção')
compare = true.drop(columns = ['ticker'])
compare = scaler.fit_transform(compare)
y_prediction = scaler.fit_transform(pd.DataFrame(y_prediction))
explained_variance_score(compare,y_prediction)
r2_score(compare,y_prediction)

even = prediction_final.loc[prediction_final['EVEN3'] == 1]['180d']
