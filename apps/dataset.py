class dataset:
    
    def __init__(self, title, df_original, column, name):
        self.df_original=df_original
        self.title=title
        self.df_percent_change=self.get_percent_change(df_original, column)
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
    def get_percent_change(self, df, column):
        dff=df.copy()
        dff[column]=dff[column].pct_change()
        
        return dff
