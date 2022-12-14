
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
from apps.dataset import *
from apps.dataBag import *

PATH = pathlib.Path(__file__).parent #So this first line is going to the parent of the current path, which is the Multipage app. 
DATA_PATH = PATH.joinpath("../datasets").resolve() #Once we're on that path, we go into datasets. 
df_emp= pd.read_excel(DATA_PATH.joinpath("Total Employment by Industry, County.xlsx"))
employmentDataset=dataset('Employment by Industry Chart', df_emp, 'Value', 'totalEmp', 'County', 'Value')
employmentDataset.modify_percent_change('County', 'Description', 'Value')
employmentDatabag=dataBag([employmentDataset])
df_total=pd.read_excel(DATA_PATH.joinpath("Total Employment by County, LBS.xlsx"))
df_unemp=pd.read_excel(DATA_PATH.joinpath("Unemployment by County.xlsx"))



layout=html.Div(children=[
    html.Div(id='sidebar-space-emp',children=[
        html.Div(
    [
        html.H6(id='sidebar-title-emp',children='Employment by Industry Chart'),
        html.Hr(),
        html.P(
            "Use the following buttons to edit the chart.", className="lead"
        ),
        dbc.RadioItems(
            id='chart-options-emp',
            options=[
                {'label':'Percent Change','value':'PercentChange'},
                {'label': 'Original Chart','value':'Original'}
            ],
            value='Original',
            
        ),
        


        
    ],
    style=SIDEBAR_STYLE,
    )
    ], hidden=True),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H2(['Employment by Industry'], style=TITLE)
                ])
            ])
        ])
    ]),
    dbc.Container(children=[
        dbc.Row([
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
            ], width=5),
            dbc.Col([
                html.Div([
                    daq.PowerButton(
                            id='emp-monthly-pw',
                            on=False,
                            label='Monthly Data',
                            style=LABEL
                        )
                ])
            ], width=2),
            dbc.Col([
                html.Div([
                    daq.LEDDisplay(
                    id='led-unemp',
                    label='Unemployment',
                    value=5,
                    style={'color':'#FF8200', 'font-weight':'bold'},
                    color=blue
                )
                ])
            ], width=5)
        ]),
        html.Br(),
        dbc.Row([
            html.Div(children=[
                dbc.Row([
                    dbc.Col([
                        html.P('Units: Amount of Individuals', style={'color':blue, 'font-weight':'bold'})
                    ]),
                    dbc.Col(
                        html.P('Last Update: March 2022', style={'color':blue, 'font-weight':'bold'})
                    ),
                    dbc.Col(
                        html.P('Source: USA Gov', style={'color':blue, 'font-weight':'bold'})
                    )
                ])
            ], )
        ]),
        html.Br(),
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
            ]),
            dbc.Col([
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
            ]),
            dbc.Col([
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
                    ]),
            ]),
            dbc.Col([
                html.Div([
                    dbc.Button('Edit Graph', id='edit-emp', outline=True, color="primary", className="me-1", value='yearly', n_clicks=0)
                ])
            ], width=2)
            
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
    ]),
    dbc.Container([
        dbc.Row([
            dbc.Col([
            html.Div(children=[
                dbc.Row([
                    dbc.Col([
                        
                    ], width=2),
                    dbc.Col([
                        html.P(' Units: Individuals', style={'color':blue, 'font-weight':'bold'})
                    ], width=3),
                    dbc.Col([
                        html.P('Last Update: 2020', style={'color':blue, 'font-weight':'bold'})
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

@app.callback(
    Output('sidebar-space-emp','hidden'),
    [Input('edit-emp', 'n_clicks'),
    Input('sidebar-space-emp', 'hidden'),
    Input('chart-options-emp', 'value')]
)
def get_sidebar(button, hideSideBar, graphMode):
    trigger_id=ctx.triggered_id
    if(trigger_id=='edit-emp'):
        if(hideSideBar):
            hideSideBar=False
        else:
            hideSideBar=True
    employmentDatabag.getDataframe().activateDataframe(graphMode)

    
    return hideSideBar

@app.callback(
    [
        Output(component_id='led-emp', component_property='value'), Output(component_id='led-unemp', component_property='value'),
        Output(component_id='emp-month-select', component_property='disabled'),
        Output('employment-graph', 'figure')
    ],
    [
        Input(component_id='emp-monthly-pw', component_property='on'),
        Input(component_id='emp-county-select', component_property='value'),
        Input(component_id='emp-year-select', component_property='value'),
        Input(component_id='emp-month-select', component_property='value'),
        Input('chart-options-emp','value')
    ]
)
def update_data(empPw, countyEmp, yearEmp, monthEmp, dummyValue):
    emp=0
    unemp=0
    dfemp=df_total.copy()
    dfunemp=df_unemp.copy()
    monthSE=False
    monthSU=False
    if(empPw):
        monthSE=False
        emp=sum(dfemp[(dfemp['County']==countyEmp) & (dfemp['Year']==yearEmp) & (dfemp['Period']==monthEmp)]['Value'])
        unemp=sum(dfunemp[(dfunemp['County']==countyEmp) & (dfunemp['Year']==yearEmp) & (dfunemp['Month']==monthEmp)]['Unemployed'])
    else:
        monthSE=True
        emp=sum(dfemp[(dfemp['County']==countyEmp) & (dfemp['Year']==yearEmp)]['Value'])
        unemp=sum(dfunemp[(dfunemp['County']==countyEmp) & (dfunemp['Year']==yearEmp)]['Unemployed'])
    dff=employmentDatabag.getDataframe().getActive().copy()
    fig=make_subplots(1,1)
    fig=create_subplot(fig, 1, 1, filter_df(dff, 'County', countyEmp), 'Year', 'Value', 'Description')
    
    fig.update_layout(height=700)
    fig.update_xaxes(rangeslider_visible=True)
    return emp, unemp, monthSE, fig