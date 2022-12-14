
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
DATA_PATH = PATH.joinpath("../datasets/Trade").resolve() #Once we're on that path, we go into datasets. 
df_trade_hs= pd.read_excel(DATA_PATH.joinpath("Imports & Exports by HS Commodities, yearly.xlsx"))
hsImportsDataset=dataset('Imports by HS Commodities Imports Chart', df_trade_hs,'Imports', 'hsImports', 'Port', 'Imports')
hsImportsDataset.modify_percent_change(['Measures', 'Commodity'], 'Port', 'Imports')
hsExportsDataset=dataset('Exports by HS Commodities Imports Chart', df_trade_hs,'Exports', 'hsExports', 'Port', 'Exports')
hsExportsDataset.modify_percent_change(['Measures', 'Commodity'], 'Port', 'Exports')
df_trade_naics=pd.read_excel(DATA_PATH.joinpath("Exports & Imports by NAICS Commodities, yearly.xlsx"))
naicsDataset=dataset('Imports & Exports by NAICS Commodities Chart', df_trade_naics, 'Value', 'naics', 'Commodity', 'Value')
naicsDataset.modify_percent_change(['Commodity', 'Measures'], 'District', 'Value')
df_ep=pd.read_excel(DATA_PATH.joinpath("Total Flows to El Paso.xlsx"))
epDataset=dataset('Total Flows to El Paso Chart', df_ep, 'Total', 'totalFlows', 'Commodity', 'Total')
epDataset.modify_percent_change('Mode', 'Commodity', 'Total')
tradeDatabag=dataBag([naicsDataset, hsExportsDataset, hsImportsDataset, epDataset])


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
    html.Div(id='sidebar-space-trade',children=[
        html.Div(
    [
        html.H6(id='sidebar-title-trade',children='Imports by HS Commodities Imports Chart'),
        html.Hr(),
        html.P(
            "Use the following buttons to edit the chart.", className="lead"
        ),
        dbc.RadioItems(
            id='chart-options-trade',
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
            dbc.Col([
                html.Div([
                    html.H2(['Imports & Exports by HS/NAICS Commodities'], style=TITLE)
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
            ]),
            dbc.Col([
                html.Div([
                    
                    dbc.Button('Edit Graph', id='edit-trade-impex', outline=True, color="primary", className="me-1", value='edit')
                ])
            ], width=2)
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
    dbc.Container([
        dbc.Row([
            dbc.Col([
            html.Div(children=[
                dbc.Row([
                    dbc.Col([
                        html.P(' Units: Dollars in Millions ($)', style={'color':blue, 'font-weight':'bold'})
                    ], width=3),
                    dbc.Col([
                        html.P('Last Update: 2022', style={'color':blue, 'font-weight':'bold'})
                    ], width=3),
                    dbc.Col([
                        html.P('Source: USA Gov', style={'color':blue, 'font-weight':'bold'})
                    ], width=3),
                    dbc.Col([
                    html.Div([
                        dbc.Button('Download Dataset', id='download-bttn-trade', outline=True, color="primary", className="me-1", value='yearly', n_clicks=0)
                    ]),
                    dcc.Download(id='download-trade')
            ],  style={'margin-left': '0px', 'margin-right':'1px'}, width=2)
                ], align='center', justify='center')
            ])
            ]),
        ], align='center', justify='center'),
        html.Br(),
    html.Br(),
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
    ]),
    dbc.Container([
        dbc.Row([
            dbc.Col([
            html.Div(children=[
                dbc.Row([
                    dbc.Col([
                        html.P(' Units: Dollars in Thousands ($)', style={'color':blue, 'font-weight':'bold'})
                    ], width=3),
                    dbc.Col([
                        html.P('Last Update: 2020', style={'color':blue, 'font-weight':'bold'})
                    ], width=3),
                    dbc.Col([
                        html.P('Source: USA Gov', style={'color':blue, 'font-weight':'bold'})
                    ], width=3),
                    dbc.Col([
                    html.Div([
                        dbc.Button('Download Dataset', id='download-bttn-trade2', outline=True, color="primary", className="me-1", value='yearly', n_clicks=0)
                    ]),
                    dcc.Download(id='download-trade2')
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
    Output('download-trade','data'),
    Input('download-bttn-trade', 'n_clicks'),
    prevent_initial_call=True
)
def download_median(downloadB): #THERE ARE TWO DATA FRAMES. SHOULD WE APPEND THEM. 

    return dcc.send_data_frame(pd.concat([df_trade_naics, df_trade_hs]).to_excel, 'Imports & Exports by HS/NAICS Commodities.xlsx')

@app.callback(
    Output('download-trade2','data'),
    Input('download-bttn-trade2', 'n_clicks'),
    prevent_initial_call=True
)
def download_median(downloadB):

    return dcc.send_data_frame(df_ep.to_excel, 'Total Flows to El Paso.xlsx')

@app.callback(
    
    [Output('sidebar-space-trade', 'hidden'),
    Output('sidebar-title-trade', 'children')],
    [Input('edit-trade-impex', 'n_clicks'),
    Input('sidebar-space-trade', 'hidden'),
    Input('chart-options-trade', 'value'),
    Input('toggle-int-2', 'value'),
    Input('toggle-int','value'),
    Input('sidebar-title-trade', 'children')]
)
def get_sidebar(buttonimpEx, showSideBar, chartMode, hsNaics, impExp, title):
    trigger_id=ctx.triggered_id
    name='hsImports'
    if(buttonimpEx):
        if(showSideBar):
            showSideBar=False
        else:
            showSideBar=True
        if(hsNaics):
            name='naics'
        else:
            if(impExp):
                name='hsExports'
            else:
                name='hsImports'

    tradeDatabag.getByName(name).activateDataframe(chartMode)
    title=tradeDatabag.getByName(name).title
    return showSideBar, title

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
        Input('select-mode-int','value'),
        Input('chart-options-trade', 'value'),
        Input('sidebar-title-trade', 'children')
    ]
)
def update_data(measureValue, commodityValue, measureOptions, compareOn, toggleImEx,toggleHsNaics, portValue1, portValue2, commodityOptions, portOptions1, portOptions2, mode, dummyValue, sideBarTitle):
    #Chunk to update Top Part of Page. 
    comparePort1=True
    comparePort2=True
    importsToggle=False
    naicsDropdown=True
    trigger_id=ctx.triggered_id
    dff=tradeDatabag.getDataframe(sideBarTitle).getActive().copy()
    if(toggleHsNaics==True):
        #dff=df_trade_naics.copy()
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
            fig.update_xaxes(rangeslider= {'visible':True}, row=1, col=1)
            fig.update_xaxes(rangeslider= {'visible':True}, row=1, col=2)
            
        else:
            fig=px.line(dff[(dff['Measures']==measureValue)&(dff['Commodity']==commodityValue)], x='Year', y='Value', color='District', color_discrete_sequence=get_colors(dff['District'].unique()))
            
    else:
        #dff=df_trade_hs.copy()
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
                fig.update_xaxes(rangeslider= {'visible':True}, row=1, col=1)
                fig.update_xaxes(rangeslider= {'visible':True}, row=1, col=2)
            else:
                fig=create_subplot(fig, 1, 1, dff[(dff['Port']==portValue1)&(dff['Measures']==measureValue)&(dff['Commodity']==commodityValue)], 'Year', 'Imports','Port')
                fig=create_subplot(fig, 1, 2, dff[(dff['Port']==portValue2)&(dff['Measures']==measureValue)&(dff['Commodity']==commodityValue)], 'Year', 'Imports','Port')
                fig.update_xaxes(rangeslider= {'visible':True}, row=1, col=1)
                fig.update_xaxes(rangeslider= {'visible':True}, row=1, col=2)
        else:
            if(toggleImEx):
                fig=px.line(dff[(dff['Measures']==measureValue)&(dff['Commodity']==commodityValue)], x='Year', y='Exports', color='Port', color_discrete_sequence=get_colors(dff['Port'].unique()))
                fig.update_xaxes(rangeslider_visible=True)
            else:
                fig=px.line(dff[(dff['Measures']==measureValue)&(dff['Commodity']==commodityValue)], x='Year', y='Imports', color='Port', color_discrete_sequence=get_colors(dff['Port'].unique()))
                fig.update_xaxes(rangeslider_visible=True)
    #Chunk to Update Second Section:
    dff_ep=df_ep.copy()
    fig2=px.line(dff_ep[dff_ep['Mode']==mode], x='Year', y="Total", color='Commodity', color_discrete_sequence=get_colors(dff['Commodity'].unique()))
    total_f=round(sum(dff_ep[dff_ep['Mode']==mode]['Total']),1)
    fig2.update_xaxes(tick0=1, dtick=1)
    fig2.update_xaxes(rangeslider_visible=True)
    return fig, comparePort1, comparePort2, importsToggle, measureOptions, measureValue, commodityOptions, commodityValue, portOptions1, portValue1, portOptions2, portValue2, fig2, total_f