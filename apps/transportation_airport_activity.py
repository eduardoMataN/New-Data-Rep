
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
df_domes_int=pd.read_excel(DATA_PATH.joinpath('Jurez & Chihuahua.xlsx'))
df_ep=pd.read_excel(DATA_PATH.joinpath('El Paso Passengers 2012-2022.xlsx'))

layout=html.Div(children=[
    dbc.Container(children=[
        dbc.Row([
            dbc.Col([
                html.H2(['Domestic and International Air Passengers'], style=TITLE)
            ])
        ])
    ]),
    dbc.Container(children=[
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Label(['Municipality'], style=LABEL),
                    dcc.Dropdown(
                        id='select-mun-air',
                        options=[{'label':x, 'value':x}for x in df_domes_int['Municipality'].unique()],
                        value=df_domes_int['Municipality'].unique()[0],
                        multi=False,
                        style=DROPDOWN,
                        optionHeight=90,
                        disabled=False
                    )
                ])
            ]),
            dbc.Col([
                html.Div([
                    html.Label(['Type'], style=LABEL),
                    dcc.Dropdown(
                        id='select-type-air',
                        options=[{'label':x, 'value':x}for x in df_domes_int['Type'].unique()],
                        value=df_domes_int['Type'].unique()[0],
                        multi=False,
                        style=DROPDOWN,
                        optionHeight=90
                    )
                ])
            ]),
            dbc.Col(
                html.Div([
                    html.Label(['Year'], style=LABEL),
                    dcc.Dropdown(
                        id='select-year-air',
                        options=[{'label':x, 'value':x}for x in df_domes_int['Year'].unique()],
                        value=df_domes_int['Year'].unique()[0],
                        multi=False,
                        style=DROPDOWN,
                        optionHeight=90
                    )
                ])
            ),
            dbc.Col([
                html.Div([
                    daq.PowerButton(
                        id='air-pwr',
                        on=False,
                        label='Compare',
                        labelPosition='top',
                        style=LABEL,
                        color='#FF5E5E'
                    )
                ])
            ], width=1)
        ])
    ]),
    dbc.Container(children=[
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Graph(
                        id='bar-domes-int',
                        figure={}
                    )
                ])
            ])
        ])
    ]),
    dbc.Container(children=[
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H2(['El Paso Passengers Statistics'], style=TITLE)
                ])
            ])
        ])
    ]),
    dbc.Container(children=[
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Label(['Year'], style=LABEL),
                    dcc.Dropdown(
                        id='select-year-airep',
                        options=[{'label':x, 'value':x}for x in df_ep['Year'].unique()],
                        value=df_ep['Year'].unique()[0],
                        style=DROPDOWN,
                        optionHeight=90
                    )
                ])
            ])
        ]),
    ]),
    dbc.Container(children=[
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Graph(
                        id='bar-air',
                        figure={}
                    )
                ])
            ])
        ])
    ])
])

@app.callback(
    [Output('bar-air', 'figure'),
    Output('bar-domes-int','figure'),
    Output('select-mun-air', 'disabled')],
    [Input('select-year-airep', 'value'), 
    Input('select-mun-air', 'value'),
    Input('select-type-air','value'),
    Input('select-year-air', 'value'),
    Input('air-pwr','on')]
)
def update_data(yearEP, municipality, type, year, on):
    dff=df_ep.copy()
    dff=dff[dff['Year']==yearEP]
    fig=px.bar(dff, 'Month', 'Value', color='Type')
    munDis=False
    dff2=df_domes_int.copy()
    if(on==True):
        dff3=dff2[(dff2['Municipality']=='Ciudad Juárez')&(dff2['Year']==year)&(dff2['Type']==type)]
        dff4=dff2[(dff2['Municipality']=='Chihuahua')&(dff2['Year']==year)&(dff2['Type']==type)]
        fig2=make_subplots(1,2)
        fig2.add_trace(go.Bar(x=dff3['Month'], y=dff3['Value'], name='Ciudad Juárez'), 1, 1)
        fig2.add_trace(go.Bar(x=dff4['Month'], y=dff4['Value'], name='Chihuahua'), 1, 2)
        munDis=True
    else:
        dff2=dff2[(dff2['Municipality']==municipality)&(dff2['Year']==year)&(dff2['Type']==type)]
        fig2=px.bar(dff2, 'Month', 'Value', hover_data=['Value'], color='Value')
    return fig, fig2, munDis