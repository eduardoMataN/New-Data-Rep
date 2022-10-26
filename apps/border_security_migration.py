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
DATA_PATH = PATH.joinpath("../datasets/Migration Indicators").resolve()

df_migration=pd.read_excel(DATA_PATH.joinpath('County to County Migration Flows 2009-2018.xlsx'))

layout=html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H2(['Migration Indicators'], style=TITLE)
                ])
            ])
        ])
    ]),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Label(['Migration Flow'], style=LABEL),
                    dcc.Dropdown(
                        id='select-flow',
                        options=get_options(df_migration, 'Migration'),
                        value=df_migration['Migration'].unique()[0],
                        multi=False,
                        style=DROPDOWN,
                        optionHeight=90
                    )
                ])
            ])
        ])
    ])
])