import numpy as np
import matplotlib.pyplot as plt
from BaseData import BaseData

class CategoricalData(BaseData):
    def __init__(self, dataList, printedName):
        BaseData.__init__(self, dataList)
        self.name = printedName
    
    def GetCategoricalDataCount(self, value):
        return sum(1 for item in BaseData.GetData(self) if item == value)
    
    def DrawBarChart(self, xticks, categoricalDataFilter, yLabel, title):
        categoricalData = []
        for item in categoricalDataFilter:
            categoricalData.append(self.GetCategoricalDataCount(item))

        y_pos = np.arange(len(xticks))
        plt.bar(y_pos, tuple(categoricalData), align='center', alpha=0.5)
        plt.xticks(y_pos, xticks)
        plt.ylabel(yLabel)
        plt.title(title)
        plt.show()

    def GetMode(self):
        return max(set(self.data), key=self.data.count)

    def GetFeatureNames():
        return ["Feature", "Count", "Miss. %", "Card.", "Mode"]

    def GetFeatureSet(self):
        features = []
        features.append(self.name)
        features.append(self.GetDataLength())
        features.append(float(self.FindMissingCount()) / self.GetDataLength() * 100)
        features.append(self.GetDataCardinality())
        features.append(self.GetMode())
        return features