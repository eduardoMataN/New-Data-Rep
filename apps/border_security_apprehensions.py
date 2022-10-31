
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
    html.Br(),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H2(['Yearly Apprehensions by Sector'], style=TITLE)
                ])
            ])
        ])
    ]),
    dbc.Container([
        dcc.Tabs(id='app-tabs', value='tab-cit', children=[
            dcc.Tab(label='By Citizenship', value='tab-cit', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='By Country',value='tab-country', style=tab_style, selected_style=tab_selected_style)
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
    ]),
    html.Br(),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H2(children=['Monthly Apprehensions by Sector'], style=TITLE)
                ])
            ])
        ])
    ]),
    dbc.Container([
        dcc.Tabs(id='monthly-tabs', value='family-unit', children=[
            dcc.Tab(label='Family Unit Apprehensions', value='family-unit', style=LABEL),
            dcc.Tab(label='AUC Apprehensions', value='auc-app', style=LABEL)
        ])
    ]),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Label(['Sector'], style=LABEL),
                    dcc.Dropdown(
                        id='sector-monthly',
                        options=get_options(df_family,'Sector'),
                        value=df_family['Sector'].unique()[0],
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
                        id='monthly-graph',
                        figure={}
                    )
                ])
            ])
        ])
    ]),
    html.Br(),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H2(['Southwest Border'], style=TITLE)
                ])
            ])
        ])
    ]),
    dbc.Container([
        dcc.Tabs(id='south-tabs', value='apps', children=[
            dcc.Tab(label='Apprehensions', value='apps', style=LABEL),
            dcc.Tab(label='Deaths', value='deaths', style=LABEL)
        ])
    ]),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Label(['Sector'], style=LABEL),
                    dcc.Dropdown(
                        id='south-sector',
                        options=get_options(df_southwesta, 'Sector'),
                        value=df_southwesta['Sector'].unique()[0],
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
                        id='south-graph',
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
    Output('select-sector','value'),
    Output('sector-monthly','options'),
    Output('sector-monthly','value'),
    Output('monthly-graph','figure'),
    Output('south-sector','options'),
    Output('south-sector','value'),
    Output('south-graph','figure')],
    [Input('select-sector','value'),
    Input('select-sector','options'),
    Input('app-tabs','value'),
    Input('monthly-tabs', 'value'),
    Input('sector-monthly', 'options'),
    Input('sector-monthly','value'),
    Input('south-tabs','value'),
    Input('south-sector','options'),
    Input('south-sector','value')]
)
def update_data(sectorValue, sectorOptions, currentTab, monthlyTab, monthlyOptions, monthlyValue, southTab, southOptions, southValue):
    #Chunk for section 1:
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
    
    #Chunk for section 2:
    if(monthlyTab=='family-unit'):
        dff2=df_family.copy()
        if(trigger_id=='monthly-tabs'):
            monthlyOptions=get_options(dff2, 'Sector')
            monthlyValue=dff2['Sector'].unique()[0]
        fig2=px.line(filter_df(dff2, 'Sector',monthlyValue), x='Date', y='Total')
    if(monthlyTab=='auc-app'):
        dff2=df_uac.copy()
        if(trigger_id=='monthly-tabs'):
            monthlyOptions=get_options(dff2, 'Sector')
            monthlyValue=dff2['Sector'].unique()[0]
        fig2=px.line(filter_df(dff2, 'Sector', monthlyValue), x='Date', y='Unaccompanied Alien Children Apprehended')
    
    #Chunk for section 3:
    if(southTab=='apps'):
        dff3=df_southwesta.copy()
        if(trigger_id=='south-tabs'):
            southOptions=get_options(dff3, 'Sector')
            southValue=dff3['Sector'].unique()[0]
        fig3=px.line(filter_df(dff3,'Sector',southValue), x='Fiscal Year', y='Total')
    if(southTab=='deaths'):
        dff3=df_southwestb.copy()
        if(trigger_id=='south-tabs'):
            southOptions=get_options(dff3, 'Sector')
            southValue=dff3['Sector'].unique()[0]
        fig3=px.line(filter_df(dff3, 'Sector', southValue), x='Year', y='Deaths')
    return fig, sectorOptions, sectorValue, monthlyOptions, monthlyValue, fig2, southOptions, southValue, fig3