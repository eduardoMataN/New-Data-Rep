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

PATH = pathlib.Path(__file__).parent #So this first line is going to the parent of the current path, which is the Multipage app. 
DATA_PATH = PATH.joinpath("../datasets").resolve() #Once we're on that path, we go into datasets. 
df_est=pd.read_excel(DATA_PATH.joinpath('Number of Establishments.xlsx'))
toTable=df_est[df_est['Year']==df_est['Year'][0]][['County', 'Period', 'Value']]

layout=html.Div(children=[
    dbc.Container(children=[
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H2(id='title',children=['Number of Business Stablishments by Year'], style={'color':blue})
                ])
            )
        ]),
        dbc.Row([
            dbc.Col(
                dcc.Graph(id='line-1', figure={})
            )
            
        ]),
        dbc.Row([
            dbc.Col(
                html.Div(
                    dcc.Dropdown(
                        id='select-county-ind',
                        options=[{'label':x, 'value':x} for x in df_est['County'].unique()],
                        multi=False,
                        value=df_est['County'].unique()[0],
                        style={'width':'100%'},
                        optionHeight=90            
                    )
                )
            ),
            dbc.Col([
                html.Div(
                    dcc.Dropdown(
                        id='select-year-ind',
                        options=[{'label':x, 'value':x} for x in df_est['Year'].unique()],
                        value=df_est['Year'].unique()[0],
                        style={'width':'100%'},
                        optionHeight=90
                    )
                )
                    ])
        ]),
        html.Br(),
        dbc.Row(
            dbc.Col([
                html.Div(id='table-loc',children=[
                    dash_table.DataTable(
                        id='industry-table',
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
            ])
        )
    ])
])

@app.callback(
    
        
        [Output(component_id='line-1', component_property='figure'),
        Output('industry-table', 'data'), Output('industry-table', 'columns')]
    ,
    
        [Input('title', 'children'), Input('select-county-ind', 'value'),
        Input('select-year-ind', 'value')]
    
)
def update_data(title, countyT,yearT):
    dff=df_est.copy()
    finalFig=px.line(dff, x='Year', y='Value', color='County')
    finalFig.update_xaxes(nticks=len(pd.unique(dff['Year'])), rangeslider_visible=True)
    toTable=dff[(dff['Year']==yearT) & (dff['County']==countyT)][['County', 'Period', 'Value']]
    return finalFig, toTable.to_dict('records'), [{'name':i, 'id':i} for i in toTable.columns]