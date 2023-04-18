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


layout=html.Div(children=[
    html.Div(id='sidebar-space-bc',children=[
        html.Div(
    [
        html.H6(id='sidebar-title-bc',children='Border Crossings Chart'),
        html.Hr(),
        html.P(
            "Use the following buttons to edit the chart.", className="lead"
        ),
        dbc.RadioItems(
            id='chart-options-bc',
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
        html.Br(),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H1(id='section-title', children=['Border Crossings'], style={'color':'#041E42'})
                ]),
                width=3
            ),
            dbc.Col(
                width=4
            ),
            
            
            dbc.Col()
        ],className="g-0")
    ]),
    
    
    
    dbc.Container(children=[
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.Label(['Indicator'], style={'font-weight':'bold', 'color':'#041E42'}),
                    dcc.Dropdown(id='select-indicator',
                                options=[{'label':x, 'value':x} for x in sorted(df.Measure.unique())],
                                multi=False,
                                value=df['Measure'].tolist()[0],
                                style={'width':'100%'},
                                optionHeight=90)
                ])
                
            , style={'margin-right': '3px', 'margin-left': '5px'},),
            dbc.Col([
                html.Div([
                    
                    dbc.Button('Edit Graph', id='edit-bc', outline=True, color="primary", className="me-1", value='monthly')
                ], )
            ], style={'margin-right': '1px', 'margin-left': '1px'},width=2),
            dbc.Col([
                html.Div([
                    
                    dbc.Button('Reset', id='reset-bc', outline=True, color="primary", className="me-1", value='reset')
                ])
            ], width=1, style={'margin-right': '0px', 'margin-left': '0px'}),
            
            
        ]),

    ]),
    
    dbc.Container(children=[
        dbc.Row([
            
            dbc.Col([
                html.Div([
                    dcc.Graph(id='graph', figure={})
                ]),
                
                ]),
            
            
        ])
    ]),
    dbc.Container([
        dbc.Row([
            dbc.Col([
            html.Div(children=[
                dbc.Row([
                    dbc.Col([
                        html.P(' Units: Individuals', style={'color':blue, 'font-weight':'bold'})
                    ], width=3),
                    dbc.Col([
                        html.P('Last Update: June 2022', style={'color':blue, 'font-weight':'bold'})
                    ], width=3),
                    dbc.Col([
                        html.P('Source: USA Gov', style={'color':blue, 'font-weight':'bold'})
                    ], width=3),
                    dbc.Col([
                    html.Div([
                        dbc.Button('Download Dataset', id='download-bttn-bc', outline=True, color="primary", className="me-1", value='yearly', n_clicks=0)
                    ]),
                    dcc.Download(id='download-bc')
            ],  style={'margin-left': '0px', 'margin-right':'1px'})
                ], align='center', justify='center', style={"height": "100%"}),
                dbc.Row([
                    dbc.Col([
                        html.P('Hidden', style={'color':'#FFFFFF'})
                    ])
                ],style={"height": "50%"})
            ])
            ], style={'margin-right': '3px', 'margin-left': '5px'}),
            dbc.Col(
                html.Div([
                    #html.Label(['Current'], style=LABEL),
                    daq.LEDDisplay(id='Number1', value=initialValue, color='#FF8200',labelPosition='bottom',)
                ]),width=2
                
            ),
        ], align='center', justify='center'),
    html.Br(),
    ]),
 ]
)

@app.callback(
    Output('download-bc','data'),
    Input('download-bttn-bc', 'n_clicks'),
    prevent_initial_call=True
)
def download_median(downloadB): 
 
    return dcc.send_data_frame(df.to_excel, 'Border Crossings.xlsx') 
