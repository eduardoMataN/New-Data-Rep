
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
from apps.common_items import *

PATH = pathlib.Path(__file__).parent #So this first line is going to the parent of the current path, which is the Multipage app. 
DATA_PATH = PATH.joinpath("../datasets").resolve() #Once we're on that path, we go into datasets. 
df_emp= pd.read_excel(DATA_PATH.joinpath("Total Employment by Industry, County.xlsx"))
df_total=pd.read_excel(DATA_PATH.joinpath("Total Employment by County, LBS.xlsx"))
df_unemp=pd.read_excel(DATA_PATH.joinpath("Unemployment by County.xlsx"))


layout=html.Div(children=[
    dbc.Container(children=[
        dbc.Row([
            html.Div([
                html.H2(['Employment vs. Unemployment'], style={'color':'#041E42'})
            ])
        ]),
        dbc.Row([
            dbc.Col([
                html.Div([
                        html.Label(['County'], style={'font-weight':'bold', 'color':'#041E42'}),
                        dcc.Dropdown(
                            id='emp-county-select',
                            options=[{'label':x, 'value':x} for x in df_total['County'].unique()],
                            multi=False,
                            value=df_total['County'].unique()[0],
                            style={'width':'100%'},
                            optionHeight=90
                        )
                    ]),
                
                
                    html.Div([
                        html.Label(['Year'], style={'font-weight':'bold', 'color':'#041E42'}),
                        dcc.Dropdown(
                            id='emp-year-select',
                            options=[{'label':x, 'value':x} for x in df_total['Year'].unique()],
                            multi=False,
                            value=df_total['Year'].unique()[0],
                            style={'width':'100%'},
                            optionHeight=90
                        )
                    ]),
                
                
                    html.Div([
                        html.Label(['Month'], style={'font-weight':'bold', 'color':'#041E42'}),
                        dcc.Dropdown(
                            id='emp-month-select',
                            options=[{'label':x, 'value':x} for x in df_total['Period'].unique()],
                            multi=False,
                            value=df_total['Period'].unique()[0],
                            style={'width':'100%'},
                            optionHeight=90,
                            disabled=True
                        ),
                        daq.PowerButton(
                            id='emp-monthly-pw',
                            on=False
                        )
                    ]),
            ]),
            dbc.Col([
                html.Div([
                    daq.LEDDisplay(
                        id='led-emp',
                        label='Employment',
                        value=5,
                        style={'color':'#FF8200', 'font-weight':'bold'},
                        color=blue
                    )
                ])
            ]),
            dbc.Col([
                daq.LEDDisplay(
                    id='led-unemp',
                    label='Unemployment',
                    value=5,
                    style={'color':'#FF8200', 'font-weight':'bold'},
                    color=blue
                )
            ]),
            dbc.Col([
                html.Div([
                    html.Label(['County'], style={'font-weight':'bold', 'color':'#041E42'}),
                        dcc.Dropdown(
                            id='unemp-county-select',
                            options=[{'label':x, 'value':x} for x in df_unemp['County'].unique()],
                            multi=False,
                            value=df_unemp['County'].unique()[0],
                            style={'width':'100%'},
                            optionHeight=90
                        )
                ]),
                html.Div([
                    html.Label(['Year'], style={'font-weight':'bold', 'color':'#041E42'}),
                        dcc.Dropdown(
                            id='unemp-year-select',
                            options=[{'label':x, 'value':x} for x in df_unemp['Year'].unique()],
                            multi=False,
                            value=df_unemp['Year'].unique()[0],
                            style={'width':'100%'},
                            optionHeight=90
                        )
                ]),
                html.Div([
                    html.Label(['Month'], style={'font-weight':'bold', 'color':'#041E42'}),
                        dcc.Dropdown(
                            id='unemp-month-select',
                            options=[{'label':x, 'value':x} for x in df_unemp['Month'].unique()],
                            multi=False,
                            value=df_unemp['Month'].unique()[0],
                            style={'width':'100%'},
                            optionHeight=90,
                            disabled=True
                        ),
                        daq.PowerButton(
                            id='unemp-monthly-pw',
                            on=False
                        )
                ])
            ])
        ])
    ]),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H2(['Employment by Industry'], style=TITLE)
                ])
            ])
        ])
    ]),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Graph(
                        id='employment-graph',
                        figure={}
                    )
                ])
            ])
        ])
    ])
])

@app.callback(
    [
        Output(component_id='led-emp', component_property='value'), Output(component_id='led-unemp', component_property='value'),
        Output(component_id='emp-month-select', component_property='disabled'), Output(component_id='unemp-month-select', component_property='disabled'),
        Output('employment-graph', 'figure')
    ],
    [
        Input(component_id='emp-monthly-pw', component_property='on'), Input(component_id='unemp-monthly-pw', component_property='on'),
        Input(component_id='emp-county-select', component_property='value'), Input(component_id='unemp-county-select', component_property='value'),
        Input(component_id='emp-year-select', component_property='value'), Input(component_id='unemp-year-select', component_property='value'),
        Input(component_id='emp-month-select', component_property='value'), Input(component_id='unemp-month-select', component_property='value')
    ]
)
def update_data(empPw, unemPw, countyEmp, countyUnemp, yearEmp, yearUnemp, monthEmp, monthUnemp):
    emp=0
    unemp=0
    dfemp=df_total.copy()
    dfunemp=df_unemp.copy()
    monthSE=False
    monthSU=False
    if(empPw):
        monthSE=False
        emp=sum(dfemp[(dfemp['County']==countyEmp) & (dfemp['Year']==yearEmp) & (dfemp['Period']==monthEmp)]['Value'])
    else:
        monthSE=True
        emp=sum(dfemp[(dfemp['County']==countyEmp) & (dfemp['Year']==yearEmp)]['Value'])
    if(unemPw):
        monthSU=False
        unemp=sum(dfunemp[(dfunemp['County']==countyUnemp) & (dfunemp['Year']==yearUnemp) & (dfunemp['Month']==monthUnemp)]['Unemployed'])
    else:
        monthSU=True
        unemp=sum(dfunemp[(dfunemp['County']==countyUnemp) & (dfunemp['Year']==yearUnemp)]['Unemployed'])
    dff=df_emp.copy()
    fig=make_subplots(2,1)
    fig=create_subplot(fig, 1, 1, filter_df(dff, 'County', countyEmp), 'Year', 'Value', 'Description')
    fig=create_subplot(fig, 2, 1, filter_df(dff, 'County', countyUnemp), 'Year', 'Value', 'Description')
    fig.update_layout(height=700)
    return emp, unemp, monthSE, monthSU, fig