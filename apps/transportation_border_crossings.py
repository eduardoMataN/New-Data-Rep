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
from apps.common_items import *
from apps.dataset import *
from apps.dataBag import *
from dash import Dash, dcc, html, Input, Output
from app import app

PATH = pathlib.Path(__file__).parent #So this first line is going to the parent of the current path, which is the Multipage app. 
DATA_PATH = PATH.joinpath("../datasets").resolve() #Once we're on that path, we go into datasets. 
df= pd.read_excel(DATA_PATH.joinpath("Border Crossings.xlsx"))
borderCDataSet=dataset('Border Crossings', df, 'Value', 'graph', 'Port', 'Value')
borderCDataSet.modify_percent_change('Measure', 'Port', 'Value')
boderDataBag=dataBag([borderCDataSet])
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

from apps import transportation_border_crossing_bcg as Border
from apps import transportation_border_crossing_pa  as Port
subsectionDic={'Border':Border.layout, 'Port':Port.layout}


layout=html.Div(children=[
    html.Br(),
    dbc.Container(children=[
        dcc.Tabs(id='Crossing-tabs', children=[
            dcc.Tab(label='Port Analyzer', value='Border', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Border Crossing', value='Port', style=tab_style, selected_style=tab_selected_style)
        ], value='Border'),
        html.Br(),
        html.Div(id='subMenu-section-crossing',children=[])
        
    ])
])


@app.callback(
    Output('subMenu-section-crossing', 'children'),
    Input('Crossing-tabs','value')
)
def update_submenu(tabValue):
    try:
        return subsectionDic[tabValue]
    except:
        return Border.layout




@app.callback(
    Output('sidebar-space-bc','hidden'),
    [Input('edit-bc','n_clicks'),
    Input('sidebar-space-bc','hidden'),
    Input('chart-options-bc','value')]
)
def show_sidebar(button, showSidebar, graphMode):
    trigger_id=ctx.triggered_id
    if(trigger_id=='edit-bc'):
        if(showSidebar):
            showSidebar=False
        else:
            showSidebar=True
    boderDataBag.getDataframe().activateDataframe(graphMode)
    return showSidebar
    

@app.callback(
    [Output(component_id='graph', component_property='figure'), 
    Output(component_id='Number1', component_property='value'),  
    ],
    (Input(component_id='select-indicator', component_property='value'),
    Input('chart-options-bc','value'), Input('reset-bc','n_clicks'))
    
    
)
def update_indicator(indicator, dummyValue, resetButton):
    dff=boderDataBag.getDataframe().getActive().copy()
    dff['Date'] = pd.to_datetime(df['Date'], format='%y%m')
    dff=dff[dff['Measure']==indicator]
    trigger_id=ctx.triggered_id
    
    

    #dff=dff[(dff['Value']>=start1) & (dff['Value']<=end1)]
    
    fig=px.line(dff, x='Date', y='Value', title=indicator+' by Port ', color='Port')
    fig.update_xaxes(nticks=len(pd.unique(dff['Year'])), rangeslider_visible=True)
    if(dummyValue=='PercentChange'):
        fig.update_yaxes(tickformat='000',ticksuffix='%')
    
    
    

    
    
    
    
    #dff2=dff2[(dff2['Value']>=start2) & (dff2['Value']<=end2)]
    
    dff2=boderDataBag.getDataframe().get_original().copy()
    dff2['Date'] = pd.to_datetime(df['Date'], format='%y%m')
    dff2=dff2[dff2['Measure']==indicator]
    dff2=dff2[dff2['Year']==dff2['Year'].max()]
    
    return fig, sum(dff2['Value'])



@app.callback(
    [Output(component_id='profiler-table', component_property='data'),
    Output(component_id='profiler-table', component_property='columns'),
    Output(component_id='bar-chart', component_property='figure')],

    [Input(component_id='county-prof-selector', component_property='value'), 
     Input(component_id='Year-selector', component_property='value')]
)
def update_profiler(county, Year):
    df_profiler=df[df['Port']==county]
    df_profiler=df_profiler[df_profiler['Year']==Year]

    toTable=df_profiler[['Measure', 'Month', 'Value']]

    df_bar=df.copy()
    df_bar=df_bar[df_bar['Year']==Year]
    fig=px.bar(df_bar, x='Measure', y='Value', color='Port')

    return toTable.to_dict('records'), [{'name':i, 'id':i} for i in toTable.columns], fig
