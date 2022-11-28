
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
DATA_PATH = PATH.joinpath("../datasets/Apprehensions").resolve()

df_cit=pd.read_excel(DATA_PATH.joinpath('Apprehensions by Citizenship.xlsx'))
df_cit_per=df_cit.copy()
df_cit_per['Apprehensions']=df_cit_per['Apprehensions'].pct_change()
citDataset=dataset('Yearly Apprehensions by Citizenship', df_cit, df_cit_per)

df_country=pd.read_excel(DATA_PATH.joinpath('Apprehensions by Country.xlsx'))
df_country_per=df_country.copy()
df_country_per['Illegal Alien Apprehensions']=df_country_per['Illegal Alien Apprehensions'].pct_change()
countryDataset=dataset('Yearly Apprehensions by Country', df_country, df_country_per)


df_uac=pd.read_excel(DATA_PATH.joinpath('Monthly UAC Apprehensions by Sector.xlsx'))

df_family=pd.read_excel(DATA_PATH.joinpath('Monthly Family Unit Apprehensions.xlsx'))

df_southwesta=pd.read_excel(DATA_PATH.joinpath('Southwest Border Apprehensions.xlsx'))

df_southwestb=pd.read_excel(DATA_PATH.joinpath('Southwest Border Deaths.xlsx'))

current=df_cit.copy()
previous=df_cit.copy()
show_sidebar=True



layout=html.Div([
    html.H6(id='dummy1', children='', hidden=True),
    html.Div(id='dummy',children=[], hidden=True),
    html.Div(dcc.Location(id='sidebar-location',refresh=False)),
    html.Div(id='sidebar-space',children=[
        html.Div(
    [
        html.H6(id='sidebar-title',children='Chart'),
        html.Hr(),
        html.P(
            "Use the following buttons to edit the chart.", className="lead"
        ),
        dbc.RadioItems(
            id='chart-options',
            options=[
                {'label':'Percent Change','value':'percent-change'},
                {'label': 'Original Chart','value':'original'}
            ],
            value='original',
            
        ),
        
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        


        dbc.Button('Hide', id='hide-button', outline=True, color="primary", className="me-1", value='hide', n_clicks=0 )
    ],
    style=SIDEBAR_STYLE,
    )
    ], hidden=True),
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
            ]),
            dbc.Col([
                html.Div([
                    dbc.Button('Edit Graph', id='edit-yearly', outline=True, color="primary", className="me-1", value='yearly', n_clicks=0)
                ])
            ], width=2)
        ]),
       
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
            dcc.Tab(label='Family Unit Apprehensions', value='family-unit', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='AUC Apprehensions', value='auc-app', style=tab_style, selected_style=tab_selected_style)
        ])
    ]),
    html.Br(),
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
            ]),
            dbc.Col([
                html.Div([
                    dbc.Button('Edit Graph', id='edit-monthly', outline=True, color="primary", className="me-1", value='monthly')
                ])
            ], width=2)
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
            dcc.Tab(label='Apprehensions', value='apps', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Deaths', value='deaths', style=tab_style, selected_style=tab_selected_style)
        ])
    ]),
    html.Br(),
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
            ]),
            dbc.Col([
                html.Div([
                    dbc.Button('Edit Graph', id='edit-southwest', outline=True, color="primary", className="me-1", value='southwest')
                ])
            ], width=2)
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
    [Output('sidebar-space','hidden'),
    Output('dummy1','children'),
    Output('sidebar-title','children')],
    [Input('edit-yearly','n_clicks'),
    Input('sidebar-space','children'),
    Input('app-tabs','value'),
    Input('edit-monthly','n_clicks'),
    Input('monthly-tabs', 'value'),
    Input('sidebar-space','hidden'),
    Input('edit-southwest','n_clicks'),
    Input('south-tabs','value')]
)
def get_sidebar(button, sidebarSpace, currentTabApp, monthlyButton, monthlyTab, sideBarShow, southButton, southTabs):
    trigger_id=ctx.triggered_id
    sidebar=html.Div()
    sideBarShow=True
    title=''
    
        
    if(trigger_id=='edit-yearly'):
        if(sideBarShow):
            sideBarShow=False
        else:
            sideBarShow=True
        
        if(currentTabApp=='tab-cit'):
            title='Yearly Apprehensions by Citizenship Chart'
            
        else:
            title='Yearly Apprehensions by Country Chart'
            
    if(trigger_id=='edit-monthly'):
        if(sideBarShow):
            sideBarShow=False
        else:
            sideBarShow=True
        
        if(monthlyTab=='family-unit'):
            title='Family Unit Monthly Apprehensions by Sector Chart'     
        else:
            title='AUC Monthly Apprehensions Chart'
    if(trigger_id=='edit-southwest'):
        if(sideBarShow):
            sideBarShow=False
        else:
            sideBarShow=True
        
        if(southTabs=='apps'):
            title='Family Unit Monthly Apprehensions by Sector Chart'     
        else:
            title='AUC Monthly Apprehensions Chart'
    
    

         
    return sideBarShow, title, title

@app.callback(
    Output('dummy','children'),
    [Input('chart-options', 'value'),
    Input('dummy1', 'children')]
)
def update_chart(pathname, title):
    if(pathname=='percent-change'):
        if(title=='Yearly Apprehensions by Citizenship Chart'):
            citDataset.activateDataframe('PercentChange')
        if(title=='Yearly Apprehensions by Country Chart'):
            countryDataset.activateDataframe('PercentChange')
    if(pathname=='original'):
        if(title=='Yearly Apprehensions by Citizenship Chart'):
            citDataset.activateDataframe('Original')
        if(title=='Yearly Apprehensions by Country Chart'):
            countryDataset.activateDataframe('Original')
    return None

@app.callback(
    [Output('apprehensions-graph', 'figure'),
    Output('select-sector','options'),
    Output('select-sector','value'),
    Output('sector-monthly','options'),
    Output('sector-monthly','value'),
    Output('monthly-graph','figure'),
    Output('south-sector','options'),
    Output('south-sector','value'),
    Output('south-graph','figure'),
    ],
    [Input('select-sector','value'),
    Input('select-sector','options'),
    Input('app-tabs','value'),
    Input('monthly-tabs', 'value'),
    Input('sector-monthly', 'options'),
    Input('sector-monthly','value'),
    Input('south-tabs','value'),
    Input('south-sector','options'),
    Input('south-sector','value'),
    Input('edit-yearly','value'),
    Input('edit-monthly','value'),
    Input('edit-southwest','value'),
    Input('chart-options','value')]
)
def update_data(sectorValue, sectorOptions, currentTab, monthlyTab, monthlyOptions, monthlyValue, southTab, southOptions, southValue, yearlyButton, monthlyButton, southwestButton, chartType):
    #Chunk for section 1:
    trigger_id=ctx.triggered_id
    if(currentTab=='tab-cit'):
        dff=citDataset.getActive().copy()
        if(trigger_id=='app-tabs'):
            sectorOptions=get_options(dff, 'Sector')
            sectorValue=dff['Sector'].unique()[0]
        fig=px.line(dff[dff['Sector']==sectorValue], x='Year', y='Apprehensions', color='Citizenship', color_discrete_sequence=get_colors(dff['Citizenship'].unique()))
        fig.update_xaxes(rangeslider_visible=True)
    if(currentTab=='tab-country'):
        dff=countryDataset.getActive().copy()
        if(trigger_id=='app-tabs'):
            sectorOptions=get_options(dff, 'Sector')
            sectorValue=dff['Sector'].unique()[0]
        fig=px.line(dff[dff['Sector']==sectorValue], x='Year', y='Illegal Alien Apprehensions', color='Country', color_discrete_sequence=get_colors(dff['Country'].unique()))   
    
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
