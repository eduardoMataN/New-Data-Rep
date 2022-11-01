
import pandas as pd
import plotly.express as px
import dash as dash
from dash import dcc, ctx
from dash import html
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash.dependencies import Input, Output, State
import pathlib
from app import app
import plotly.graph_objects as go
from plotly.subplots import make_subplots


blue='#041E42'
orange='#FF8200'
LABEL={'font-weight':'bold', 'color':'#041E42'}
TITLE={'color':'#041E42'}
DROPDOWN={'width':'100%'}

tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#FF8200',
    'color': 'white',
    'padding': '6px'
}

PATH = pathlib.Path(__file__).parent #So this first line is going to the parent of the current path, which is the Multipage app. 
 #Once we're on that path, we go into datasets. 
def create_subplot(fig,row, col, df, xaxes, yaxes, names):
    df_sub=df.copy()
    legend=df_sub[names].unique()
    for name in legend:
        df_ind=df_sub[df_sub[names]==name]
        x=df_ind[xaxes]
        y=df_ind[yaxes]
        if(col>1 or row>1):
            fig.add_trace(go.Scatter(x=x, y=y, name=name, legendgroup='group1', showlegend=False), row=row, col=col)
        else:
            fig.add_trace(go.Scatter(x=x, y=y, name=name, legendgroup='group1'), row=row, col=col)
    return fig
def get_options(df, col):
    return [{'label':x,'value':x}for x in df[col].unique()]
def filter_df(df, col, value):
    return df[df[col]==value]
def sum_df(df, sumCol, sumBy, target):
    newDf={sumBy:[], sumCol:[], target:[]}
    colValues=df[sumCol].unique()
    sumByValues=df[sumBy].unique()
    for sumValue in sumByValues:
        for value in colValues:
            df_temp=filter_df(df, sumBy, sumValue)
            df_temp=filter_df(df_temp, sumCol, value)
            newDf[sumBy].append(sumValue)
            newDf[sumCol].append(value)
            newDf[target].append(sum(df_temp[target]))
   
    return pd.DataFrame.from_dict(newDf)






