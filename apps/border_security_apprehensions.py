
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
from dash.exceptions import PreventUpdate
DATA_PATH = PATH.joinpath("../datasets/Apprehensions").resolve()

df_cit=pd.read_excel(DATA_PATH.joinpath('Apprehensions by Citizenship.xlsx'))
df_cit_per=df_cit.copy()
df_cit_per['Apprehensions']=df_cit_per['Apprehensions'].pct_change()
citDataset=dataset('Yearly Apprehensions by Citizenship Chart', df_cit, 'Apprehensions','tab-cit', 'Citizenship', 'Apprehensions', 'Citizenship')
citDataset.modify_percent_change('Sector', 'Citizenship', 'Apprehensions')

df_country=pd.read_excel(DATA_PATH.joinpath('Apprehensions by Country.xlsx'))
df_country_per=df_country.copy()
df_country_per['Illegal Alien Apprehensions']=df_country_per['Illegal Alien Apprehensions'].pct_change()
countryDataset=dataset('Yearly Apprehensions by Country Chart', df_country, 'Illegal Alien Apprehensions', 'tab-country', 'Country', 'Illegal Alien Apprehensions')
countryDataset.modify_percent_change('Sector', 'Country', 'Illegal Alien Apprehensions')



df_uac=pd.read_excel(DATA_PATH.joinpath('Monthly UAC Apprehensions by Sector.xlsx'))
aucDataset=dataset('AUC Monthly Apprehensions Chart', df_uac, 'Unaccompanied Alien Children Apprehended', 'auc-app', 'Sector', 'Unaccompanied Alien Children Apprehended')

df_family=pd.read_excel(DATA_PATH.joinpath('Monthly Family Unit Apprehensions.xlsx'))
familyDataset=dataset('Family Unit Monthly Apprehensions by Sector Chart', df_family, 'Total','family-unit', 'Sector', 'Total')

df_southwesta=pd.read_excel(DATA_PATH.joinpath('Southwest Border Apprehensions.xlsx'))
southwestAppDataset=dataset('Southwest Border Apprehensions Chart',df_southwesta, 'Total', 'apps', 'Sector', 'Total')

df_southwestb=pd.read_excel(DATA_PATH.joinpath('Southwest Border Deaths.xlsx'))
southwestDeathDataset=dataset('Southwest Border Deaths Chart',df_southwestb, 'Deaths', 'deaths', 'Sector', 'Deaths')

borderSecurityBag=dataBag([citDataset, countryDataset, aucDataset, familyDataset, southwestAppDataset, southwestDeathDataset])

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
                {'label':'Percent Change','value':'PercentChange'},
                {'label': 'Original Chart','value':'Original'}
            ],
            value='Original',
            
        ),
        html.Label('Max Y Value:', style=LABEL),
        dcc.Input(id='max_input_app', type='number', min=10, max=1000, value=150),
        html.Label('Min Y Value:', style=LABEL),
        dcc.Input(id='min_input_app', type='number', min=10, max=1000, value=150),
        html.Br(),
        html.Br(),
        dbc.Button('Reset', id='reset-app', outline=True, color="primary", className="me-1", value='reset', n_clicks=0),
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
                    html.H2(id='app-title',children=['Yearly Apprehensions by Sector'], style=TITLE)
                ])
            ]),
            html.Hr(style={'color':blue, 'borderWidth': "0.3vh", 'borderColor':blue, 'opacity':'unset', 'width':'100%'})
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
                    html.Label(['Edit'], style={'color':'#ffffff'}),
                    html.Br(),
                    dbc.Button('Edit Graph', id='edit-yearly', outline=True, color="primary", className="me-1", value='yearly', n_clicks=0)
                ])
            ], width=2),
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
    dbc.Container([
        dbc.Row([
            dbc.Col([
            html.Div(children=[
                dbc.Row([
                    dbc.Col([
                        html.P(' Units: Individuals', style={'color':blue, 'font-weight':'bold'})
                    ], width=3),
                    dbc.Col([
                        html.P('Last Update: 2019', style={'color':blue, 'font-weight':'bold'})
                    ], width=3),
                    dbc.Col([
                        html.P('Source: USA Gov', style={'color':blue, 'font-weight':'bold'})
                    ], width=3),
                    dbc.Col([
                    html.Div([
                        dbc.Button('Download Dataset', id='download-bttn-app', outline=True, color="primary", className="me-1", value='yearly', n_clicks=0)
                    ]),
                    dcc.Download(id='download-app')
            ],  style={'margin-left': '0px', 'margin-right':'1px'}, width=2)
                ], align='center', justify='center')
            ])
            ]),
        ], align='center', justify='center'),
        html.Br(),
    html.Br(),
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
            ], width=2),
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
    dbc.Container([
        dbc.Row([
            dbc.Col([
            html.Div(children=[
                dbc.Row([
                    dbc.Col([
                        html.P(' Units: Individuals', style={'color':blue, 'font-weight':'bold'})
                    ], width=3),
                    dbc.Col([
                        html.P('Last Update: 2019', style={'color':blue, 'font-weight':'bold'})
                    ], width=3),
                    dbc.Col([
                        html.P('Source: USA Gov', style={'color':blue, 'font-weight':'bold'})
                    ], width=3),
                    dbc.Col([
                    html.Div([
                        dbc.Button('Download Dataset', id='download-bttn-app-2', outline=True, color="primary", className="me-1", value='yearly', n_clicks=0)
                    ]),
                    dcc.Download(id='download-app-2')
            ],  style={'margin-left': '0px', 'margin-right':'1px'}, width=2)
                ], align='center', justify='center')
            ])
            ]),
        ], align='center', justify='center'),
        html.Br(),
    html.Br(),
    ]),
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
            ], width=2),
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
    ]),
    dbc.Container([
        dbc.Row([
            dbc.Col([
            html.Div(children=[
                dbc.Row([
                    dbc.Col([
                        html.P(' Units: Individuals', style={'color':blue, 'font-weight':'bold'})
                    ], width=3),
                    dbc.Col([
                        html.P('Last Update: 2018', style={'color':blue, 'font-weight':'bold'})
                    ], width=3),
                    dbc.Col([
                        html.P('Source: USA Gov', style={'color':blue, 'font-weight':'bold'})
                    ], width=3),
                    dbc.Col([
                    html.Div([
                        dbc.Button('Download Dataset', id='download-bttn-app-3', outline=True, color="primary", className="me-1", value='yearly', n_clicks=0)
                    ]),
                    dcc.Download(id='download-app-3')
            ],  style={'margin-left': '0px', 'margin-right':'1px'}, width=2)
                ], align='center', justify='center')
            ])
            ]),
        ], align='center', justify='center'),
        html.Br(),
    html.Br(),
    ]),
])
@app.callback(
    Output('download-app','data'),
    [Input('download-bttn-app', 'n_clicks'),
    Input('app-tabs', 'value')],
    prevent_initial_call=True
)
def download_median(downloadB, tab): 
    trigger_id=ctx.triggered_id 
    if(trigger_id=='app-tabs'):
        raise PreventUpdate
    else:
        if(tab=='tab-cit'):
            return dcc.send_data_frame(df_cit.to_excel, 'Yearly Apprehensions by Sector and Citizenship.xlsx')
        else:
            return dcc.send_data_frame(df_country.to_excel, 'Yearly Apprehensions by Sector and Country.xlsx')
@app.callback(
    Output('download-app-2','data'),
    [Input('download-bttn-app-2', 'n_clicks'),
    Input('monthly-tabs', 'value')],
    prevent_initial_call=True
)
def download_median(downloadB, tab): 
    trigger_id=ctx.triggered_id 
    if(trigger_id=='monthly-tabs'):
        raise PreventUpdate
    else:
        if(tab=='family-unit'):
            return dcc.send_data_frame(df_family.to_excel, 'Monthly Family Unit Apprehensions by Sector.xlsx')
        else:
            return dcc.send_data_frame(df_uac.to_excel, 'Monthly UUC Apprehensions by Sector.xlsx')
@app.callback(
    Output('download-app-3','data'),
    [Input('download-bttn-app-3', 'n_clicks'),
    Input('south-tabs', 'value')],
    prevent_initial_call=True
)
def download_median(downloadB, tab): 
    trigger_id=ctx.triggered_id 
    if(trigger_id=='south-tabs'):
        raise PreventUpdate
    else:
        if(tab=='apps'):
            return dcc.send_data_frame(df_southwesta.to_excel, 'Southwest Border Apprehensions by Sector.xlsx')
        else:
            return dcc.send_data_frame(df_southwestb.to_excel, 'Southwest Border Deaths by Sector.xlsx')

@app.callback(
    [Output('sidebar-space','hidden'),
    Output('dummy1','children'),
    Output('sidebar-title','children'),
    Output('max_input_app', 'max'),
    Output('max_input_app', 'min'),
    Output('min_input_app', 'max'),
    Output('min_input_app','min'),
    Output('max_input_app','value'),
    Output('min_input_app','value')],
    [Input('edit-yearly','n_clicks'),
    Input('sidebar-space','children'),
    Input('app-tabs','value'),
    Input('edit-monthly','n_clicks'),
    Input('monthly-tabs', 'value'),
    Input('sidebar-space','hidden'),
    Input('edit-southwest','n_clicks'),
    Input('south-tabs','value'),
    Input('sidebar-title', 'children'),
    Input('reset-app','n_clicks'),
    Input('app-title','children'),
    Input('select-sector','value')]
)
def get_sidebar(button, sidebarSpace, currentTabApp, monthlyButton, monthlyTab, sideBarShow, southButton, southTabs, title, reset, dummyTitle, filterValue):
    trigger_id=ctx.triggered_id    
    if(trigger_id=='select-sector'):
        borderSecurityBag.getByName(currentTabApp).adjustMinMax('Sector', filterValue)
    if(trigger_id=='edit-yearly'):
        borderSecurityBag.getByName(currentTabApp).adjustMinMax('Sector', filterValue)
        currentDataset=borderSecurityBag.getByName(currentTabApp)
        newTitle=currentDataset.title
        if(sideBarShow):
            sideBarShow=False
        else:
            sideBarShow=True
        if(title!=newTitle):
            sideBarShow=False
        title=newTitle
        
            
    if(trigger_id=='edit-monthly'):
        currentDataset=borderSecurityBag.getByName(monthlyTab)
        newTitle=currentDataset.title
        if(sideBarShow):
            sideBarShow=False
        elif(title==newTitle):
            sideBarShow=True
        
        title=newTitle
        
    if(trigger_id=='edit-southwest'):
        currentDataset=borderSecurityBag.getByName(southTabs)
        newTitle=currentDataset.title
        if(sideBarShow):
            sideBarShow=False
        elif(title==newTitle):
            sideBarShow=True
        title=newTitle
        
    if(trigger_id=='app-tabs'):
        currentDataset=borderSecurityBag.getByName(currentTabApp)
        title=currentDataset.title
    if(trigger_id=='monthly-tabs'):
        currentDataset=borderSecurityBag.getByName(monthlyTab)
        title=currentDataset.title
    if(trigger_id=='south-tabs'):
        currentDataset=borderSecurityBag.getByName(southTabs)
        title=currentDataset.title
    currentDataset=borderSecurityBag.getDataframe(title)
    currMin=currentDataset.min
    currMax=currentDataset.max
    if(currentDataset.isTrimmed()):
        currentValueMax=currentDataset.trimMax
        currentValueMin=currentDataset.trimMin
        minMax=currentDataset.trimMax-1
        maxMin=currentDataset.trimMin+1
    else:
        currentValueMax=currentDataset.max
        currentValueMin=currentDataset.min
        minMax=currentDataset.max-1
        maxMin=currentDataset.min+1
    if(trigger_id=='reset-app'):
        currentValueMax=currentDataset.max
        currentValueMin=currentDataset.min
        sideBarShow=False
    if(trigger_id=='max_input_app' or trigger_id=='min_input_app'):
        minMax=max-1
        maxMin=min+1
        currentValueMax=max
        currentValueMin=min
        sideBarShow=False
    if(trigger_id=='reset-app'):
        currentValueMax=currentDataset.max
        currentValueMin=currentDataset.min
        sideBarShow=False
    if(trigger_id=='max_input_app' or trigger_id=='min_input_app'):
        minMax=max-1
        maxMin=min+1
        currentValueMax=max
        currentValueMin=min
        sideBarShow=False
    
        
    
    

         
    return sideBarShow, title, title, currMax, maxMin, minMax, currMin, currentValueMax, currentValueMin

@app.callback(
    Output('app-title','children'),
    [Input('app-title','children'),
    Input('chart-options','value'),
    Input('sidebar-title','children'),
    Input('reset-app','n_clicks'),
    Input('max_input_app','value'),
    Input('min_input_app','value')]
)
def change_chart(title, chartMode, sideBarTitle, reset, max, min):
    trigger_id=ctx.triggered_id
    borderSecurityBag.getDataframe(sideBarTitle).activateDataframe(chartMode)
    if(trigger_id=='max_input_app' or trigger_id=='min_input_app'):
        borderSecurityBag.getDataframe(sideBarTitle).trim(max, min)
    if(trigger_id=='reset-app'):
        borderSecurityBag.getDataframe(sideBarTitle).reset()
    return title

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
    Input('chart-options','value'),
    Input('max_input_app','value'),
    Input('min_input_app','value'),
    Input('reset-app','n_clicks')]
)
def update_data(sectorValue, sectorOptions, currentTab, monthlyTab, monthlyOptions, monthlyValue, southTab, southOptions, southValue, yearlyButton, monthlyButton, southwestButton, chartType, dummyMax, dummyMin, dummyReset):
    #Chunk for section 1:
    trigger_id=ctx.triggered_id
    if(currentTab=='tab-cit'):
        dff=borderSecurityBag.getByName(currentTab).getActive().copy()
        if(trigger_id=='app-tabs'):
            sectorOptions=get_options(dff, 'Sector')
            sectorValue=dff['Sector'].unique()[0]
        fig=px.line(dff[dff['Sector']==sectorValue], x='Year', y='Apprehensions', color='Citizenship', color_discrete_sequence=borderSecurityBag.getByName(currentTab).colors)
        fig.update_xaxes(rangeslider_visible=True)
    if(currentTab=='tab-country'):
        dff=borderSecurityBag.getByName(currentTab).getActive().copy()
        if(trigger_id=='app-tabs'):
            sectorOptions=get_options(dff, 'Sector')
            sectorValue=dff['Sector'].unique()[0]
        fig=px.line(dff[dff['Sector']==sectorValue], x='Year', y='Illegal Alien Apprehensions', color='Country', color_discrete_sequence=borderSecurityBag.getByName(currentTab).colors)
        fig.update_xaxes(rangeslider_visible=True)   
    if(borderSecurityBag.getByName(currentTab).get_active_mode()=='Original'):
        nothing='nothing'
    else:
        fig.update_yaxes(ticksuffix='%')
        #fig.update_layout(xaxis=dict(range=[x[0],x[-1]],rangeslider=dict(range=[x[0],x[-1]])))
    
    #Chunk for section 2:
    if(monthlyTab=='family-unit'):
        dff2=borderSecurityBag.getByName(monthlyTab).getActive().copy()
        if(trigger_id=='monthly-tabs'):
            monthlyOptions=get_options(dff2, 'Sector')
            monthlyValue=dff2['Sector'].unique()[0]
        fig2=px.line(filter_df(dff2, 'Sector',monthlyValue), x='Date', y='Total')
        fig2.update_traces(line_color='#FF8200')
    if(monthlyTab=='auc-app'):
        dff2=borderSecurityBag.getByName(monthlyTab).getActive().copy()
        if(trigger_id=='monthly-tabs'):
            monthlyOptions=get_options(dff2, 'Sector')
            monthlyValue=dff2['Sector'].unique()[0]
        fig2=px.line(filter_df(dff2, 'Sector', monthlyValue), x='Date', y='Unaccompanied Alien Children Apprehended')
        fig2.update_traces(line_color='#FF8200')
    if(borderSecurityBag.getByName(monthlyTab).get_active_mode()=='Original'):
        nothing='nothing'
    else:
        fig2.update_yaxes(ticksuffix='%')
    fig2.update_xaxes(rangeslider_visible=True)
    
    #Chunk for section 3:
    if(southTab=='apps'):
        dff3=borderSecurityBag.getByName(southTab).getActive().copy()
        if(trigger_id=='south-tabs'):
            southOptions=get_options(dff3, 'Sector')
            southValue=dff3['Sector'].unique()[0]
        fig3=px.line(filter_df(dff3,'Sector',southValue), x='Fiscal Year', y='Total')
        fig3.update_traces(line_color='#FF8200')
    if(southTab=='deaths'):
        dff3=borderSecurityBag.getByName(southTab).getActive().copy()
        if(trigger_id=='south-tabs'):
            southOptions=get_options(dff3, 'Sector')
            southValue=dff3['Sector'].unique()[0]
        fig3=px.line(filter_df(dff3, 'Sector', southValue), x='Year', y='Deaths')
        fig3.update_traces(line_color='#FF8200')
    fig3.update_xaxes(rangeslider_visible=True)
    if(borderSecurityBag.getByName(southTab).get_active_mode()=='Original'):
        nothing='nothing'
    else:
        fig3.update_yaxes(ticksuffix='%')
    
    return fig, sectorOptions, sectorValue, monthlyOptions, monthlyValue, fig2, southOptions, southValue, fig3
