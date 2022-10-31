
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
df_crime=pd.read_excel(DATA_PATH.joinpath('Crime 2006 - 2019.xlsx'))



layout=html.Div(children=[
    dbc.Container(children=[
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H2(children=['Crime by County'], style={'color':'#041E42'})
                ])
            ])
        ]),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Label(['Crime'], style={'font-weight':'bold', 'color':'#041E42'}),
                    dcc.Dropdown(
                        id='select-type-cr',
                        options=[{'label':x, 'value':x}for x in df_crime['Crime Desctiption'].unique()],
                        value=df_crime['Crime Desctiption'].unique()[0],
                        style={'width':'100%'},
                        optionHeight=90
                    )
                ])
            ]),
            dbc.Col([
                html.Div([
                    html.Label(['County'], style=LABEL),
                    dcc.Dropdown(
                        id='select-county1-cr',
                        options=[{'label':x, 'value':x}for x in df_crime['County'].unique()],
                        value=df_crime['County'].unique()[0],
                        style=DROPDOWN,
                        optionHeight=90,
                        disabled=True
                    )
                ])
            ]),
            dbc.Col([
                html.Div([
                    daq.PowerButton(
                        id='sbs-cr',
                        on=False,
                        label='VS',
                        labelPosition='top',
                        style=LABEL,
                        color='#FF5E5E'
                    )
                ])
            ], width=1),
            dbc.Col([
                html.Div([
                    html.Label(['County'], style=LABEL),
                    dcc.Dropdown(
                        id='select-county2-cr',
                        options=[{'label':x, 'value':x}for x in df_crime['County'].unique()],
                        value=df_crime['County'].unique()[-1],
                        style=DROPDOWN,
                        optionHeight=90,
                        disabled=True
                    )
                ])
            ])
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    dcc.Graph(
                        id='cr-graph',
                        figure={}
                    )
                ])
            )
        ])
    ])
])

@app.callback(
    [
        Output('cr-graph', 'figure'),
        Output('select-county1-cr','disabled'),
        Output('select-county2-cr','disabled')
    ],
    [
        Input('select-type-cr','value'),
        Input('select-county1-cr','value'),
        Input('select-county2-cr', 'value'),
        Input('sbs-cr', 'on')
    ] 
)
def update_data(type, county1, county2, on):
    dff=df_crime.copy()
    dff=dff[dff['Crime Desctiption']==type]
    d1_dis=True
    d2_dis=True
    if(on==True):
        fig=make_subplots(rows=1, cols=2)
        dff1=dff[dff['County']==county1]
        dff2=dff[dff['County']==county2]
        fig=create_subplot(fig,1,1,dff1,'Year','Number','County')
        fig=create_subplot(fig,1,2,dff2,'Year','Number','County')
        fig.update_xaxes(rangeslider= {'visible':True}, row=1, col=1)
        fig.update_xaxes(rangeslider= {'visible':True}, row=1, col=2)
        
        d1_dis=False
        d2_dis=False
    else:
        fig=px.line(dff,'Year','Number', color='County')
        fig.update_xaxes(rangeslider_visible=True)
    return fig, d1_dis, d2_dis