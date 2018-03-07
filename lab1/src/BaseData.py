class BaseData:
    def __init__(self, dataList):
        self.data = dataList
        self.dataLength = len(self.data)

    def GetDataLength(self):
        return self.dataLength

    def FindMissingCount (self):
        missingCount = 0
        for item in self.data:
            if not item and item != 0:
                missingCount = missingCount + 1
        return missingCount

    def GetDataCardinality (self):
        return len(set(self.data))

    def GetData(self):
        return self.data