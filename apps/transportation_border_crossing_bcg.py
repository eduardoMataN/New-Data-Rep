import pandas as pd
import plotly.express as px
import dash as dash
from dash import dcc, ctx
from dash import html, dash_table
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash.dependencies import Input, Output, State
import pathlib
import plotly.graph_objects as go
from app import app
from apps.common_items import *
from apps.dataset import *
from apps.dataBag import *

PATH = pathlib.Path(__file__).parent #So this first line is going to the parent of the current path, which is the Multipage app. 
DATA_PATH = PATH.joinpath("../datasets").resolve() #Once we're on that path, we go into datasets. 
df= pd.read_excel(DATA_PATH.joinpath("Border Crossings.xlsx"))
borderCDataSet=dataset('Border Crossings', df, 'Value', 'graph', 'Port', 'Value')
borderCDataSet.modify_percent_change('Measure', 'Port', 'Value')
boderDataBag=dataBag([borderCDataSet])
df['Value']=pd.to_numeric(df['Value'])
df_copy=df.copy()
maxYear=df['Year'].max()
df_copy=df[df['Measure']=='Truck Containers Empty']
initialValue=sum(df_copy.loc[df_copy.Year==maxYear, 'Value'].tolist())
df_current=df[df['Year']==df['Year'].max()]
df_profiler=df_current[df_current['Port']==sorted(df['Port'].unique())[0]]


toTable=df_profiler[['Measure', 'Month', 'Value']]

layout=html.Div(children=[
    html.Br(),
    dbc.Container(children=[
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H1(id='profiler-title',children=[('Port Analyzer')], style={'color':'#041E42'}),
                ])
            ], width=2),
        ], className="g-0"),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Label('Port', style={'font-weight':'bold'}),
                    dcc.Dropdown(id='county-prof-selector', 
                    options=[{'label':x, 'value':x} for x in sorted(df['Port'].unique())],
                    multi=False,
                    value=sorted(df['Port'].unique())[0])
                ])
            ]),
            dbc.Col([
                html.Div([
                    html.Label('Year', style={'font-weight':'bold'}),
                    dcc.Dropdown(id='Year-selector',
                    options=[{'label':i, 'value':i} for i in sorted(df['Year'].unique())],
                    multi=False,
                    value=sorted(df['Year'].unique())[0])
                ])
            ]),
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col([
                html.Div(id='table-loc',children=[
                    dash_table.DataTable(
                        id='profiler-table',
                        columns=[{'name':i, 'id':i} for i in toTable.columns],
                        data=toTable.to_dict('records'),
                        editable=True,
                        filter_action='native',
                        sort_action='native',
                        sort_mode='multi',
                        row_selectable=False,
                        row_deletable=False,
                        selected_columns=[],
                        selected_rows=[],
                        page_size=10,
                    )
                ])
            ]),
            dbc.Col([
                html.Div([
                    dcc.Graph(id='bar-chart', figure={})
                ])
            ])
        ]),
        html.Br(),
    dbc.Container([
        dbc.Row([
            dbc.Col([
            html.Div(children=[
                dbc.Row([
                    dbc.Col([
                        
                    ], width=2),
                    dbc.Col([
                        html.P(' Units: Dollars ($)', style={'color':blue, 'font-weight':'bold'})
                    ], width=3),
                    dbc.Col([
                        html.P('Last Update: June 2022', style={'color':blue, 'font-weight':'bold'})
                    ], width=3),
                    dbc.Col([
                        html.P('Source: USA Gov', style={'color':blue, 'font-weight':'bold'})
                    ], width=3)
                ], align='center', justify='center')
            ])
            ]),
        ], align='center', justify='center'),
        html.Br(),
    html.Br(),
    ]),
    ])

    
]
)