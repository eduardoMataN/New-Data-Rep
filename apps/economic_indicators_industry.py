
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
df_est=pd.read_excel(DATA_PATH.joinpath('Number of Establishments.xlsx'))
stabDataset=dataset('Number of Business Stablishments by Year Chart', df_est, 'Value', 'stablishments', 'County', 'Value')
toTable=df_est[df_est['Year']==df_est['Year'][0]][['County', 'Period', 'Value']]
df_gdp=pd.read_excel(DATA_PATH.joinpath('GDP by Industry for Border Counties.xlsx'))
gdpDatasetCounty=dataset('GDP by Industry for Border Counties Chart', df_gdp, 'GDP', 'gdpCounty', 'County', 'GDP')
gdpDatasetCounty.modify_percent_change('County','Description', 'GDP')
gdpDatasetIndustry=dataset('GDP by County for Industries Chart', df_gdp, 'GDP', 'gdpDesc', 'County', 'GDP')
gdpDatasetIndustry.modify_percent_change('Description','County', 'GDP')
industryDatabag=dataBag([stabDataset, gdpDatasetIndustry, gdpDatasetCounty])
layout=html.Div(children=[
    html.Br(),
    dbc.Container(children=[
        html.Div(id='sidebar-space-ind',children=[
        html.Div(
    [
        html.H6(id='sidebar-title-ind',children='Number of Business Stablishments by Year'),
        html.Hr(),
        html.P(
            "Use the following buttons to edit the chart.", className="lead"
        ),
        dbc.RadioItems(
            id='chart-options-ind',
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
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H2(id='title',children=['Number of Business Stablishments by Year'], style={'color':blue})
                ])
            ),
            dbc.Col([
                html.Div([
                    dbc.Button('Edit Graph', id='edit-stablishments', outline=True, color="primary", className="me-1", value='yearly', n_clicks=0)
                ])
            ], width=2),
            dbc.Col([
                    html.Div([
                        dbc.Button('Download Dataset', id='download-bttn-ind', outline=True, color="primary", className="me-1", value='yearly', n_clicks=0)
                    ]),
                    dcc.Download(id='download-ind')
            ],  style={'margin-left': '0px', 'margin-right':'1px'}, width=2)
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col(
                dcc.Graph(id='line-1', figure={})
            )
            
        ]),
        dbc.Container([
        dbc.Row([
            dbc.Col([
            html.Div(children=[
                dbc.Row([
                    dbc.Col([
                        
                    ], width=2),
                    dbc.Col([
                        html.P(' Units: Dollars ($)', style={'color':blue, 'font-weight':'bold'})
                    ], width=3),
                    dbc.Col([
                        html.P('Last Update: June 2022', style={'color':blue, 'font-weight':'bold'})
                    ], width=3),
                    dbc.Col([
                        html.P('Source: USA Gov', style={'color':blue, 'font-weight':'bold'})
                    ], width=3)
                ], align='center', justify='center')
            ])
            ]),
        ], align='center', justify='center'),
        html.Br(),
    html.Br(),
    ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.Label(['County'], style=LABEL),
                    dcc.Dropdown(
                        id='select-county-ind',
                        options=[{'label':x, 'value':x} for x in df_est['County'].unique()],
                        multi=False,
                        value=df_est['County'].unique()[0],
                        style={'width':'100%'},
                        optionHeight=90            
                    )
            ])
            ),
            dbc.Col([
                html.Div([
                    html.Label(['Year'], style=LABEL),
                    dcc.Dropdown(
                        id='select-year-ind',
                        options=[{'label':x, 'value':x} for x in df_est['Year'].unique()],
                        value=df_est['Year'].unique()[0],
                        style={'width':'100%'},
                        optionHeight=90
                    )
                ])
                    ]),
            
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
                        filter_action='none',
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
        ),
    ]),
    html.Br(),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H1(['GDP by Industry for Border Counties'], style=TITLE)
                ])
            ])
        ])
    ]),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    daq.PowerButton(
                        id='county-button',
                        on=True,
                        color=orange
                    )
                ])
            ], width=1),
            dbc.Col([
                html.Div([
                    html.Label(['County'], style=LABEL),
                    dcc.Dropdown(
                        id='select-county-gdp',
                        options=get_options(df_gdp, 'County'),
                        value=df_gdp['County'].unique()[0],
                        multi=False,
                        style=DROPDOWN,
                        optionHeight=90,
                        disabled=False
                    )
                ])
            ]),
            dbc.Col([
                html.Div([
                    daq.PowerButton(
                        id='industry-button',
                        on=False,
                        color=orange
                    )
                ])
            ], width=1),
            dbc.Col([
                html.Div([
                    html.Label(['Industry'], style=LABEL),
                    dcc.Dropdown(
                        id='select-industry-gdp',
                        options=get_options(df_gdp, 'Description'),
                        value=df_gdp['Description'].unique()[0],
                        style=DROPDOWN,
                        optionHeight=90,
                        disabled=True
                    )
                ])
            ]),
            dbc.Col([
                html.Div([
                    dbc.Button('Edit Graph', id='edit-gdp', outline=True, color="primary", className="me-1", value='yearly', n_clicks=0)
                ])
            ], width=2),
            dbc.Col([
                    html.Div([
                        dbc.Button('Download Dataset', id='download-bttn-ind-2', outline=True, color="primary", className="me-1", value='yearly', n_clicks=0)
                    ]),
                    dcc.Download(id='download-ind-2')
            ],  style={'margin-left': '0px', 'margin-right':'1px'}, width=2)
        ])
    ]),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Graph(
                        id='gdp-graph',
                        figure={}
                    )
                ])
            ])
        ]),
    ]),
    dbc.Container([
        dbc.Row([
            dbc.Col([
            html.Div(children=[
                dbc.Row([
                    dbc.Col([
                        
                    ], width=2),
                    dbc.Col([
                        html.P(' Units: Dollars ($)', style={'color':blue, 'font-weight':'bold'})
                    ], width=3),
                    dbc.Col([
                        html.P('Last Update: June 2022', style={'color':blue, 'font-weight':'bold'})
                    ], width=3),
                    dbc.Col([
                        html.P('Source: USA Gov', style={'color':blue, 'font-weight':'bold'})
                    ], width=3)
                ], align='center', justify='center')
            ])
            ]),
        ], align='center', justify='center'),
        html.Br(),
    html.Br(),
    ]),
])
@app.callback(
    Output('download-ind','data'),
    Input('download-bttn-ind', 'n_clicks'),
    prevent_initial_call=True
)
def download_median(downloadB): 
 
    return dcc.send_data_frame(df_est.to_excel, 'Number of Business Stablishments by Year Data.xlsx')

@app.callback(
    Output('download-ind-2','data'),
    Input('download-bttn-ind-2', 'n_clicks'),
    prevent_initial_call=True
)
def download_median(downloadB): 
 
    return dcc.send_data_frame(df_gdp.to_excel, 'GDP By Industry for Border Counties Data.xlsx')

@app.callback(
    [Output('sidebar-space-ind','hidden'),
    Output('sidebar-title-ind','children')],
    [Input('sidebar-space-ind', 'hidden'),
    Input('edit-gdp','n_clicks'),
    Input('edit-stablishments', 'n_clicks'),
    Input('chart-options-ind','value'),
    Input('county-button', 'on'),
    Input('industry-button','on'),
    Input('sidebar-title-ind','children')]
)
def get_sidebar(hideSideBar, button, button2, chartMode, countyButton, industryButton, title):
    trigger_id=ctx.triggered_id
    if(trigger_id=='edit-stablishments'):
        if(hideSideBar):
            hideSideBar=False
        else:
            hideSideBar=True
        title=industryDatabag.get_title_by_name('stablishments')
    if(trigger_id=='edit-gdp'):
        if(hideSideBar):
            hideSideBar=False
        else:
            hideSideBar=True
        if(countyButton):
            title=industryDatabag.get_title_by_name('gdpCounty')
        if(industryButton):
            title=industryDatabag.get_title_by_name('gdpDesc')
    print(chartMode)
    industryDatabag.getDataframe(title).activateDataframe(chartMode)
        
    
            
    return hideSideBar, title

@app.callback(
    
        
        [Output(component_id='line-1', component_property='figure'),
        Output('industry-table', 'data'), Output('industry-table', 'columns'),
        Output('gdp-graph','figure'),
        Output('county-button','on'),
        Output('select-county-gdp','disabled'),
        Output('industry-button','on'),
        Output('select-industry-gdp','disabled')]
    ,
    
        [Input('title', 'children'), Input('select-county-ind', 'value'),
        Input('select-year-ind', 'value'),
        Input('county-button','on'),
        Input('select-county-gdp','value'),
        Input('industry-button', 'on'),
        Input('select-industry-gdp','value'),
        Input('chart-options-ind', 'value')]
    
)
def update_data(title, countyT,yearT, countyOn, countyValue, industryOn, industryValue, dummyValue):
    trigger_id=ctx.triggered_id
    dff=industryDatabag.getByName('stablishments').getActive().copy()
    finalFig=px.line(sum_df(dff, 'County', 'Year', 'Value'), x='Year', y='Value', color='County', color_discrete_sequence=get_colors(dff['County'].unique()))
    finalFig.update_xaxes(nticks=len(pd.unique(dff['Year'])))
    finalFig.update_xaxes( rangeslider_visible=True)
    toTable=dff[(dff['Year']==yearT) & (dff['County']==countyT)][['County', 'Period', 'Value']]

    #GDP Section:
    disableCounty=False
    disableIndustry=True
    dff2=df_gdp.copy()
    if(trigger_id=='industry-button'):
        disableCounty=True
        disableIndustry=False
        countyOn=False
        industryOn=True
        
    if(trigger_id=='county-button'):
        disableCounty=False
        disableIndustry=True
        countyOn=True
        industryOn=False
        
    if(countyOn):
        dff2=industryDatabag.getByName('gdpCounty').getActive().copy()
        fig=px.line(filter_df(dff2, 'County', countyValue), x='Year', y='GDP', color='Description', color_discrete_sequence=get_colors(dff2['Description'].unique()))
        disableCounty=False
        disableIndustry=True
        countyOn=True
        industryOn=False
    if(industryOn):
        dff2=industryDatabag.getByName('gdpDesc').getActive().copy()
        fig=px.line(filter_df(dff2, 'Description', industryValue), x='Year', y='GDP', color='County', color_discrete_sequence=get_colors(dff2['County'].unique()))
        disableCounty=True
        disableIndustry=False
        countyOn=False
        industryOn=True
    fig.update_xaxes(rangeslider_visible=True)
    

    return finalFig, toTable.to_dict('records'), [{'name':i, 'id':i} for i in toTable.columns], fig, countyOn, disableCounty, industryOn, disableIndustry