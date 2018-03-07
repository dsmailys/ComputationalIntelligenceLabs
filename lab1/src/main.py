import csv
import prettytable

from CampaignDetails import CampaignDetails
from CategoricalData import CategoricalData
from NumericalData import NumericalData
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

def PrintData(header, data, fileName):
    with open(fileName, 'w+') as outliersFile:
        outliersFile.write(header + "\n")
        for item in data:
            outliersFile.write(str(item) + ", ")           

def PrintTable (headers, rows):
    table = prettytable.PrettyTable(headers)
    for row in rows:
        table.add_row(row)
    print (table)

def __main__():
    data = ReadInitialData(Constants.DATA_FILE)

    # calculate categorical value for credit card holder
    CardHolderData = CategoricalData(list(item.CC_CARD for item in data), "Card holder")
    CardHolderData.DrawBarChart(("CreditCard", "Cash"), ["1", "0"], "Usage", "Credit card usage")

    # calculate categorical value for web shoppers
    WebShopperData = CategoricalData(list(item.WEB for item in data), "Web shopper")
    WebShopperData.DrawBarChart(("Web Shopper", "Store Shopper"), ["1", "0"], "Usage", "Web shopping usage")

    # calculate numerical value for average amount spent per visit
    AverageSpentData = NumericalData(list(float(item.AVRG) for item in data), "Average spent")
    AverageSpentData.DrawHistogram("Average amount spent per visit", "Frequency", "Amount spent", 500, [0, 300, 0, 800])
    PrintData("Outliers for average amount spent", AverageSpentData.GetOutliers(), Constants.OUTLIERS_FILE)

    #number of RESPONDED promotions last year
    RespondedPromotionsData = NumericalData(list(int(item.RESPONDED) for item in data), "Responded Promotions")
    RespondedPromotionsData.DrawHistogram("Number of responded promotions last year", "Frequency", "Responded amount", 30, [0, 10, 0, 12000])
    RespondedPromotionsData.DrawBoxPlot(3, ["Number of respondents to promotion"])    

    print("Categorical features:")
    PrintTable(["Feature", "Count", "Miss. %", "Card."], [WebShopperData.GetFeatureSet(), CardHolderData.GetFeatureSet()])

    print("Continuous features:")    
    PrintTable(["Feature", "Count", "Miss. %", "Card.", "Outliers %", "Mean", "Range"], [AverageSpentData.GetFeatureSet(), RespondedPromotionsData.GetFeatureSet()])


# TODO: 
# (3) explore the shape of distribution. Perform standardization and normalization, consider the normality of data 
# 	- graphs and description of actions done
# (4) explore the characteristics of features: central tendency, spread measures and dependency (the technique depends on which data type you have)
# 	- table of characteristics
# (5) append the data set with two derived features of different types (at least 2 out of 4)
# 	- description of new features (types, characterics, distribution)
# Calculate corelation for numerical features
# Calculate moda for categorical features
# Make a report of labs

__main__()