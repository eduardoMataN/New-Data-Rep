import pandas as pd
class dataset:
    
    def __init__(self, title, df_original, column, name, group, By):
        self.df_original=df_original
        self.title=title
        self.df_percent_change=self.get_percent_change(df_original, column, group, By)
        self.df_active=df_original
        self.name=name

    def activateDataframe(self, mode):
        if(mode=='Original'):
            self.df_active=self.df_original
            return
        if(mode=='PercentChange'):
            self.df_active=self.df_percent_change
            return
    def getActive(self):
        return self.df_active
    def get_percent_change(self, df, column, group, By):
        dff=df.copy()
        dff[column]=df.groupby(group)[By].apply(lambda x: x.div(x.iloc[0]).subtract(1).mul(100))
        
        return dff
    def modify_percent_change(self, filter, group, by):
        #Filter will be a column. For every element in that column, we'll do the percent change thing. So we have to filter one by one. 
        elements=self.df_original[filter].unique()
        dataframes=[]
        for element in elements:
            dff=self.df_original[self.df_original[filter]==element]
            df=dff.copy()
            df[by]=df.groupby(group)[by].apply(lambda x: x.div(x.iloc[0]).subtract(1).mul(100))
            dataframes.append(df)
        df_rest=pd.concat(dataframes)
        self.df_percent_change=df_rest
        
