from turtle import width
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
DATA_PATH = PATH.joinpath("../datasets/Border Patrol Agent Staffing").resolve()

df_region=pd.read_excel(DATA_PATH.joinpath('Staffing by region.xlsx'))
df_sector=pd.read_excel(DATA_PATH.joinpath('Staffing by Sector.xlsx'))

layout=html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H2(['Border Patrol Agent Staffing'], style=TITLE)
            ])
        ])
    ]),
    dbc.Container([
        dcc.Tabs(id='select-indicator', value='region', children=[
            dcc.Tab(label='By Region', value='region', style=LABEL),
            dcc.Tab(label='By Sector', value='sector', style=LABEL)
        ])
    ]),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Graph(
                        id='staffing-graph',
                        figure={}
                    )
                ])
            ])
        ])
    ])
])