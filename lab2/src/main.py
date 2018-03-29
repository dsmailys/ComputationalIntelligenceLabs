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
from sklearn.ensemble import BaggingClassifier  
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NearestNeighbors
from sklearn.ensemble import RandomForestClassifier
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

def RunTraining(classifier, columns, resultCol, trainingData, testdata, imgFile=""):
    training_data_projection = trainingData[columns].values
    target_data_projection = trainingData[resultCol].values

    test_data_projection = testdata[columns].values
    actual_result_data = testdata[resultCol].values

    classifier.fit(training_data_projection, target_data_projection)
    results = classifier.predict(test_data_projection)

    matrix = [0, 0, 0, 0]
    
    for i in range(0, len(results)):
        if actual_result_data[i] and results[i]:
            matrix[0] = matrix[0] + 1
        elif actual_result_data[i] and not results[i]:
            matrix[1] = matrix[1] + 1
        elif not actual_result_data[i] and results[i]:
            matrix[2] = matrix[2] + 1
        elif not actual_result_data[i] and not results[i]:
            matrix[3] = matrix[3] + 1

    accuracy = accuracy_score(actual_result_data, results)*100
    if imgFile != "":
        dot_data = StringIO()
        export_graphviz(classifier, out_file=dot_data, filled=True, rounded=True,  special_characters=True)
        graph = pydot.graph_from_dot_data(dot_data.getvalue())
        graph[0].write_png(imgFile)
    
    return accuracy, matrix 


def RunDecisionTree(columns, resultCol, trainingData, testdata, imgFile):    
    clf_gini = DecisionTreeClassifier(criterion = "entropy", max_depth=5, min_samples_leaf=5)
    return RunTraining(clf_gini, columns, resultCol, trainingData, testdata, imgFile)

def RunDecisionTreeWithBagging(columns, resultCol, trainingData, testdata):    
    # bagging = BaggingClassifier(KNeighborsClassifier(),max_samples=0.5, max_features=0.5)
    bagging = BaggingClassifier(DecisionTreeClassifier(criterion = "entropy", max_depth=5, min_samples_leaf=5),max_samples=0.5, max_features=0.5)
    return RunTraining(bagging, columns, resultCol, trainingData, testdata)

def RunDecisionTreeWithForest(columns, resultCol, trainingData, testdata):    
    bagging = RandomForestClassifier(n_estimators=10)
    return RunTraining(bagging, columns, resultCol, trainingData, testdata)

def RunBestFit(data):
    nbrs = NearestNeighbors(n_neighbors=2, algorithm='ball_tree').fit(data) 

def __main__():  
    df = pd.read_csv (Constants.DATA_FILE)
    df = shuffle(df)
    training_data, test_data = SplitDataByProportion(df, 90, 10)
    run1, matrix1 = RunDecisionTree(['RESPONDED',  'WEB', 'AVRG', 'CC_CARD'], 'RESP', training_data, test_data, '4features.png')
    run2, matrix2 = RunDecisionTree(['RESPONDED', 'WEB', 'AVRG',  'CC_CARD', 'derived_RESPONSE_TO_PROMOTION', 'derived_AVERAGE_SPENT'], 'RESP', training_data, test_data, '4features+2derived.png')
    run3, matrix3 = RunDecisionTree(["HHKEY", "ZIP_CODE", "REC", "FRE", "MON", "CC_CARD", "AVRG", "PSWEATERS", "PKNIT_TOPS", "PKNIT_DRES","PBLOUSES","PJACKETS","PCAR_PNTS","PCAS_PNTS","PSHIRTS","PDRESSES","PSUITS","POUTERWEAR","PJEWELRY","PFASHION","PLEGWEAR","PCOLLSPND","AMSPEND","PSSPEND","CCSPEND","AXSPEND","TMONSPEND","OMONSPEND","SMONSPEND","PREVPD","GMP","PROMOS","DAYS","FREDAYS","MARKDOWN","CLASSES","COUPONS","STYLES","STORES","STORELOY","WEB","MAILED","RESPONDED","RESPONSERATE","HI","LTFREDAY","CLUSTYPE","PERCRET",'derived_RESPONSE_TO_PROMOTION','derived_AVERAGE_SPENT'], 'RESP', training_data, test_data, 'allFeatures.png')
    run4_1, matrix4_1 = RunDecisionTreeWithBagging(['RESPONDED', 'WEB', 'AVRG', 'CC_CARD'], 'RESP', training_data, test_data)
    run4_2, matrix4_2 = RunDecisionTreeWithForest(['RESPONDED', 'WEB', 'AVRG', 'CC_CARD'], 'RESP', training_data, test_data)
    
    print(run1)
    print(matrix1)
    print("*******************")

    print(run2)
    print(matrix2)
    print("*******************")    

    print(run3)
    print(matrix3)
    print("*******************")

    print(run4_1)
    print(matrix4_1)
    print("*******************")

    print(run4_2)
    print(matrix4_2)
    print("*******************")   

    
#prediction kaip gavome??

# Lab2 Report link: https://docs.google.com/document/d/1SWtKXVoKqoz7XgTmn5he2f8zm2Z3e508Rk_c8y3y82M/edit?usp=sharing
# TODO: balance target value RESP
# TODO: visualize trees with bagging and forest
__main__()