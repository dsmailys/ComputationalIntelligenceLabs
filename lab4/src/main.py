#!python3

import csv
import random
import numpy as np
from CampaignDetails import CampaignDetails
import Constants
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.utils import shuffle
from sklearn.metrics import accuracy_score
from sklearn.externals.six import StringIO
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import roc_curve, auc
import scikitplot as skplt


def CalculateRatio(data, feature, val1, val2):
    dataLen = len(data)
    valLen1 = len(data.loc[data[feature] == val1])
    valLen2 = len(data.loc[data[feature] == val2])
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

def DrawLift(label, Y, computedY):
    skplt.metrics.plot_lift_curve(Y, computedY, title=label)
    plt.show()

def DrawRoc(label, Y, computedY):    
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    fpr[0], tpr[0], _ = roc_curve(Y, computedY)
    roc_auc[0] = auc(fpr[0], tpr[0])
        

    # Compute micro-average ROC curve and ROC area
    fpr["micro"], tpr["micro"], _ = roc_curve(Y.ravel(), computedY.ravel())
    roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])
    plt.figure()
    lw = 2
    plt.plot(fpr[0], tpr[0], color='darkorange', lw=lw, label='ROC curve (area = %0.2f)' % roc_auc[0])
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(label)
    plt.legend(loc="lower right")
    plt.show()

def RunTraining(classifier, columns, resultCol, trainingData, testdata, title=""):
    training_data_projection = trainingData[columns].values
    target_data_projection = trainingData[resultCol].values

    test_data_projection = testdata[columns].values
    actual_result_data = testdata[resultCol].values

    classifier.fit(training_data_projection, target_data_projection)
    results = classifier.predict(test_data_projection)
    DrawRoc(title, actual_result_data, results)
    DrawLift(title, actual_result_data, classifier.predict_proba(test_data_projection))
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


def RunBernuliClassifier(columns, resultCol, trainingData, testdata, alpha=0, title=""):    
    classifier = BernoulliNB(alpha=alpha, binarize=None)
    return RunTraining(classifier, columns, resultCol, trainingData, testdata, title)

def RunMultinomialClassifier(columns, resultCol, trainingData, testdata, alpha=0, title=""):    
    classifier = MultinomialNB(alpha=alpha)
    return RunTraining(classifier, columns, resultCol, trainingData, testdata, title)

def DoRuns(name, columns, resultCol, trainingData, testdata):
    params = [0, 2, 5, 10]
    print(name + ":")
    for param in params:
        print("*******************")
        print("With " + str(param) + " alpha smoothing ")
        #run, matrix = RunBernuliClassifier(columns, resultCol, trainingData, testdata, param, name +" with " + str(param) + " alpha smoothing ")
        run, matrix = RunMultinomialClassifier(columns, resultCol, trainingData, testdata, param, name +" with " + str(param) + " alpha smoothing ")
        print("precision: " + str(run))
        print("confusion matrix: ")
        print(str(matrix[0]) + " " + str(matrix[1]))
        print(str(matrix[2]) + " " + str(matrix[3]))
        if matrix[0] + matrix[1] > 0 and matrix[0] + matrix[2] > 0:
            precision = float(matrix[0]) / (matrix[0] + matrix[1])
            recall = float(matrix[0]) / (matrix[0] + matrix[2])
            f1 = 2*(precision * recall)/(precision + recall)
            print("f1: " + str(f1))
    print("-----------------------------------------")

def CalculateAPrioriProb(feature, data, val):
    dataLen = len(data)
    positive = len(data.loc[data[feature] == val])
    return float(positive) / dataLen

def CalculateByasProb(feature, target, data, val):
    target_prob = CalculateAPrioriProb(target, data, val)
    feature_prob = CalculateAPrioriProb(feature, data, val)
    target_feature_prob = float(len(data.loc[(data[feature] == val) & (data[target] == val)])) / len(data)
    feature_target_prob = target_prob * target_feature_prob / feature_prob
    return target_prob, feature_prob, target_feature_prob, feature_target_prob

def __main__():  
    df = pd.read_csv (Constants.DATA_FILE)
    print("Before drop")
    CalculateRatio(df, 'RESP', 1, 0)
    df = Drop(df, 'RESP', 0, 0.7) # drop 55% of rows with 0 RESP
    print("After drop")
    CalculateRatio(df, 'RESP', 1, 0)    
    df = shuffle(df)
    training_data, test_data = SplitDataByProportion(df, 90, 10)

    target_prob, feature_prob, target_feature_prob, feature_target_prob = CalculateByasProb('CC_CARD', 'RESP', training_data, 1)

    print('Target feature probability: ')
    print(target_prob)

    print('Credit card holder feature probability: ')
    print(feature_prob)

    print('Feature probability to affect target')
    print(target_feature_prob)

    print('Byas probablity of target feature')
    print(feature_target_prob)

    DoRuns('Categorical features', ['CC_CARD', 'WEB'], 'RESP', training_data, test_data)
    #DoRuns('Numerical', ['PROMOS','STYLES', 'DAYS', 'REC'], 'RESP', training_data, test_data)
    DoRuns('Mixed', ['derived_RESPONSE_TO_PROMOTION','derived_AVERAGE_SPENT'], 'RESP', training_data, test_data)
    DoRuns('Mixed', ['derived_RESPONSE_TO_PROMOTION','derived_AVERAGE_SPENT','CC_CARD', 'WEB'], 'RESP', training_data, test_data)
    
__main__()


# TODO: decide on classifier and tests
# TODO: finish report
