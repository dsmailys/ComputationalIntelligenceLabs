import matplotlib.pyplot as plt
import numpy as np

from BaseData import BaseData

class NumericalData(BaseData):
    def __init__(self, dataList, printedName):
        BaseData.__init__(self, dataList)
        self.name = printedName
        self.outliers, self.nonOutliers = self.__FindOutliers()

    def DrawHistogram (self, title, yLabel, xLabel, norm, axisConfig):
        plt.hist (BaseData.GetData(self), norm)
        plt.ylabel(yLabel)
        plt.xlabel(xLabel)
        plt.title(title)
        plt.axis(axisConfig)
        plt.grid(True)
        plt.show()

    def DrawBoxPlot(self, whisNumber, xAxisLabel):
        plt.boxplot(BaseData.GetData(self), whis = whisNumber, labels=xAxisLabel)
        plt.show()

    def __FindOutliers (self):
        mean = np.mean (BaseData.GetData(self))
        sd = np.std(BaseData.GetData(self))
        outliers = []
        nonOutliers = []
        for x in BaseData.GetData(self):
            if x < mean - 2 * sd or x > mean + 2 * sd:
                outliers.append(x)
            else:
                nonOutliers.append(x)
        outliers = sorted(outliers)
        return outliers, nonOutliers

    def GetOutliersPercentage(self):
        return float(len(self.outliers)) / BaseData.GetDataLength(self) * 100
    
    def GetOutliers(self):
        return self.outliers
    
    def GetNormalizedData(self):
        return self.nonOutliers

    def GetMeanOfNormalized(self):
        return np.mean(self.GetNormalizedData())

    def GetRangeOfNormalized(self):
        return max(self.GetNormalizedData()) - min(self.GetNormalizedData())

    def GetFeatureSet(self):
        features = []
        features.append(self.name)
        features.append(BaseData.GetDataLength(self))
        features.append(float(BaseData.FindMissingCount(self)) / BaseData.GetDataLength(self) * 100)
        features.append(BaseData.GetDataCardinality(self))
        features.append(round(self.GetOutliersPercentage(), 2))
        features.append(round(self.GetMeanOfNormalized(), 2))
        features.append(self.GetRangeOfNormalized())
        return features