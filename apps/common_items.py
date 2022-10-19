from turtle import width
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

PATH = pathlib.Path(__file__).parent #So this first line is going to the parent of the current path, which is the Multipage app. 
 #Once we're on that path, we go into datasets. 
def create_subplot(fig,row, col, df, xaxes, yaxes, names):
    df_sub=df.copy()
    legend=df_sub[names].unique()
    for name in legend:
        df_ind=df_sub[df_sub[names]==name]
        x=df_ind[xaxes]
        y=df_ind[yaxes]
        fig.add_trace(go.Scatter(x=x, y=y, name=name), row=row, col=col)
    return fig






