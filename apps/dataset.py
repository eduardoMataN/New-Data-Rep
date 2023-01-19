import pandas as pd
class dataset:
    
    def __init__(self, title, df_original, column=None, name=None, group=None, By=None):
        self.df_original=df_original
        self.title=title
        if(column!=None):
            self.max=df_original[column].max()
            self.min=df_original[column].min()
        if(column==None):
            self.df_percent_change=None
           
        elif(column!=None and group!=None and By!=None):
            self.df_percent_change=self.get_percent_change(df_original, column, group, By)
        elif(column!=None and group==None and By==None):
            self.df_percent_change=self.get_percent_change_simple(column)
        self.df_active=df_original
        self.name=name
        self.active_mode='Original'
        self.trimMax=None
        self.trimMin=None
        self.trimmed=False
        self.unit=1
        
    def get_original(self):
        return self.df_original

    def activateDataframe(self, mode):
        if(mode=='Original'):
            self.df_active=self.df_original
            self.active_mode='Original'
            self.unit=1
            return
        if(mode=='PercentChange'):
            self.df_active=self.df_percent_change
            self.active_mode='PercentChange'
            self.unit=0.1
            return
    def getActive(self):
        return self.df_active
    def get_percent_change(self, df, column, group, By):
        dff=df.copy()
        dff[column]=df[column].astype(float)
        dff[column]=df.groupby(group)[By].apply(lambda x: x.div(x.iloc[0]).subtract(1).mul(100))
        
        return dff
    def get_percent_change_simple(self, column):
        dff=self.df_original.copy()
        dff[column].pct_change()
        result=dff.copy()
        return result
    def get_active_mode(self):
        return self.active_mode
    def modify_percent_change(self, filter, group, by):
        #Filter will be a column. For every element in that column, we'll do the percent change thing. So we have to filter one by one. 
        if(type(filter) is list):
            if(len(filter)==2):
                firstFilter=self.df_original[filter[0]].unique()
                secondFilter=self.df_original[filter[1]].unique()
                dataframes=[]
                for element in firstFilter:
                    for filtering in secondFilter:
                        dff=self.df_original[(self.df_original[filter[0]]==element) & (self.df_original[filter[1]]==filtering)]
                        df=dff.copy()
                        df[by]=df.groupby(group)[by].apply(lambda x: x.div(x.iloc[0]).subtract(1).mul(100))
                        dataframes.append(df)
                df_rest=pd.concat(dataframes)
                self.df_percent_change=df_rest
                return
            if(len(filter)==3):
                firstFilter=self.df_original[filter[0]].unique()
                secondFilter=self.df_original[filter[1]].unique()
                thirdFilter=self.df_original[filter[2]].unique()
                dataframes=[]
                for element in firstFilter:
                    for filtering in secondFilter:
                        for filteringTwo in thirdFilter:
                            dff=self.df_original[(self.df_original[filter[0]]==element) & (self.df_original[filter[1]]==filtering) & (self.df_original[filter[2]==filteringTwo])]
                            df=dff.copy()
                            df[by]=df.groupby(group)[by].apply(lambda x: x.div(x.iloc[0]).subtract(1).mul(100))
                            dataframes.append(df)
                df_rest=pd.concat(dataframes)
                self.df_percent_change=df_rest
                return
            if(len(filter)==4):
                firstFilter=self.df_original[filter[0]].unique()
                secondFilter=self.df_original[filter[1]].unique()
                thirdFilter=self.df_original[filter[2]].unique()
                fourthFilter=self.df_original[filter[3]].unique()
                dataframes=[]
                for element in firstFilter:
                    for filtering in secondFilter:
                        for filteringTwo in thirdFilter:
                            for filteringThree in fourthFilter:
                                try:
                                    dff=self.df_original[(self.df_original[filter[0]]==element) & (self.df_original[filter[1]]==filtering) & (self.df_original[filter[2]==filteringTwo]) & (self.df_original[filter[3]==filteringThree])]
                                except:
                                    continue
                                df=dff.copy()
                                df[by]=df.groupby(group)[by].apply(lambda x: x.div(x.iloc[0]).subtract(1).mul(100))
                                dataframes.append(df)
                df_rest=pd.concat(dataframes)
                self.df_percent_change=df_rest
                return

        elements=self.df_original[filter].unique()
        dataframes=[]
        for element in elements:
            dff=self.df_original[self.df_original[filter]==element]
            df=dff.copy()
            df[by]=df.groupby(group)[by].apply(lambda x: x.div(x.iloc[0]).subtract(1).mul(100))
            dataframes.append(df)
        df_rest=pd.concat(dataframes)
        self.df_percent_change=df_rest
    def trim(self, max, min):
        if(max==self.max and min==self.min):
            self.reset()
            return
        self.trimMax=max
        self.trimMin=min
        self.trimmed=True
    def isTrimmed(self):
        return self.trimmed
    def reset(self):
        self.trimMax=None
        self.trimMin=None
        self.trimmed=False
    def getMin(self):
        return self.min
    def getMax(self):
        return self.max

        
