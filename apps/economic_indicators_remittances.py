
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
from apps.dataset import *
from apps.dataBag import *

PATH = pathlib.Path(__file__).parent #So this first line is going to the parent of the current path, which is the Multipage app. 
DATA_PATH = PATH.joinpath("../datasets").resolve() #Once we're on that path, we go into datasets. 
df_rem=pd.read_excel(DATA_PATH.joinpath('Worker Remittances Juarez.xlsx'))
remDataset=dataset('Revenues by Workers Remittances Chart', df_rem, 'Value', name='remit', group='City', By='Value')
remDatabag=dataBag([remDataset])

layout=html.Div(children=[
    html.Div(id='sidebar-space-rem',children=[
        html.Div(
    [
        html.H6(id='sidebar-title-rem',children='Revenues by Workers Remittances Chart'),
        html.Hr(),
        html.P(
            "Use the following buttons to edit the chart.", className="lead"
        ),
        dbc.RadioItems(
            id='chart-options-rem',
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
    dbc.Container(children=[
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H2(id='rem-title',children=['Revenues by Workers Remittances. Juarez Unit.'], style={'color':'#041E42'})
                ])
            )
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col([
                html.Div(children=[
                dbc.Row([
                    dbc.Col([
                        html.P(' Units: Thousands of Dollars (K)', style={'color':blue, 'font-weight':'bold'})
                    ], width=4),
                    dbc.Col([
                        html.P('Last Update: June 2022', style={'color':blue, 'font-weight':'bold'})
                    ], width=4),
                    dbc.Col([
                        html.P('Source: USA Gov', style={'color':blue, 'font-weight':'bold'})
                    ], width=4)
                ], align='center',justify='center')
            ], style={"border":"2px black solid"})
            ]),
            dbc.Col([
                html.Div([
                    dbc.Button('Edit Graph', id='edit-rem', outline=True, color="primary", className="me-1", value='yearly', n_clicks=0)
                ])
            
            ], width=2),
        ], align='center', justify='center'),
        html.Br(),
        dbc.Row([
            dbc.Col(
                dcc.Graph(id='rem-graph', figure={})
            )
        ])
    ])
])

@app.callback(
    Output('sidebar-space-rem','hidden'),
    [Input('edit-rem', 'n_clicks'),
    Input('sidebar-space-rem', 'hidden'),
    Input('chart-options-rem', 'value')]
)
def get_sidebar(button, hideSideBar, graphMode):
    trigger_id=ctx.triggered_id
    if(trigger_id=='edit-rem'):
        if(hideSideBar):
            hideSideBar=False
        else:
            hideSideBar=True
    remDatabag.getDataframe().activateDataframe(graphMode)

    
    return hideSideBar

@app.callback(
    Output('rem-graph', 'figure'),
    [Input('rem-title', 'children'),
    Input('chart-options-rem', 'value')]
    
)
def update_data(title, dummyValue):
    dff=remDatabag.getDataframe().getActive().copy()
    fig=px.line(dff, x='Year', y='Value')
    fig.update_xaxes(nticks=len(pd.unique(dff['Year'])), rangeslider_visible=True)
    if(dummyValue=='Original'):
        fig.update_yaxes(tickprefix='$')
    else:
        fig.update_yaxes(ticksuffix='%')
    return fig