import pandas as pd
import plotly.express as px
import dash as dash
from dash import dcc, ctx
from dash import html
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash.dependencies import Input, Output, State
import pathlib
from app import app
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from apps.dataset import *
from apps.dataBag import *

PATH = pathlib.Path(__file__).parent #So this first line is going to the parent of the current path, which is the Multipage app. 
DATA_PATH = PATH.joinpath("../datasets/Income").resolve() #Once we're on that path, we go into datasets. 
df_income= pd.read_excel(DATA_PATH.joinpath("Household_Family Income by Zip Code.xlsx"))
df_median=pd.read_excel(DATA_PATH.joinpath("Median Household income.xlsx"))
df_income_copy=df_income.copy()
#incomeDataset=dataset('Median Household & Personal Income Chart', df_median, 'Income', 'income', 'Indicator', 'Income')
#incomeDataset.modify_percent_change(['County', 'Household Type', 'Industry', 'Indicator'], 'County', 'Income')
df_income_zip=df_income_copy[~df_income_copy['ZIP'].isin(['Texas', 'El Paso County, Texas'])]
df_overall=df_income[df_income['ZIP'].isin(['Texas', 'El Paso County, Texas'])]
df_revenues=pd.read_excel(DATA_PATH.joinpath('Revenues by Workers Remittances, Distribution by municipality, Chihuahua, Juárez.xlsx'))
revenuesDataset=dataset('Revenues by Workers Remittances Chart', df_revenues, 'Dollars in Millions', name='revenues')
maxYear=df_income['Year'].max()

df_median=pd.read_excel(DATA_PATH.joinpath("Median Household income.xlsx"))

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
    dbc.Container(children=[
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H1(id='Port-Title-income',  style={'color':'#041E42', 'text-align':'center'})
                    
                ]),
            ),
            dbc.Col(
                html.Div([
                    html.H1(id='section-title-income', children=['Economic Indicators'], style={'color':'#041E42', 'text-align':'center'})
                ])
            ),
            dbc.Col(
                html.Div([
                    html.H1(id='Port-Title2-income', style={'color':'#041E42', 'text-align':'center'})
                ])
            )
            
        ])
    ]),
    dbc.Container(children=[
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H2(id='median-income-title', children=['Median Household & Personal Income'], style={'color':'#041E42'})
                ])
            )
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.Label('Indicator', style={'font-weight':'bold'}),
                    dcc.Dropdown(id='select-indicator',
                    options=[{'label':x, 'value':x} for x in df_median['Indicator'].unique()],
                    multi=False,
                    value=df_median['Indicator'].tolist()[0],
                    style={'width':'100%'},
                    optionHeight=90)
                ])
            ),
            dbc.Col(
                html.Div([
                    html.Label('Household Type', style={'font-weight':'bold'}),
                    dcc.Dropdown(id='select-household',
                    options=[{'label':x, 'value':x} for x in df_median['Household Type'].dropna().unique()],
                    multi=False,
                    value=df_median['Household Type'].dropna().unique()[0],
                    style={'width':'100%'},
                    optionHeight=90,
                    disabled=True)
                ])
            ),
            dbc.Col(
                html.Div([
                    html.Label('Industry', style={'font-weight':'bold'}),
                    dcc.Dropdown(id='select-industry',
                    options=[{'label':x, 'value':x} for x in df_median['Industry'].dropna().unique()],
                    multi=False,
                    value=df_median['Industry'].dropna().unique()[0],
                    style={'width':'100%'},
                    optionHeight=90,
                    disabled=True)
                ])
            ),
            
        ])
    ]),
    dbc.Container(children=[
        dbc.Row([
            dbc.Col(
                html.Div([
                    dcc.Graph(id='median-graph', figure={})
                ])
            )
        ])
    ]),
    dbc.Container(children=[
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H2(id='households-title', children=['Household Family Income by Zip Code'], style={'color':'#041E42'})
                ])
            )
        ])
    ]),
    dbc.Container(children=[
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.Label('Zip Code', style={'font-weight':'bold'}),
                    dcc.Dropdown(id='select-zip',
                    options=[{'label':x, 'value':x} for x in df_income_zip['ZIP'].unique()],
                    multi=False,
                    value=df_income_zip['ZIP'].tolist()[0],
                    style={'width':'100%'},
                    optionHeight=90)
                    
                ])
            ),
            dbc.Col(
                html.Div([
                    html.Label('Year', style={'font-weight':'bold'}),
                    dcc.Dropdown(id='select-year',
                    options=[{'label':x, 'value':x} for x in df_income_zip['Year'].unique()],
                    multi=False,
                    value=df_income_zip['Year'].tolist()[0],
                    style={'width':'100%'},
                    optionHeight=90)
                    
                ])
            )
            
        ])
    ]),
    dbc.Container(children=[
        dbc.Row([
            dbc.Col(
                html.Div([
                    dcc.Graph(id='pie-income', figure={})
                ])
            )
            
        ])
    ]),
    dbc.Container(children=[
        dbc.Row([
            dbc.Col(
                html.Div([
                    dcc.Graph(id='pie-ep', figure={})
                ])
            ),
            dbc.Col(
                html.Div([
                    dcc.Graph(id='pie-tx', figure={})
                ])
            )
        ])
    ]),
    dbc.Container(children=[
        dbc.Row([
            dbc.Col(
                html.H2("Revenues by Workers Remittances. Chihuahua, Juarez.", style={'color':'#041E42'})
            )
        ]),
        dbc.Row([
            dbc.Col(
                dcc.Graph(id='line-rev', figure={})
            )
        ])
    ])
    
    
    
    
    
    
]

)
@app.callback(
    [Output(component_id='median-graph', component_property='figure'), Output(component_id='select-household', component_property='disabled'),
    Output(component_id='select-industry', component_property='disabled'), Output(component_id='line-rev', component_property='figure')],
    [Input(component_id='select-indicator', component_property='value'), Input(component_id='select-household', component_property='value'),
    Input(component_id='select-industry', component_property='value')]
)
def update_median(ind, household, industry):
    drop1=True
    
    drop3=True
    
    dff=df_median.copy()
    
    fig=make_subplots(rows=1, cols=1)
    if(ind=='Personal Per Capita Income'):
        drop1=True
        df_temp=dff[dff['Indicator']==ind]
        counties=df_temp['County'].unique()
        for county in counties:
            df_ind=df_temp[df_temp['County']==county]
            x=df_ind['Year']
            y=df_ind['Income']
            fig.add_trace(go.Scatter(x=x, y=y, name=county), row=1, col=1)
        fig.update_xaxes(rangeslider_visible=True)
    
    if (ind=='Median Household Income'):
        drop1=False
        df_temp=dff[dff['Indicator']==ind]
        counties=df_temp['County'].unique()
        for county in counties:
            df_ind=df_temp[(df_temp['County']==county) &(df_temp['Household Type']==household)]
            x=df_ind['Year']
            y=df_ind['Income']
            fig.add_trace(go.Scatter(x=x, y=y, name=county), row=1, col=1)
        fig.update_xaxes(rangeslider_visible=True)
    
    if (ind=='Earnings by Industry'):
        drop3=False
        df_temp=dff[dff['Indicator']==ind]
        #df_temp=dff[dff['Industry']==industry]
        counties=df_temp['County'].unique()
        for county in counties:
            df_ind=df_temp[(df_temp['County']==county) & (df_temp['Industry']==industry)]
            x=df_ind['Year']
            y=df_ind['Income'].dropna()
            fig.add_trace(go.Scatter(x=x, y=y, name=county), row=1, col=1)
        fig.update_xaxes(rangeslider_visible=True)
    fig3=px.line(df_revenues, x='Date', y='Dollars in Millions')
    fig3.update_layout(yaxis_tickprefix='$')
    fig3.update_xaxes(rangeslider_visible=True)
    return fig, drop1, drop3, fig3



        


@app.callback(
    [Output(component_id='pie-income', component_property='figure'),
    Output(component_id='pie-ep', component_property='figure'), Output(component_id='pie-tx', component_property='figure')],
    [Input(component_id='select-zip', component_property='value'), 
    Input(component_id='select-year', component_property='value'),
    ]
)
def update_pie(zip, year):
    dff=df_income.copy()
    df_zip=dff[~dff['ZIP'].isin(['Texas', 'El Paso County, Texas'])]
    df_overall=dff[dff['ZIP'].isin(['Texas', 'El Paso County, Texas'])]
    


    df_zip=df_zip[(df_zip['ZIP']==zip) & (df_zip['Year']==year)]
    
    df_ep=df_overall[(df_overall['ZIP']== 'El Paso County, Texas') & (df_overall['Year']==year)]
    df_tx=df_overall[(df_overall['ZIP']== 'Texas') & (df_overall['Year']==year)]
    fig=px.pie(df_zip, values='Income', names='HouseholdsTypes')
    
    fig_ep=px.pie(df_ep, values='Income', names='HouseholdsTypes', title='El Paso Households Income', color_discrete_sequence=px.colors.sequential.Sunset)
    fig_tx=px.pie(df_tx, values='Income', names='HouseholdsTypes', title='Texas Household Income', color_discrete_sequence=px.colors.sequential.Sunset)

    return fig,  fig_ep, fig_tx



