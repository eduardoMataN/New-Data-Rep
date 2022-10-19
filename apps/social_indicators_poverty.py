from turtle import width
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

PATH = pathlib.Path(__file__).parent #So this first line is going to the parent of the current path, which is the Multipage app. 
DATA_PATH = PATH.joinpath("../datasets").resolve() #Once we're on that path, we go into datasets. 
df_age=pd.read_excel(DATA_PATH.joinpath('Poverty by Age.xlsx'))
df_sex=pd.read_excel(DATA_PATH.joinpath('Poverty by Sex.xlsx'))
df_educ=pd.read_excel(DATA_PATH.joinpath('Poverty by Educational Attainment.xlsx'))
df_race=pd.read_excel(DATA_PATH.joinpath('Poverty by Race.xlsx'))

layout=html.Div([
    dbc.Container([
    dcc.Tabs(id='poverty-tabs', value='tab-age', children=[
        dcc.Tab(label='By Age', value='tab-age'),
        dcc.Tab(label='By Race', value='tab-race'),
        dcc.Tab(label='By Sex', value='tab-sex'),
        dcc.Tab(label='By Educational Attainment', value='tab-educ')
    ])]),
    html.Br(),
    html.Div(id='content-div', children=[
        dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H2(id='section-title',children=['Poverty By Age'], style=TITLE)
                ])
            ])
        ])
    ]),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Label(id='county-dropdown-label', children=['County'], style=LABEL),
                    dcc.Dropdown(
                        id='select-county',
                        options=[{'label':x, 'value':x}for x in df_age['County'].unique()],
                        value=df_age['County'].unique()[0],
                        style=DROPDOWN,
                        optionHeight=90,
                        disabled=False
                    )
                ])
            ]),
            dbc.Col([
                html.Div([
                    html.Label(id='category-dropdown-label',children=['Age'], style=LABEL),
                    dcc.Dropdown(
                        id='select-category',
                        options=[{'label':x,'value':x}for x in df_age['Age'].unique()],
                        value=df_age['Age'].unique()[0],
                        style=DROPDOWN,
                        optionHeight=90,
                        disabled=True
                    )
                ])
            ]),
            dbc.Col([
                html.Div([
                    daq.ToggleSwitch(
                        id='toggle-poverty',
                        label='By County/By Age',
                        labelPosition='bottom',
                        value=False,
                        style=LABEL,
                        disabled=False
                    )
                ])
            ], width=2)
        ])
    ]),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Graph(
                        id='poverty-graph',
                        figure={}
                    )
                ])
            ])
        ])
    ])
    ])
])


@app.callback(
    [Output('section-title', 'children'),
    Output('select-county','options'), Output('select-county','value'), Output('select-county','disabled'),
    Output('category-dropdown-label','children'), Output('select-category','options'), Output('select-category','value'), Output('select-category','disabled'),
    Output('toggle-poverty','label'),
    Output('poverty-graph','figure')],
    [Input('poverty-tabs', 'value'),
    Input('select-county','options'), Input('select-county','value'),
    Input('select-category','options'), Input('select-category','value'),
    Input('toggle-poverty','value'), Input('toggle-poverty','label')]
)
def update_content(tab, countyOptions, countyValue, categoryOptions, categoryValue, toggleValue, toggleLabel):
    trigger_id=ctx.triggered_id
    categoryLabel=['Age']
    disableCounty=False
    disableCategory=False
    if(tab=='tab-age'):
        dff=df_age.copy()
        title=['Poverty By Age']
        if(trigger_id=='poverty-tabs'):
            countyOptions=[{'label':x,'value':x}for x in dff['County'].unique()]
            countyValue=dff['County'].unique()[0]
            categoryOptions=[{'label':x,'value':x}for x in dff['Age'].unique()]
            categoryValue=dff['Age'].unique()[0]
            categoryLabel=['Age']
            toggleLabel='By County/By Age'
        if(toggleValue):
            dff=dff[dff['Age']==categoryValue]
            fig=px.line(dff,x='Year',y='Percentage',color='County')
            disableCounty=True
        else:
            dff=dff[dff['County']==countyValue]
            fig=px.line(dff, x='Year',y='Percentage', color='Age')
            disableCategory=True
            
        
    elif(tab=='tab-race'):
        dff=df_race.copy()
        title=['Poverty By Race']
        if(trigger_id=='poverty-tabs'):
            countyOptions=[{'label':x,'value':x}for x in dff['County'].unique()]
            countyValue=dff['County'].unique()[0]
            categoryOptions=[{'label':x,'value':x}for x in dff['Race'].unique()]
            categoryValue=dff['Race'].unique()[0]
            categoryLabel=['Race']
            toggleLabel='By County/By Race'
        if(toggleValue):
            dff=dff[dff['Race']==categoryValue]
            fig=px.line(dff,x='Year',y='Percentage',color='County')
            disableCounty=True
        else:
            dff=dff[dff['County']==countyValue]
            fig=px.line(dff, x='Year',y='Percentage', color='Race')
            disableCategory=True
        
    elif(tab=='tab-sex'):
        dff=df_sex.copy()
        title=['Poverty By Sex']
        if(trigger_id=='poverty-tabs'):
            countyOptions=[{'label':x,'value':x}for x in dff['County'].unique()]
            countyValue=dff['County'].unique()[0]
            categoryOptions=[{'label':x,'value':x}for x in dff['Sex'].unique()]
            categoryValue=dff['Sex'].unique()[0]
            categoryLabel=['Sex']
            toggleLabel='By County/By Sex'
        if(toggleValue):
            dff=dff[dff['Sex']==categoryValue]
            fig=px.line(dff,x='Year',y='Percentage',color='County')
            disableCounty=True
        else:
            dff=dff[dff['County']==countyValue]
            fig=px.line(dff, x='Year',y='Percentage', color='Sex')
            disableCategory=True
        
    elif(tab=='tab-educ'):
        dff=df_educ.copy()
        title=['Poverty By Educational Attainment']
        if(trigger_id=='poverty-tabs'):
            countyOptions=[{'label':x,'value':x}for x in dff['County'].unique()]
            countyValue=dff['County'].unique()[0]
            categoryOptions=[{'label':x,'value':x}for x in dff['Educational Attainment'].unique()]
            categoryValue=dff['Educational Attainment'].unique()[0]
            categoryLabel=['Educational Attainment']
            toggleLabel='By County/By Educational Attainment'
        if(toggleValue):
            dff=dff[dff['Educational Attainment']==categoryValue]
            fig=px.line(dff,x='Year',y='Percentage',color='County')
            disableCounty=True
        else:
            dff=dff[dff['County']==countyValue]
            fig=px.line(dff, x='Year',y='Percentage', color='Educational Attainment')
            disableCategory=True
        
    else:
        title=['Poverty By Age']
        dff=df_age.copy()
        title=['Poverty By Age']
        if(trigger_id=='poverty-tabs'):
            countyOptions=[{'label':x,'value':x}for x in dff['County'].unique()]
            countyValue=dff['County'].unique()[0]
            categoryOptions=[{'label':x,'value':x}for x in dff['Age'].unique()]
            categoryValue=dff['Age'].unique()[0]
            categoryLabel=['Age']
            toggleLabel='By County/By Age'
        if(toggleValue):
            dff=dff[dff['Age']==categoryValue]
            fig=px.line(dff,x='Year',y='Percentage',color='County')
            disableCounty=True
        else:
            dff=dff[dff['County']==countyValue]
            fig=px.line(dff, x='Year',y='Percentage', color='Age')
            disableCategory=True
    
    return title, countyOptions, countyValue, disableCounty, categoryLabel,categoryOptions, categoryValue, disableCategory,toggleLabel, fig
