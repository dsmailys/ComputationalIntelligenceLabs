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
    
def __main__():
    #read initial data set
    data = ReadInitialData(Constants.DATA_FILE)

    # # calculate categorical value for credit card holder
    # cardHolderCount = sum(1 for item in data if item.CC_CARD == '1')
    # nonCardHolder = sum(1 for item in data if item.CC_CARD == '0')
    # DrawBarChart(("CreditCard", "Cash"), (cardHolderCount, nonCardHolder), "Usage", "Credit card usage", True)

    # # calculate categorical value for web shoppers
    # webShopperCount = sum(1 for item in data if item.WEB == '1')
    # nonWebShopperCount = sum(1 for item in data if item.WEB == '0')
    # DrawBarChart(("Web Shopper", "Store Shopper"), (webShopperCount, nonWebShopperCount), "Usage", "Web shopping usage", True)

    # # calculate numerical value for average amount spent per visit
    # spentSorted = list(float(item.AVRG) for item in data)
    # DrawHistogram(spentSorted, "Average amount spent per visit", "Frequency", "Amount spent", 500, [0, 300, 0, 800], True)

    # number of RESPONDED promotions last year
    # responded = list(int(item.RESPONDED) for item in data)
    # DrawHistogram(responded, "Number of responded promotions last year", "Frequency", "Responded amount", 30, [0, 10, 0, 12000], True)

    # # finding outliers for average spent
    # elements = list(float(item.AVRG) for item in data)
    # outliers = FindOutliers (elements)
    # PrintList(outliers)

    # finding outliers for promotions responded last year
    # elements = list(int(item.RESPONDED) for item in data)
    # outliers = FindOutliers (elements)
    # PrintList (outliers)


__main__()