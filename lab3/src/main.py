#!python3

import csv
import random

from CampaignDetails import CampaignDetails
import Constants
import pandas as pd
from sklearn.utils import shuffle
from sklearn.metrics import accuracy_score
from sklearn.externals.six import StringIO
from sklearn.neighbors import KNeighborsClassifier


def CalculateRatio(data, feature, val1, val2):
    dataLen = len(data)
    valLen1 = len(data.loc[data[feature] == val1])
    valLen2 = len(data.loc[data[feature] == val2])
    print ("Feature " + feature)
    print("Value " + str(val1) + " and " + str(val2) + " ratio - " + str(round(float(valLen1) / dataLen, 2)) + ":" +  str(round(float(valLen2) / dataLen, 2)))

def Drop(data, feature, value, percentage):
    
    withValue = data.loc[data[feature] == value]
    rowsToDrop = withValue.tail(int(len(withValue) * percentage)).index
    rowsToKeep = set(range(data.shape[0])) - set(rowsToDrop) # faster than dropping
    return data.take(list(rowsToKeep))
    

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
    return accuracy, matrix 


def RunKNeighborsClassifier(columns, resultCol, trainingData, testdata, neighbors=3, distance="manhattan"):    
    classifier = KNeighborsClassifier(n_neighbors=neighbors, metric=distance)
    return RunTraining(classifier, columns, resultCol, trainingData, testdata)

def DoRuns(name, columns, resultCol, trainingData, testdata):
    params = [(2, "manhattan"), (3, "manhattan"), (4, "manhattan"), (2, "minkowski"), (3, "minkowski"), (4, "minkowski")]
    print(name + ":")
    for param in params:
        print("*******************")
        print("With " + str(param[0]) + " neightboars and using " + str(param[1]) + " distance" )
        run, matrix = RunKNeighborsClassifier(columns, resultCol, trainingData, testdata, param[0], param[1])
        print("precision: " + str(run))
        print("confusion matrix: ")
        print(str(matrix[0]) + " " + str(matrix[1]))
        print(str(matrix[2]) + " " + str(matrix[3]))
        
    print("-----------------------------------------")

def __main__():  
    df = pd.read_csv (Constants.DATA_FILE)
    print("Before drop")
    CalculateRatio(df, 'RESP', 1, 0)
    df = Drop(df, 'RESP', 0, 0.55) # drop 55% of rows with 0 RESP
    print("After drop")
    CalculateRatio(df, 'RESP', 1, 0)    
    df = shuffle(df)
    

    training_data, test_data = SplitDataByProportion(df, 90, 10)
    print("-----------------------------------------")
    DoRuns("Numerical", ['RESPONDED',  'AVRG'], 'RESP', training_data, test_data)
    DoRuns("Categorical", ['WEB',  'CC_CARD'], 'RESP', training_data, test_data)
    DoRuns("Mixed", ['WEB',  'CC_CARD', 'RESPONDED',  'AVRG'], 'RESP', training_data, test_data)
    # TODO: make lab3 report
    # https://docs.google.com/document/d/1JMO2iZFIIGlOCF70O3tbLZR1Fm_fx7HPoC-w-ISUs6I/
__main__()