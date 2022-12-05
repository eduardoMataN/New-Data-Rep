import pandas as pd
import plotly.express as px
import dash as dash
from dash import dcc, ctx
from dash import html, dash_table
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash.dependencies import Input, Output, State
import pathlib
import plotly.graph_objects as go
from app import app
from apps.common_items import *
from apps.dataset import *
from apps.dataBag import *

PATH = pathlib.Path(__file__).parent #So this first line is going to the parent of the current path, which is the Multipage app. 
DATA_PATH = PATH.joinpath("../datasets").resolve() #Once we're on that path, we go into datasets. 
df= pd.read_excel(DATA_PATH.joinpath("Border Crossings.xlsx"))
df['Value']=pd.to_numeric(df['Value'])
df_copy=df.copy()
maxYear=df['Year'].max()
df_copy=df[df['Measure']=='Truck Containers Empty']
initialValue=sum(df_copy.loc[df_copy.Year==maxYear, 'Value'].tolist())
df_current=df[df['Year']==df['Year'].max()]
df_profiler=df_current[df_current['Port']==sorted(df['Port'].unique())[0]]

toTable=df_profiler[['Measure', 'Month', 'Value']]
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
    html.Div(id='sidebar-space-bc',children=[
        html.Div(
    [
        html.H6(id='sidebar-title-bc',children='Border Crossings Chart'),
        html.Hr(),
        html.P(
            "Use the following buttons to edit the chart.", className="lead"
        ),
        dbc.RadioItems(
            id='chart-options-bc',
            options=[
                {'label':'Percent Change','value':'PercentChange'},
                {'label': 'Original Chart','value':'Original'}
            ],
            value='Original',
            
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
        


        
    ],
    style=SIDEBAR_STYLE,
    )
    ], hidden=True),
    dbc.Container([
        html.Br(),
        dbc.Row([
            dbc.Col([
                html.Div([
                    dbc.Button(
                        "?",
                        id="click-target-1",
                        className="me-1",
                        n_clicks=0,
                        style={'color':'##FF8200'},
                        size='sm'
                    ),
                    dbc.Popover(
                        children='This first section displays information throughout the Years for each indicator by County. Use the slider at the bottom to change the range of the Y axis. You may also isolate a line by double clicking on its legend element. ',
                        target='click-target-1',
                        body=True,
                        trigger='click'
                    )
                ])
            ], width=1),
            dbc.Col(
                width=3
            ),
            dbc.Col(
                html.Div([
                    html.H1(id='section-title', children=['Border Security'], style={'color':'#041E42'})
                ]),
                width=4
            ),
            
            dbc.Col(
                html.Div([
                    #html.Label(['Current'], style=LABEL),
                    daq.LEDDisplay(id='Number1', value=initialValue, color='#FF8200', label={'label':'Current', 'style':LABEL}, labelPosition='bottom',)
                ]),
                
            ),
            dbc.Col()
        ])
    ]),
    
    
    html.Br(),
    dbc.Container(children=[
        dbc.Row([
            dbc.Col(
                width=1
            ),
            dbc.Col(
                html.Div([
                    html.Label(['Indicator'], style={'font-weight':'bold', 'color':'#041E42'}),
                    dcc.Dropdown(id='select-indicator',
                                options=[{'label':x, 'value':x} for x in sorted(df.Measure.unique())],
                                multi=False,
                                value=df['Measure'].tolist()[0],
                                style={'width':'100%'},
                                optionHeight=90)
                ])
                
            ),
            dbc.Col([
                html.Div([
                    
                    dbc.Button('Edit Graph', id='edit-bc', outline=True, color="primary", className="me-1", value='monthly')
                ])
            ], width=2)
            
            
        ]),

    ]),
    
    dbc.Container(children=[
        dbc.Row([
            
            dbc.Col([
                html.Div([
                    dcc.Graph(id='graph', figure={})
                ]),
                
                ]),
            
            
        ])
    ]),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    dbc.Container(children=[
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H1(id='profiler-title',children=[('Port Analyzer')], style={'color':'#041E42'}),
                ])
            ], width=3),
            dbc.Col([
                html.Div([
                    dbc.Button(
                        "?",
                        id="click-target",
                        className="me-1",
                        n_clicks=0,
                        style={'color':'##FF8200'},
                        size='sm'
                    ),
                    dbc.Popover(
                        children='In this section, you can see information for every individual county at any given specific Year, as well as the distribution for every indicator at that given Year. Use the dropdowns to switch between counties and Years. You may also use the second row of the table to look for any specific value.',
                        target='click-target',
                        body=True,
                        trigger='click'
                    )
                ])
            ])
        ]),
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Label('Port', style={'font-weight':'bold'}),
                    dcc.Dropdown(id='county-prof-selector', 
                    options=[{'label':x, 'value':x} for x in sorted(df['Port'].unique())],
                    multi=False,
                    value=sorted(df['Port'].unique())[0])
                ])
            ]),
            dbc.Col([
                html.Div([
                    html.Label('Year', style={'font-weight':'bold'}),
                    dcc.Dropdown(id='Year-selector',
                    options=[{'label':i, 'value':i} for i in sorted(df['Year'].unique())],
                    multi=False,
                    value=sorted(df['Year'].unique())[0])
                ])
            ]),
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col([
                html.Div(id='table-loc',children=[
                    dash_table.DataTable(
                        id='profiler-table',
                        columns=[{'name':i, 'id':i} for i in toTable.columns],
                        data=toTable.to_dict('records'),
                        editable=True,
                        filter_action='native',
                        sort_action='native',
                        sort_mode='multi',
                        row_selectable=False,
                        row_deletable=False,
                        selected_columns=[],
                        selected_rows=[],
                        page_size=10,
                    )
                ])
            ]),
            dbc.Col([
                html.Div([
                    dcc.Graph(id='bar-chart', figure={})
                ])
            ])
        ]),
        html.Br()
    ])
    
    
    
    
    
    
]
)
@app.callback(
    Output('sidebar-space-bc','hidden'),
    [Input('edit-bc','n_clicks'),
    Input('sidebar-space-bc','hidden')]
)
def show_sidebar(button, showSidebar):
    trigger_id=ctx.triggered_id
    if(trigger_id=='edit-bc'):
        if(showSidebar):
            showSider=False
        else:
            showSidebar=True
    return showSidebar
    

@app.callback(
    [Output(component_id='graph', component_property='figure'), 
    Output(component_id='Number1', component_property='value'),  
    ],
    (Input(component_id='select-indicator', component_property='value'))
    
    
)
def update_indicator(indicator):
    dff=df.copy()
    dff['Date'] = pd.to_datetime(df['Date'], format='%y%m')
    dff=dff[dff['Measure']==indicator]
    trigger_id=ctx.triggered_id
    
    

    #dff=dff[(dff['Value']>=start1) & (dff['Value']<=end1)]
    
    fig=px.line(dff, x='Date', y='Value', title=indicator+' by Port ', color='Port')
    fig.update_xaxes(nticks=len(pd.unique(dff['Year'])), rangeslider_visible=True)
    
    

    
    
    
    
    #dff2=dff2[(dff2['Value']>=start2) & (dff2['Value']<=end2)]
    
    
    
    
    dff=dff[dff['Year']==dff['Year'].max()]
    
    return fig, sum(dff['Value'])



@app.callback(
    [Output(component_id='profiler-table', component_property='data'), Output(component_id='profiler-table', component_property='columns'),
    Output(component_id='bar-chart', component_property='figure')],
    [Input(component_id='county-prof-selector', component_property='value'), Input(component_id='Year-selector', component_property='value')]
    
)
def update_profiler(county, Year):
    df_profiler=df[df['Port']==county]
    df_profiler=df_profiler[df_profiler['Year']==Year]

    toTable=df_profiler[['Measure', 'Month', 'Value']]

    df_bar=df.copy()
    df_bar=df_bar[df_bar['Year']==Year]
    fig=px.bar(df_bar, x='Measure', y='Value', color='Port')

    return toTable.to_dict('records'), [{'name':i, 'id':i} for i in toTable.columns], fig
