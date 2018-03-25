import csv
import random

from CampaignDetails import CampaignDetails
import Constants

def ReadInitialData(dataFile):
    data_list = []
    with open(dataFile, 'rt') as csv_file:
        reader = csv.reader(csv_file)
        next(reader, None)  # Skip the header.
        # Unpack the row directly in the head of the for loop.
        for line in reader:
            data_list.append(CampaignDetails(line))
    return data_list

def SplitDataByProportion (data, training_proportion, test_proportion):
    if training_proportion > 100 or training_proportion < 0:
        raise ValueError("Training proportion must be between 0 and 100")
    if test_proportion > 100 or test_proportion < 0:
        raise ValueError("Test proportion must be between 0 and 100")
    if test_proportion + training_proportion != 100:
        raise ValueError("Test and training proportions must be equal to 100 when added")
    
    totalLength = len(data)
    trainingCount = training_proportion * totalLength / 100
    trainingData = data[:trainingCount]

    testData = data[trainingCount:totalLength]
    return trainingData, testData

def __main__():
    data = ReadInitialData(Constants.DATA_FILE)
    random.shuffle(data)
    
    training_data, test_data = SplitDataByProportion(data, 90, 10)
    print(len(training_data))
    print(len(test_data))
    
# Lab2 Report link: https://docs.google.com/document/d/1SWtKXVoKqoz7XgTmn5he2f8zm2Z3e508Rk_c8y3y82M/edit?usp=sharing

__main__()