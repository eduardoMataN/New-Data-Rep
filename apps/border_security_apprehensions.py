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
DATA_PATH = PATH.joinpath("../datasets/Apprehensions").resolve()


df_cit=pd.read_excel(DATA_PATH.joinpath('Apprehensions by Citizenship.xlsx'))
df_country=pd.read_excel(DATA_PATH.joinpath('Apprehensions by Country.xlsx'))
df_uac=pd.read_excel(DATA_PATH.joinpath('Monthly UAC Apprehensions by Sector.xlsx'))
df_family=pd.read_excel(DATA_PATH.joinpath('Monthly Family Unit Apprehensions.xlsx'))
df_southwesta=pd.read_excel(DATA_PATH.joinpath('Southwest Border Apprehensions.xlsx'))
df_southwestb=pd.read_excel(DATA_PATH.joinpath('Southwest Border Deaths.xlsx'))

layout=html.Div([
    dbc.Container([
        dcc.Tabs(id='app-tabs', value='tab-cit', children=[
            dcc.Tab(label='By Citizenship', value='tab-cit', style=LABEL),
            dcc.Tab(label='By Country',value='tab-country', style=LABEL)
        ]),
    ]),
    html.Br(),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Label(id='sector-label', children=['Sector'], style=LABEL),
                    dcc.Dropdown(
                        id='select-sector',
                        options=[{'label':x, 'value':x}for x in df_cit['Sector'].unique()],
                        value=df_cit['Sector'].unique()[0],
                        multi=False,
                        style=DROPDOWN,
                        optionHeight=90
                    )
                ])
            ])
        ])
    ]),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Graph(
                        id='apprehensions-graph',
                        figure={}
                    )
                ])
            ])
        ])
    ])
])
@app.callback(
    [Output('apprehensions-graph', 'figure'),
    Output('select-sector','options'),
    Output('select-sector','value')],
    [Input('select-sector','value'),
    Input('select-sector','options'),
    Input('app-tabs','value')]
)
def update_data(sectorValue, sectorOptions, currentTab):
    trigger_id=ctx.triggered_id
    if(currentTab=='tab-cit'):
        dff=df_cit.copy()
        if(trigger_id=='app-tabs'):
            sectorOptions=get_options(dff, 'Sector')
            sectorValue=dff['Sector'].unique()[0]
        fig=px.line(dff[dff['Sector']==sectorValue], x='Year', y='Apprehensions', color='Citizenship')
    if(currentTab=='tab-country'):
        dff=df_country.copy()
        if(trigger_id=='app-tabs'):
            sectorOptions=get_options(dff, 'Sector')
            sectorValue=dff['Sector'].unique()[0]
        fig=px.line(dff[dff['Sector']==sectorValue], x='Year', y='Illegal Alien Apprehensions', color='Country')   
    return fig, sectorOptions, sectorValue