import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from decimal import Decimal

from CampaignDetails import CampaignDetails
import Constants

def ReadInitialData(dataFile):
    data_list = []
    with open(dataFile, 'rb') as csv_file:
        reader = csv.reader(csv_file)
        next(reader, None)  # Skip the header.
        # Unpack the row directly in the head of the for loop.
        for line in reader:
            data_list.append(CampaignDetails(line))
    return data_list

def DrawBarChart(objectList, dataList, yLabel, title, showPlot = True):
    y_pos = np.arange(len(objectList))
    plt.bar(y_pos, dataList, align='center', alpha=0.5)
    plt.xticks(y_pos, objectList)
    plt.ylabel(yLabel)
    plt.title(title)
    if showPlot == True:
        plt.show()

def DrawHistogram (dataList, title, yLabel, xLabel, norm, axisConfig, showPlot = True):
    plt.hist (dataList, norm)
    plt.ylabel(yLabel)
    plt.xlabel(xLabel)
    plt.title(title)
    plt.axis(axisConfig)
    plt.grid(True)

    if showPlot == True:
        plt.show()

def FindOutliers (dataList):
    mean = np.mean (dataList)
    sd = np.std(dataList)
    return sorted(set((list(x for x in dataList if (x < mean - 2 * sd or x > mean + 2 * sd)))))

def PrintList (dataList):
    for item in dataList:
        print(item)

def FindMissingValues (dataList):
    missingCount = 0
    for item in dataList:
        if not item:
            missingCount = missingCount + 1
    return missingCount
    
def __main__():
    #read initial data set
    data = ReadInitialData(Constants.DATA_FILE)

    # calculate categorical value for credit card holder
    cardHolderCount = sum(1 for item in data if item.CC_CARD == '1')
    nonCardHolder = sum(1 for item in data if item.CC_CARD == '0')
    DrawBarChart(("CreditCard", "Cash"), (cardHolderCount, nonCardHolder), "Usage", "Credit card usage", True)

    # calculate categorical value for web shoppers
    webShopperCount = sum(1 for item in data if item.WEB == '1')
    nonWebShopperCount = sum(1 for item in data if item.WEB == '0')
    DrawBarChart(("Web Shopper", "Store Shopper"), (webShopperCount, nonWebShopperCount), "Usage", "Web shopping usage", True)

    # calculate numerical value for average amount spent per visit
    spentSorted = list(float(item.AVRG) for item in data)
    DrawHistogram(spentSorted, "Average amount spent per visit", "Frequency", "Amount spent", 500, [0, 300, 0, 800], True)

    #number of RESPONDED promotions last year
    responded = list(int(item.RESPONDED) for item in data)
    DrawHistogram(responded, "Number of responded promotions last year", "Frequency", "Responded amount", 30, [0, 10, 0, 12000], True)

    # finding outliers for average spent
    elements = list(float(item.AVRG) for item in data)
    outliers = FindOutliers (elements)
    print ("Outliers for average spent: ")
    PrintList(outliers)

    #finding outliers for promotions responded last year
    elements = list(int(item.RESPONDED) for item in data)
    outliers = FindOutliers (elements)
    print ("Outliers for promotions responded last year")
    PrintList (outliers)

    #finding missing values for average spent
    missing = FindMissingValues ((item.AVRG for item in data))
    print ("Missing data from average amount spent per visit:")
    print (missing)

    #finding missing values for promotions responded last year
    missing = FindMissingValues ((item.RESPONDED for item in data))
    print ("Missing data from promotions responded last year")
    print (missing)

    # finding cardinality for average spent
    avgSpent = list((item.AVRG for item in data))
    avgSpentSet = set(avgSpent)
    print("Average spent data set length:")
    print(len(avgSpent))
    print("Cardinality of values:")
    print(len(avgSpentSet))

    # finding cardinality for promotions responded
    responded = list((item.RESPONDED for item in data))
    respondedSet = set(responded)
    print("Responded to promotions data set length:")
    print(len(responded))
    print("Cardinality of values:")
    print(len(respondedSet))

# TODO: Do we need table and graphs for quality report?
# TODO: 
# (3) explore the shape of distribution. Perform standardization and normalization, consider the normality of data 
# 	- graphs and description of actions done
# (4) explore the characteristics of features: central tendency, spread measures and dependency (the technique depends on which data type you have)
# 	- table of characteristics
# (5) append the data set with two derived features of different types (at least 2 out of 4)
# 	- description of new features (types, characterics, distribution)

__main__()