import csv
import numpy as np
import matplotlib.pyplot as plt

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
    if showPlot == True:
        y_pos = np.arange(len(objectList))
        plt.bar(y_pos, dataList, align='center', alpha=0.5)
        plt.xticks(y_pos, objectList)
        plt.ylabel(yLabel)
        plt.title(title)
        plt.show()
    
def __main__():
    #read initial data set
    data = ReadInitialData(Constants.DATA_FILE)

    # calculate categorical value for credit card holder
    cardHolderCount = sum(1 for item in data if item.CC_CARD == '1')
    nonCardHolder = sum(1 for item in data if item.CC_CARD == '0')
    DrawBarChart(("CreditCard", "Cash"), (cardHolderCount, nonCardHolder), "Usage", "Credit card usage", False)

    # calculate categorical value for web shoppers
    webShopperCount = sum(1 for item in data if item.WEB == '1')
    nonWebShopperCount = sum(1 for item in data if item.WEB == '0')
    DrawBarChart(("Web Shopper", "Store Shopper"), (webShopperCount, nonWebShopperCount), "Usage", "Web shopping usage", False)

__main__()