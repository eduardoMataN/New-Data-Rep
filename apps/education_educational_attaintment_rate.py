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
df_edu=pd.read_excel(DATA_PATH.joinpath('Educational Attainment and Rate.xlsx'))

layout=html.Div(children=[
    dbc.Container(children=[
        dbc.Row([
            dbc.Col([
                html.H2(['Educational Attainment Rate by County'], style=TITLE)
            ])
        ])
    ]),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Label(['County'], style=LABEL),
                dcc.Dropdown(
                    id='select-county-edu',
                    options=[{'label':x,'value':x}for x in df_edu['County'].unique()],
                    value=df_edu['County'].unique()[0],
                    style=DROPDOWN,
                    optionHeight=90
                )
            ]),
            dbc.Col([
                html.Label(['Age'], style=LABEL),
                dcc.Dropdown(
                    id='select-age-edu',
                    options=[{'label':x,'value':x}for x in df_edu['Age'].unique()],
                    value=df_edu['Age'].unique()[0],
                    style=DROPDOWN,
                    optionHeight=90
                )
            ])
        ])
    ]),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Graph(
                        id='line-edu',
                        figure={}
                    )
                ])
                
            ])
        ]),
        dbc.Row([
            dbc.Col([
                html.Div([
                html.Label(['Year'], style=LABEL),
                    dcc.Dropdown(
                        id='select-year-educ',
                        options=[{'label':x,'value':x}for x in df_edu['Year'].unique()],
                        value=df_edu['Year'].unique()[0],
                        style=DROPDOWN,
                        optionHeight=90
                    ),
                    dash_table.DataTable(
                        id='educ-table',
                        columns=[{'name':i, 'id':i} for i in df_edu[(df_edu['County']==df_edu['County'].unique()[0]) &(df_edu['Age']==df_edu['Age'].unique()[0])&(df_edu['Year']==df_edu['Year'].unique()[0])][['Educational Attainment', 'Percentage']].columns],
                        data=df_edu[(df_edu['County']==df_edu['County'].unique()[0]) &(df_edu['Age']==df_edu['Age'].unique()[0])&(df_edu['Year']==df_edu['Year'].unique()[0])][['Educational Attainment', 'Percentage']].to_dict('records'),
                        editable=True,
                        filter_action='native',
                        sort_action='native',
                        sort_mode='multi',
                        row_selectable=False,
                        row_deletable=False,
                        selected_columns=[],
                        selected_rows=[],
                        page_size=10,
                        style_cell={'textAlign': 'left'},
                        style_header=LABEL
                    )
                ])
            ])
        ])
    ])
])

@app.callback(
    [Output('line-edu', 'figure'),
    Output('educ-table','data'),
    Output('educ-table', 'columns')],
    [Input('select-county-edu','value'),
    Input('select-age-edu','value'),
    Input('select-year-educ','value')]
    
)
def update_data(county, age,year):
    dff=df_edu.copy()
    fig=px.line(dff[(dff['County']==county)&(dff['Age']==age)], x='Year', y='Value', color='Educational Attainment')
    fig.update_xaxes( rangeslider_visible=True)
    toTable=df_edu[(df_edu['County']==county) &(df_edu['Age']==age)&(df_edu['Year']==year)][['Educational Attainment', 'Percentage']]
    columns=[{'name':i, 'id':i} for i in toTable.columns]
    data=toTable.to_dict('records')
    return fig, data, columns