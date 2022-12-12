
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
DATA_PATH = PATH.joinpath("../datasets/Border Patrol Agent Staffing").resolve()

df_region=pd.read_excel(DATA_PATH.joinpath('Staffing by region.xlsx'))
df_sector=pd.read_excel(DATA_PATH.joinpath('Staffing by Sector.xlsx'))
regionDataset=dataset('Border Patrol Agent Staffing by Region', df_region, 'Staffing ', 'region', 'Border Patrol Region', 'Staffing ')
sectorDataset=dataset('Border Patrol Agent Staffing by Sector', df_sector, 'Staff', 'sector', 'Sector', 'Staff')
staffDatabag=dataBag([regionDataset, sectorDataset])



layout=html.Div([
    html.Div(id='sidebar-space-staff',children=[
        html.Div(
    [
        html.H6(id='sidebar-title-staff',children='Border Patrol Agent Staffing'),
        html.Hr(),
        html.P(
            "Use the following buttons to edit the chart.", className="lead"
        ),
        dbc.RadioItems(
            id='chart-options-staff',
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
                html.H2(['Border Patrol Agent Staffing'], style=TITLE)
            ])
        ])
    ]),
    dbc.Container([
        dbc.Col([
            dcc.Tabs(id='select-indicator', value='region', children=[
                dcc.Tab(label='By Region', value='region', style=tab_style, selected_style=tab_selected_style),
                dcc.Tab(label='By Sector', value='sector', style=tab_style, selected_style=tab_selected_style)
            ])
        ]),
        html.Br(),
        
    ]),
    html.Br(),
    dbc.Container([
        dbc.Row([
            dbc.Col([
            html.Div(children=[
                dbc.Row([
                    dbc.Col([
                        html.P(' Units: Individuals', style={'color':blue, 'font-weight':'bold'})
                    ], width=4),
                    dbc.Col([
                        html.P('Last Update: 2019', style={'color':blue, 'font-weight':'bold'})
                    ], width=4),
                    dbc.Col([
                        html.P('Source: USA Gov', style={'color':blue, 'font-weight':'bold'})
                    ], width=4)
                ], align='center', justify='center')
            ], style={"border":"2px black solid"})
            ]),
            dbc.Col([
                html.Div([
                    dbc.Button('Edit Graph', id='edit-staff', outline=True, color="primary", className="me-1", value='yearly', n_clicks=0)
                ])
            ], width=2)
        ], align='center', justify='center'),
        html.Br(),
    html.Br(),
    ]),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Graph(
                        id='staffing-graph',
                        figure={}
                    )
                ])
            ])
        ])
    ])
])

@app.callback(
    [Output('sidebar-space-staff','hidden'),
    Output('sidebar-title-staff', 'children')],
    [Input('edit-staff', 'n_clicks'),
    Input('select-indicator','value'),
    Input('sidebar-space-staff', 'hidden'),
    Input('chart-options-staff', 'value')]
)
def get_sidebar(button, graphName, hideSideBar, graphMode):
    trigger_id=ctx.triggered_id
    if(trigger_id=='edit-staff'):
        if(hideSideBar):
            hideSideBar=False
        else:
            hideSideBar=True
    title=staffDatabag.getByName(graphName).title
    staffDatabag.getByName(graphName).activateDataframe(graphMode)
    return hideSideBar, title


@app.callback(
    Output('staffing-graph', 'figure'),
    [Input('select-indicator','value'),
    Input('chart-options-staff', 'value')]
)
def update_data(indicator, dummyValue):
    dff=staffDatabag.getByName(indicator).getActive().copy()
    if(indicator=='region'):
        fig=px.line(dff, x='Fiscal Year', y='Staffing ', color='Border Patrol Region', color_discrete_sequence=get_colors(dff['Border Patrol Region'].unique()))
    if(indicator=='sector'):
        fig=px.line(dff, x='Year', y='Staff', color='Sector', color_discrete_sequence=get_colors(dff['Sector'].unique()))
    fig.update_xaxes(rangeslider_visible=True)
    if(dummyValue=='PercentChange'):
        fig.update_yaxes(ticksuffix='%')
    return fig