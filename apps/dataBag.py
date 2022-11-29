class dataBag:
    def __init__(self, dataframes):
        self.dataframes=self.makeDictionary(dataframes)
        self.default=dataframes[1]
    def makeDictionary(self, dataframes):
        dictionary={}
        for dataframe in dataframes:
            dictionary[dataframe.title]=dataframe
        return dictionary
    def getDataframe(self,title):
        if(title not in self.dataframes.keys()):
            return self.default
        return self.dataframes[title]
    def getTitle(self,dataframe):
        for key in self.dataframes:
            if self.dataframes[key]==dataframe:
                return key
    def getByName(self, name):
        for key in self.dataframes:
            if self.dataframes[key].name==name:
                return self.dataframes[key]
        return