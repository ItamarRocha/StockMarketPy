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
from 7.MesmoSetor.py import preprocessed_dataframe
from collections import Counter
from sklearn.model_selection import cross_validate
from sklearn import svm, neighbors
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
    
