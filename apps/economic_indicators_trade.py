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
df_trade_hs= pd.read_excel(DATA_PATH.joinpath("Imports & Exports by HS Commodities, yearly.xlsx"))
df_trade_naics=pd.read_excel(DATA_PATH.joinpath("Exports & Imports by NAICS Commodities, yearly.xlsx"))
df_ep=pd.read_excel(DATA_PATH.joinpath("Total Flows to El Paso.xlsx"))


SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "margin-left": "0rem",
    "margin-right": "0rem",
    "padding": "0rem 0rem",
}

layout=html.Div(children=[
    dbc.Container(children=[
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H2(['Imports & Exports by HS Commodities'], style=TITLE)
                ])
            ])
        ]),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Label(['Measures'], style=LABEL),
                    dcc.Dropdown(
                        id='select-measures-int',
                        options=[{'label':x, 'value':x}for x in df_trade_hs['Measures'].unique()],
                        multi=False,
                        value=df_trade_hs['Measures'].unique()[0],
                        style=DROPDOWN,
                        optionHeight=90,
                        disabled=False
                    )
                ])
            ]),
            dbc.Col([
                html.Div([
                    html.Label(['Commodity'], style=LABEL),
                    dcc.Dropdown(
                        id='select-comm-int',
                        options=[{'label':x, 'value':x}for x in df_trade_hs['Commodity'].unique()],
                        value=df_trade_hs['Commodity'].unique()[0],
                        style=DROPDOWN,
                        optionHeight=90,
                        disabled=False
                    )
                ])
            ]),
            dbc.Col([
                html.Div([
                    daq.ToggleSwitch(
                        id='toggle-int',
                        label='Imports/Exports',
                        labelPosition='bottom',
                        value=False,
                        style=LABEL,
                        disabled=False
                    )
                ])
            ], width=1),
            dbc.Col([
                html.Div([
                    daq.ToggleSwitch(
                        id='toggle-int-2',
                        label='HS/NAICS',
                        labelPosition='bottom',
                        value=False,
                        style=LABEL
                    )
                ])
            ], width=1),
            dbc.Col([
                html.Div([
                    dcc.Dropdown(
                        id='compare-port1',
                        options=[{'label':x, 'value':x}for x in df_trade_hs['Port'].unique()],
                        value=df_trade_hs['Port'].unique()[0],
                        disabled=True,
                        style=DROPDOWN,
                        optionHeight=90
                    )
                ])
            ]),
            dbc.Col([
                html.Div([
                    daq.PowerButton(
                        id='pwr-int',
                        on=False,
                        color='#FF5E5E',
                        label='Compare',
                        style=LABEL,
                        labelPosition='bottom'
                    )
                ])
            ], width=1),
            dbc.Col([
                html.Div([
                    dcc.Dropdown(
                        id='compare-port2',
                        options=[{'label':x,'value':x}for x in df_trade_hs['Port'].unique()],
                        value=df_trade_hs['Port'].unique()[0],
                        disabled=True,
                        style=DROPDOWN,
                        optionHeight=90
                    )
                ])
            ])
        ])
    ]),
    dbc.Container(children=[
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Graph(id='hs-naics-graph', figure={})
                ])
            ])
        ])
    ]),
    dbc.Container(children=[
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H2(['Total Flows to El Paso'], style=TITLE)
                ])
            ])
        ])
    ]),
    dbc.Container(children=[
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Graph(
                        id='ep-graph',
                        figure={}
                    )
                ])
            ]),
            dbc.Col([
                html.Div([
                    html.Label(['Mode'], style=LABEL),
                    dcc.Dropdown(
                        id='select-mode-int',
                        options=[{'label':x, 'value':x}for x in df_ep['Mode'].unique()],
                        value=df_ep['Mode'].unique()[0],
                        style=DROPDOWN,
                        optionHeight=90
                    ),
                    html.Br(),
                    daq.LEDDisplay(
                        id='led-ep',
                        value=5,
                        label='Total Flows',
                        color=orange,
                        size=35,
                        style=LABEL
                    )
                
            
                ])
            ], width=4)
        ])
    ])
])

@app.callback(
    [
        Output('hs-naics-graph','figure'),
        Output('compare-port1','disabled'),
        Output('compare-port2', 'disabled'),
        Output('toggle-int','disabled'),
        Output('select-measures-int','options'),
        Output('select-measures-int','value'),
        Output('select-comm-int','options'),
        Output('select-comm-int','value'),
        Output('compare-port1','options'),
        Output('compare-port1','value'),
        Output('compare-port2','options'),
        Output('compare-port2','value'),
        Output('ep-graph','figure'),
        Output('led-ep','value')
    ],[
        Input('select-measures-int', 'value'),
        Input('select-comm-int','value'),
        Input('select-measures-int','options'),
        Input('pwr-int','on'),
        Input('toggle-int','value'),
        Input('toggle-int-2','value'),
        Input('compare-port1','value'),
        Input('compare-port2','value'),
        Input('select-comm-int', 'options'),
        Input('compare-port1','options'),
        Input('compare-port2','options'),
        Input('select-mode-int','value')
    ]
)
def update_data(measureValue, commodityValue, measureOptions, compareOn, toggleImEx,toggleHsNaics, portValue1, portValue2, commodityOptions, portOptions1, portOptions2, mode):
    #Chunk to update Top Part of Page. 
    comparePort1=True
    comparePort2=True
    importsToggle=False
    naicsDropdown=True
    trigger_id=ctx.triggered_id
    if(toggleHsNaics==True):
        dff=df_trade_naics.copy()
        naicsDropdown=False
        importsToggle=True
        if(trigger_id=='toggle-int-2'):
            measureOptions=[{'label':x,'value':x}for x in dff['Measures'].unique()]
            measureValue=dff['Measures'].unique()[0]
            commodityOptions=[{'label':x,'value':x}for x in dff['Commodity'].unique()]
            commodityValue=dff['Commodity'].unique()[0]
            portOptions1=[{'label':x,'value':x}for x in dff['District'].unique()]
            portValue1=dff['District'].unique()[0]
            portOptions2=[{'label':x,'value':x}for x in dff['District'].unique()]
            portValue2=dff['District'].unique()[1]
        if(compareOn==True):
            comparePort1=False
            comparePort2=False
            dff_compare=dff[(dff['Measures']==measureValue)&(dff['Commodity']==commodityValue)&(dff['District']==portValue1)]
            dff_compare2=dff[(dff['Measures']==measureValue)&(dff['Commodity']==commodityValue)&(dff['District']==portValue2)]
            fig=make_subplots(1,2)
            fig=create_subplot(fig, 1, 1, dff_compare, 'Year', 'Value', 'District')
            fig=create_subplot(fig, 1, 2, dff_compare2, 'Year', 'Value', 'District')
            
        else:
            fig=px.line(dff[(dff['Measures']==measureValue)&(dff['Commodity']==commodityValue)], x='Year', y='Value', color='District')
            
    else:
        dff=df_trade_hs.copy()
        if(trigger_id=='toggle-int-2'):
            measureOptions=[{'label':x,'value':x}for x in dff['Measures'].unique()]
            measureValue=dff['Measures'].unique()[0]
            commodityOptions=[{'label':x,'value':x}for x in dff['Commodity'].unique()]
            commodityValue=dff['Commodity'].unique()[0]
            portOptions1=[{'label':x,'value':x}for x in dff['Port'].unique()]
            portValue1=dff['Port'].unique()[0]
            portOptions2=[{'label':x,'value':x}for x in dff['Port'].unique()]
            portValue2=dff['Port'].unique()[1]
        if(compareOn):
            comparePort1=False
            comparePort2=False
            fig=make_subplots(1,2)
            if(toggleImEx):
                fig=create_subplot(fig, 1, 1, dff[(dff['Port']==portValue1)&(dff['Measures']==measureValue)&(dff['Commodity']==commodityValue)], 'Year', 'Exports','Port')
                fig=create_subplot(fig, 1, 2, dff[(dff['Port']==portValue2)&(dff['Measures']==measureValue)&(dff['Commodity']==commodityValue)], 'Year', 'Exports','Port')
            else:
                fig=create_subplot(fig, 1, 1, dff[(dff['Port']==portValue1)&(dff['Measures']==measureValue)&(dff['Commodity']==commodityValue)], 'Year', 'Imports','Port')
                fig=create_subplot(fig, 1, 2, dff[(dff['Port']==portValue2)&(dff['Measures']==measureValue)&(dff['Commodity']==commodityValue)], 'Year', 'Imports','Port')
        else:
            if(toggleImEx):
                fig=px.line(dff[(dff['Measures']==measureValue)&(dff['Commodity']==commodityValue)], x='Year', y='Exports', color='Port')
            else:
                fig=px.line(dff[(dff['Measures']==measureValue)&(dff['Commodity']==commodityValue)], x='Year', y='Imports', color='Port')
    #Chunk to Update Second Section:
    dff_ep=df_ep.copy()
    fig2=px.line(dff_ep[dff_ep['Mode']==mode], x='Year', y="Total", color='Commodity')
    total_f=round(sum(dff_ep[dff_ep['Mode']==mode]['Total']),1)
    fig2.update_xaxes(tick0=1, dtick=1)
    return fig, comparePort1, comparePort2, importsToggle, measureOptions, measureValue, commodityOptions, commodityValue, portOptions1, portValue1, portOptions2, portValue2, fig2, total_f