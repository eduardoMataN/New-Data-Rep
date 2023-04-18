
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


from apps import transportation_airport_activity_dip as Domestic
from apps import transportation_airport_activity_eps  as Statistics

subsectionDic={'Domestic':Domestic.layout, 'Statistics':Statistics.layout}


layout=html.Div(children=[
    html.Br(),
    dbc.Container(children=[
        dcc.Tabs(id='transport-tabs', children=[
            dcc.Tab(label='Domestic and International Air Passengers', value='Domestic', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='El Paso Passengers Statistics', value='Statistics', style=tab_style, selected_style=tab_selected_style)
        ], value='Domestic'),
        html.Br(),
        html.Div(id='subMenu-section-transport',children=[])
        
    ])
])


@app.callback(
    Output('subMenu-section-transport', 'children'),
    Input('transport-tabs','value')
)
def update_submenu(tabValue):
    try:
        return subsectionDic[tabValue]
    except:
        return Domestic.layout



# @app.callback(
#     [Output ('bar-air', 'figure'),
#     Output('bar-domes-int','figure'),
#     Output('select-mun-air', 'disabled')],
#     [
#     Input('select-year-airep', 'value'), 
#     Input('select-mun-air', 'value'),
#     Input('select-type-air','value'),
#     Input('select-year-air', 'value'),
#     Input('air-pwr','on')]
# )
# def update_data(yearEP, municipality, type, year, on):
#     dff=Statistics.df_ep.copy()
#     dff=dff[dff['Year']==yearEP]
#     fig=px.bar(dff, 'Month', 'Value', color='Type', color_discrete_sequence=get_colors(dff['Type'].unique()))
#     munDis=False
#     dff2=Domestic.df_domes_int.copy()
#     if(on==True):
#         dff3=dff2[(dff2['Municipality']=='Ciudad Juárez')&(dff2['Year']==year)&(dff2['Type']==type)]
#         dff4=dff2[(dff2['Municipality']=='Chihuahua')&(dff2['Year']==year)&(dff2['Type']==type)]
#         fig2=make_subplots(1,2)
#         fig2.add_trace(go.Bar(x=dff3['Month'], y=dff3['Value'], name='Ciudad Juárez'), 1, 1)
#         fig2.add_trace(go.Bar(x=dff4['Month'], y=dff4['Value'], name='Chihuahua'), 1, 2)
#         munDis=True
#     else:
#         dff2=dff2[(dff2['Municipality']==municipality)&(dff2['Year']==year)&(dff2['Type']==type)]
#         fig2=px.bar(dff2, 'Month', 'Value', hover_data=['Value'], color='Value', color_continuous_scale=['#041E42', '#FF8200', '#fff100'])
#     return fig, fig2, munDis