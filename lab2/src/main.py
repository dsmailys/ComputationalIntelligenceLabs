#!python3

import csv
import random

from CampaignDetails import CampaignDetails
import Constants

import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_graphviz
import numpy as np
from sklearn.utils import shuffle
from sklearn.metrics import accuracy_score
from sklearn.externals.six import StringIO  
import pydot 

def SplitDataByProportion (data, training_proportion, test_proportion):
    if training_proportion > 100 or training_proportion < 0:
        raise ValueError("Training proportion must be between 0 and 100")
    if test_proportion > 100 or test_proportion < 0:
        raise ValueError("Test proportion must be between 0 and 100")
    if test_proportion + training_proportion != 100:
        raise ValueError("Test and training proportions must be equal to 100 when added")
    
    totalLength = len(data)
    trainingCount = training_proportion * totalLength / 100
    trainingData = data[:int(trainingCount)]

    testData = data[int(trainingCount):int(totalLength)]
    return trainingData, testData

def __main__():  
    df = pd.read_csv (Constants.DATA_FILE)
    df = shuffle(df)
    training_data, test_data = SplitDataByProportion(df, 90, 10)
    
    training_data_projection = training_data[['RESPONDED', 'WEB', 'AVRG', 'CC_CARD']]
    target_data_projection = training_data['PC_CALC20']

    test_data_projection = test_data[['RESPONDED', 'WEB', 'AVRG', 'CC_CARD']]
    actual_result_data = test_data['PC_CALC20']

    clf_gini = DecisionTreeClassifier(criterion = "gini", max_depth=3, min_samples_leaf=5)
    clf_gini.fit(training_data_projection, target_data_projection)
    results = clf_gini.predict(test_data_projection)

    accuracy = accuracy_score(actual_result_data, results)*100
    print(accuracy)
    dot_data = StringIO()
    export_graphviz(clf_gini, out_file=dot_data, filled=True, rounded=True,  special_characters=True)
    graph = pydot.graph_from_dot_data(dot_data.getvalue())
    graph[0].write_png("iris.png") 

# Lab2 Report link: https://docs.google.com/document/d/1SWtKXVoKqoz7XgTmn5he2f8zm2Z3e508Rk_c8y3y82M/edit?usp=sharing

__main__()