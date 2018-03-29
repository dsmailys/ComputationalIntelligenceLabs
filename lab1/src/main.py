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

def PrintCSVData(columns, data, fileName):
    with open(fileName, 'w+') as fout:
        fout.write(",".join(columns) + "\n")
        for item in data:
            fout.write(",".join([ str(getattr(item, col)) for col in columns ])+ "\n")  

def PrintTable (headers, rows):
    table = prettytable.PrettyTable(headers)
    for row in rows:
        table.add_row(row)
    print (table)

def AppendNewDataColumn(data, colName, colData):
    if len(data) != len(colData):
        raise Exception('data and colData lengths do not match')

    for i in range(0, len(data)):
        setattr(data[i], colName, colData[i])

def __main__():
    dataColumns = ["HHKEY", "ZIP_CODE", "REC", "FRE", "MON", "CC_CARD", "AVRG", "PC_CALC20", "PSWEATERS", "PKNIT_TOPS", "PKNIT_DRES","PBLOUSES","PJACKETS","PCAR_PNTS","PCAS_PNTS","PSHIRTS","PDRESSES","PSUITS","POUTERWEAR","PJEWELRY","PFASHION","PLEGWEAR","PCOLLSPND","AMSPEND","PSSPEND","CCSPEND","AXSPEND","TMONSPEND","OMONSPEND","SMONSPEND","PREVPD","GMP","PROMOS","DAYS","FREDAYS","MARKDOWN","CLASSES","COUPONS","STYLES","STORES","STORELOY","VALPHON","WEB","MAILED","RESPONDED","RESPONSERATE","HI","LTFREDAY","CLUSTYPE","PERCRET","RESP"]
    data = ReadInitialData(Constants.DATA_FILE)

    TargetFeature = CategoricalData(list(item.RESP for item in data), "Responded")
    TargetFeature.DrawBarChart(("Responded", "Not"), ["1", "0"], "Responding", "Responding to promotions")

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
    PrintTable(CardHolderData.GetFeatureNames(), [WebShopperData.GetFeatureSet(), CardHolderData.GetFeatureSet()])

    print("Continuous features:")    
    PrintTable(AverageSpentData.GetFeatureNames(), [AverageSpentData.GetFeatureSet(), RespondedPromotionsData.GetFeatureSet()])

    #correlation between AverageSpentData and RespondedPromotionsData
    AverageSpentData.DrawScatterPlot("Correlation", "Number of respondents to promotion", "Average spent", RespondedPromotionsData.data)
    coef = AverageSpentData.GetCorrelationCoef(RespondedPromotionsData.data)[0, 1]
    print("Correlation coefficient between 'Average spent' and 'Number of respondents to promotion': " + str(coef))

    #remove outliers
    AverageSpentData.RemoveOutlierRows(data)

    #calculate new feature from responded group
    def getCategory(item):
        if int(item) < 2:
            return "0"
        if int(item) < 8:
            return "1"
        return "2"
    
    RespondedToPromotionsCategoricalData = CategoricalData(list(map(getCategory, list(int(item.RESPONDED) for item in data))), "Response strength")
    RespondedToPromotionsCategoricalData.DrawBarChart(("none or weak", "medium", "strong"), ["0", "1", "2"], "Number of responses", "Response strength")

    #calculate new feature from average spent

    def getCategoryForAvrg(item):
        if int(item) < 50:
            return "0"
        if int(item) < 200:
            return "1"
        return "2"
    
    AverageSpentCategoricalData = CategoricalData(list(map(getCategoryForAvrg, list(float(item.AVRG) for item in data))), "Spending category")
    AverageSpentCategoricalData.DrawBarChart(("small", "medium", "strong"), ["0", "1", "2"], "Number of spendings", "Spending strength")

    # add new features to data set
    AppendNewDataColumn(data, "derived_RESPONSE_TO_PROMOTION", RespondedToPromotionsCategoricalData.data)
    dataColumns.append("derived_RESPONSE_TO_PROMOTION")
    AppendNewDataColumn(data, "derived_AVERAGE_SPENT", AverageSpentCategoricalData.data)
    dataColumns.append("derived_AVERAGE_SPENT")

    # print new data set
    PrintCSVData(dataColumns, data, Constants.PROCESSED_DATA_FILE)

# median +- (1.5*IQR (inter quartile range)) Boxplot outliers exponentiniam
# Pearson correleaton kai normal distribution, kitaip naudoti Spearman arba Kendall.
# TODO: 
# Make a report of labs link: https://docs.google.com/document/d/1-zbwE8rgsRiNrSc1DGPN47sBmlfxy7hx1pXFY2gUfqI/edit?usp=sharing

__main__()