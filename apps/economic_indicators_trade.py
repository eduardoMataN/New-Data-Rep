
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
import dash_draggable



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
    dbc.Offcanvas(id='sidebar-space-trade',backdrop=False,children=[
        
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
        html.Label('Max Y Value:', style=LABEL),
        html.Br(),
        dcc.Input(id='max_input', type='number', min=10, max=1000, value=150),
        html.Br(),
        html.Label('Min Y Value:', style=LABEL),
        html.Br(),
        dcc.Input(id='min_input', type='number', min=10, max=1000, value=150),
        html.Br(),
        html.Br(),
        dbc.Button('Reset', id='reset-trade', outline=True, color="primary", className="me-1", value='reset', n_clicks=0)
                    
        


        
    
    ], is_open=False, title='Chart Modifier'),
    dbc.Container(children=[
    html.Br(),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H2(id='dummy_trade',children=['Imports & Exports by HS/NAICS Commodities'], style=TITLE)
                ])
            ]),
            html.Hr(style=HR)
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
                        disabled=False,
                        searchable=True
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
                        disabled=False,
                        searchable=True
                    )
                ])
            ]),
            dbc.Col([
                html.Div([
                    daq.ToggleSwitch(
                        id='toggle-int',
                        label='Imports/Exports',
                        labelPosition='top',
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
                        labelPosition='top',
                        value=False,
                        style=LABEL
                    )
                ])
            ], width=1),
            dbc.Col([
                html.Div([
                    ALIGN_LABEL,
                    html.Br(),
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
                        labelPosition='top'
                    )
                ])
            ], width=1),
            dbc.Col([
                html.Div([
                    ALIGN_LABEL,
                    html.Br(),
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
                    ALIGN_LABEL,
                    html.Br(),
                    dbc.Button('Edit Graph', id='edit-trade-impex', outline=True, color="primary", className="me-1", value='edit')
                ])
            ], width=2)
        ])
    ]),
    dbc.Container(children=[
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Graph(id='hs-naics-graph', figure={}, config={'editable':True, 'edits':{'legendPosition':True,'titleText':False, 'axisTitleText':False}, 'showTips':True})
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
                        html.P(' Units: Dollars in Millions ($)', style={'color':blue})
                    ], width=3),
                    dbc.Col([
                        html.P('Last Update: 2022', style={'color':blue})
                    ], width=3),
                    dbc.Col([
                        html.P('Source: USA Gov', style={'color':blue})
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
            ]),
            html.Hr(style=HR)
        ])
    ]),
    dbc.Container(children=[
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Graph(
                        id='ep-graph',
                        figure={},
                        config={'editable':False}
                    )
                ])
            ]),
            dbc.Col([
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Label(['Mode'], style=LABEL),
                            dcc.Dropdown(
                                id='select-mode-int',
                                options=[{'label':x, 'value':x}for x in df_ep['Mode'].unique()],
                                value=df_ep['Mode'].unique()[0],
                                style=DROPDOWN,
                                optionHeight=90,
                                
                            ),
                        ]),
                        dbc.Col([
                            html.Div([
                                html.Label(['Edit'], style={'color':'#ffffff'}),
                                html.Br(),
                                dbc.Button('Edit Graph', id='edit-trade-flows', outline=True, color="primary", className="me-1", value='edit')
                            ])
                        ])
                        ]),
                    html.Br(),
                    daq.LEDDisplay(
                        id='led-ep',
                        value=5,
                        label='Total Flows',
                        color=orange,
                        size=35,
                        style=LABEL
                    )
                
            
                ]),
                html.Br(),
                html.Br(),
                html.Br()
            ], width=4)
        ])
    ]),
    dbc.Container([
        dbc.Row([
            dbc.Col([
            html.Div(children=[
                dbc.Row([
                    dbc.Col([
                        html.P(' Units: Dollars in Thousands ($)', style={'color':blue})
                    ], width=3),
                    dbc.Col([
                        html.P('Last Update: 2020', style={'color':blue})
                    ], width=3),
                    dbc.Col([
                        html.P('Source: USA Gov', style={'color':blue})
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
    
    [Output('sidebar-space-trade', 'is_open'),
    Output('sidebar-title-trade', 'children'),
    Output('max_input', 'max'),
    Output('max_input', 'min'),
    Output('min_input', 'max'),
    Output('min_input','min'),
    Output('max_input','value'),
    Output('min_input','value'),
    Output('select-measures-int','options'),
    Output('select-measures-int','value'),
    Output('select-comm-int','options'),
    Output('select-comm-int','value')],
    [Input('edit-trade-impex', 'n_clicks'),
    Input('sidebar-space-trade', 'hidden'),
    Input('toggle-int-2', 'value'),
    Input('toggle-int','value'),
    Input('reset-trade','n_clicks'),
    Input('max_input','value'),
    Input('min_input','value'),
    Input('select-measures-int','value'),
    Input('select-comm-int','value'),
    Input('select-measures-int','options'),
    Input('select-comm-int','options'),
    Input('edit-trade-flows','n_clicks'),
    Input('select-mode-int','value'),
    Input('sidebar-title-trade','children')]
)
def get_sidebar(buttonimpEx, showSideBar, hsNaics, impExp, reset, max, min, measureValue, commValue, measuresOp, commOp, buttonFlows, modeValue, title):
    trigger_id=ctx.triggered_id
    name='hsImports'
    #Might need to use the Title as input to fix the cut functions being applied to the wrong graph. 
    if(trigger_id=='edit-trade-flows'):
        name='totalFlows'
        if(showSideBar):
            showSideBar=False
        else:
            showSideBar=True
        title=tradeDatabag.getByName(name).title
    if(trigger_id=='edit-trade-impex'):
        if(showSideBar):
            showSideBar=False
        else:
            showSideBar=True
        if(hsNaics==True):
            name='naics'
        else:
            if(impExp==True):
                name='hsExports'
            else:
                name='hsImports'
        title=tradeDatabag.getByName(name).title
    if(trigger_id=='toggle-int' or trigger_id=='toggle-int-2'):
        if(hsNaics==True):
            name='naics'
        else:
            if(impExp==True):
                name='hsExports'
            else:
                name='hsImports'
        title=tradeDatabag.getByName(name).title
        measuresOp, measureValue=tradeDatabag.getDataframe(title).get_options('Measures')
        commOp, commValue=tradeDatabag.getDataframe(title).get_options('Commodity')
    if(title=='Total Flows to El Paso Chart'):
        tradeDatabag.getDataframe(title).adjustMinMax('Mode', modeValue)
    else:
        tradeDatabag.getDataframe(title).adjustMinMax(['Measures','Commodity'], [measureValue, commValue])
    currentDataset=tradeDatabag.getDataframe(title)
    currMin=currentDataset.min
    currMax=currentDataset.max
    if(currentDataset.isTrimmed()):
        currentValueMax=currentDataset.trimMax
        currentValueMin=currentDataset.trimMin
        minMax=currentDataset.trimMax-1
        maxMin=currentDataset.trimMin-1
    else:
        currentValueMax=currentDataset.max
        currentValueMin=currentDataset.min
        minMax=currentDataset.max-1
        maxMin=currentDataset.min+1
    if(trigger_id=='reset-trade'):
        currentValueMax=currentDataset.max
        currentValueMin=currentDataset.min
        showSideBar=True
    if(trigger_id=='max_input' or trigger_id=='min_input'):
        minMax=max-1
        maxMin=min+1
        currentValueMax=max
        currentValueMin=min
        showSideBar=True
    
    return showSideBar, title, currMax, maxMin, minMax, currMin, currentValueMax, currentValueMin, measuresOp, measureValue, commOp, commValue
@app.callback(
    Output('dummy_trade','children'),
    [Input('chart-options-trade','value'),
    Input('max_input','value'),
    Input('min_input','value'),
    Input('sidebar-title-trade','children'),
    Input('reset-trade','n_clicks'),
    Input('dummy_trade','children')
    ]
) 
def change_chart(chartMode, max, min, title, reset, mainTitle):
    trigger_id=ctx.triggered_id
    tradeDatabag.getDataframe(title).activateDataframe(chartMode)
    if(trigger_id=='max_input' or trigger_id=='min_input'):
        tradeDatabag.getDataframe(title).trim(max, min)
    if(trigger_id=='reset-trade'):
        tradeDatabag.getDataframe(title).reset()
    return mainTitle

@app.callback(
    [
        Output('hs-naics-graph','figure'),
        Output('compare-port1','disabled'),
        Output('compare-port2', 'disabled'),
        Output('toggle-int','disabled'),
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
        Input('sidebar-title-trade', 'children'),
        Input('max_input','value'),
        Input('min_input','value'),
        Input('reset-trade','n_clicks')
    ]
)
def update_data(measureValue, commodityValue, measureOptions, compareOn, toggleImEx,toggleHsNaics, portValue1, portValue2, commodityOptions, portOptions1, portOptions2, mode, dummyValue, sideBarTitle, dummyMax, dummyMin, dummyReset):
    #Chunk to update Top Part of Page. 
    comparePort1=True
    comparePort2=True
    importsToggle=False
    naicsDropdown=True
    trigger_id=ctx.triggered_id
    #print("Resetting graph "+trigger_id)
    
    if(toggleHsNaics==True):
        currentDataset=tradeDatabag.getByName('naics')
        dff=currentDataset.getActive().copy()
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
        if(toggleImEx):
            currentDataset=tradeDatabag.getByName('hsExports')
            dff=currentDataset.getActive().copy()
        else:
            currentDataset=tradeDatabag.getByName('hsImports')
            dff=currentDataset.getActive().copy()
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
                currentDataset=tradeDatabag.getByName('hsExports')
                dff=currentDataset.getActive().copy()
                fig=px.line(dff[(dff['Measures']==measureValue)&(dff['Commodity']==commodityValue)], x='Year', y='Exports', color='Port', color_discrete_sequence=get_colors(dff['Port'].unique()))
                fig.update_xaxes(rangeslider_visible=True)
            else:
                currentDataset=tradeDatabag.getByName('hsImports')
                dff=currentDataset.getActive().copy()
                fig=px.line(dff[(dff['Measures']==measureValue)&(dff['Commodity']==commodityValue)], x='Year', y='Imports', color='Port', color_discrete_sequence=get_colors(dff['Port'].unique()))
                fig.update_xaxes(rangeslider_visible=True)
    #Chunk to Update Second Section:
    dff_ep=tradeDatabag.getByName('totalFlows').getActive().copy()
    total_f=round(sum(dff_ep[dff_ep['Mode']==mode]['Total']),1)
    fig2=tradeDatabag.getByName('totalFlows').get_line_chart('Mode', mode, colors='Commodity',tick=1,dt=1)
    return fig, comparePort1, comparePort2, importsToggle, portOptions1, portValue1, portOptions2, portValue2, fig2, total_f