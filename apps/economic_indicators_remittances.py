
import pandas as pd
import plotly.express as px
import dash as dash
from dash import dcc, ctx
from dash import html, dash_table
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash.dependencies import Input, Output, State
import pathlib
from app import app
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from apps.common_items import *

PATH = pathlib.Path(__file__).parent #So this first line is going to the parent of the current path, which is the Multipage app. 
DATA_PATH = PATH.joinpath("../datasets").resolve() #Once we're on that path, we go into datasets. 
df_rem=pd.read_excel(DATA_PATH.joinpath('Worker Remittances Juarez.xlsx'))

layout=html.Div(children=[
    dbc.Container(children=[
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H2(id='rem-title',children=['Revenues by Workers Remittances. Juarez Unit.'], style={'color':'#041E42'})
                ])
            )
        ]),
        dbc.Row([
            dbc.Col(
                dcc.Graph(id='rem-graph', figure={})
            )
        ])
    ])
])

@app.callback(
    Output('rem-graph', 'figure'),
    Input('rem-title', 'children')
    
)
def update_data(title):
    dff=df_rem.copy()
    fig=px.line(dff, x='Year', y='Value')
    fig.update_xaxes(nticks=len(pd.unique(dff['Year'])), rangeslider_visible=True)
    return fig