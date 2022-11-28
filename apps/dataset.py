class dataset:
    df_original=None
    df_percent_change=None
    df_active=None
    title=''
    def __init__(self, title, df_original, df_percent_change):
        self.df_original=df_original
        self.title=title
        self.df_percent_change=df_percent_change
        self.df_active=df_original

    def activateDataframe(self, mode):
        if(mode=='Original'):
            self.df_active=self.df_original
            return
        if(mode=='PercentChange'):
            self.df_active=self.df_percent_change
            return
    def getActive(self):
        return self.df_active
