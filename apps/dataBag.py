class dataBag:
    def __init__(self, dataframes):
        self.dataframes=self.makeDictionary(dataframes)
        self.default=dataframes[0]
    def makeDictionary(self, dataframes):
        dictionary={}
        for dataframe in dataframes:
            dictionary[dataframe.title]=dataframe
        return dictionary
    def getDataframe(self,title=None):
        if(title not in self.dataframes.keys() or title==None):
            return self.default
        if(len(self.dataframes)==1):
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
    def modify_by_name(self, name, mode):
        for key in self.dataframes:
            if self.dataframes[key].name==name:
                self.dataframes[key].activateDataframe(mode)
    def get_title_by_name(self, name):
        for key in self.dataframes:
            if self.dataframes[key].name==name:
                return key