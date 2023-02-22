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
from apps.common_items import *
from apps.dataset import *
from apps.dataBag import *

PATH = pathlib.Path(__file__).parent #So this first line is going to the parent of the current path, which is the Multipage app. 
DATA_PATH = PATH.joinpath("../datasets/Income").resolve() #Once we're on that path, we go into datasets. 
df_income= pd.read_excel(DATA_PATH.joinpath("Household_Family Income by Zip Code.xlsx"))
df_median=pd.read_excel(DATA_PATH.joinpath("Median Household income.xlsx")) #Might have to divide this. 
df_median_personal=df_median[df_median['Indicator']=='Personal Per Capita Income']
df_personal=df_median_personal.copy()
df_median_industry=df_median[df_median['Indicator']=='Earnings by Industry']
df_industry=df_median_industry.copy()
df_median_median=df_median[df_median['Indicator']=='Median Household Income']
df_median_final=df_median_median.copy()
personalDataset=dataset('Personal Per Capita Income Chart', df_personal, 'Income', 'Personal Per Capita Income', 'County', 'Income')
industryDataset=dataset('Earnings by Industry Chart', df_industry, 'Income', 'Earnings by Industry', 'County', 'Income')
industryDataset.modify_percent_change('Industry', 'County', 'Income')
medianDataset=dataset('Median Household Income Chart', df_median_final, 'Income', 'Median Household Income', 'County', 'Income')
medianDataset.modify_percent_change('Household Type', 'County', 'Income')


df_income_copy=df_income.copy()
#incomeDataset=dataset('Median Household & Personal Income Chart', df_median, 'Income', 'income', 'Indicator', 'Income')
#incomeDataset.modify_percent_change(['County', 'Household Type', 'Industry', 'Indicator'], 'County', 'Income')
df_income_zip=df_income_copy[~df_income_copy['ZIP'].isin(['Texas', 'El Paso County, Texas'])]
df_overall=df_income[df_income['ZIP'].isin(['Texas', 'El Paso County, Texas'])]
df_revenues=pd.read_excel(DATA_PATH.joinpath('Revenues by Workers Remittances, Distribution by municipality, Chihuahua, Juárez.xlsx'))
revenuesDataset=dataset('Revenues by Workers Remittances Chart', df_revenues, 'Dollars in Millions', name='revenues')
maxYear=df_income['Year'].max()
incomeDatabag=dataBag([personalDataset, medianDataset, industryDataset, revenuesDataset])
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
    dbc.Offcanvas(id='sidebar-space-income',children=[
        
    
        html.H6(id='sidebar-title-income',children='Border Patrol Agent Staffing'),
        html.Hr(),
        html.P(
            "Use the following buttons to edit the chart.", className="lead"
        ),
        dbc.RadioItems(
            id='chart-options-income',
            options=[
                {'label':'Percent Change','value':'PercentChange'},
                {'label': 'Original Chart','value':'Original'}
            ],
            value='Original',
            
        ),
        


        
    
    
    ], is_open=False),
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
                    value=df_median['Industry'].dropna().unique()[4],
                    style={'width':'100%'},
                    optionHeight=90,
                    disabled=True)
                ])
            , width=3),
            dbc.Col([
                html.Div([
                    dbc.Button('Edit Graph', id='edit-income', outline=True, color="primary", className="me-1", value='yearly', n_clicks=0)
                ], style={"padding": "0rem 0rem"})
            ], style={'margin-left': '0px', "padding": "0px 0px"}, width=2)
            
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
    dbc.Container([
        dbc.Row([
            dbc.Col([
            html.Div(children=[
                dbc.Row([
                    dbc.Col([
                        html.P(' Units: Dollars ($)', style={'color':blue, 'font-weight':'bold'})
                    ], width=3),
                    dbc.Col([
                        html.P('Last Update: 2020', style={'color':blue, 'font-weight':'bold'})
                    ], width=3),
                    dbc.Col([
                        html.P('Source: USA Gov', style={'color':blue, 'font-weight':'bold'})
                    ], width=3),
                    dbc.Col([
                html.Div([
                    dbc.Button('Download Dataset', id='download-bttn-income', outline=True, color="primary", className="me-1", value='yearly', n_clicks=0)
                ]),
                dcc.Download(id='download-income')
            ],  style={'margin-left': '0px', 'margin-right':'0px'}, width=2)
                ], align='center', justify='center')
            ])
            ]),
        ], align='center', justify='center'),
        html.Br(),
    html.Br(),
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
    dbc.Container([
        dbc.Row([
            dbc.Col([
            html.Div(children=[
                dbc.Row([
                    dbc.Col([
                        html.P(' Units: Dollars ($)', style={'color':blue, 'font-weight':'bold'})
                    ], width=3),
                    dbc.Col([
                        html.P('Last Update: 2020', style={'color':blue, 'font-weight':'bold'})
                    ], width=3),
                    dbc.Col([
                        html.P('Source: USA Gov', style={'color':blue, 'font-weight':'bold'})
                    ], width=3),
                    dbc.Col([
                html.Div([
                    dbc.Button('Download Dataset', id='download-bttn-income2', outline=True, color="primary", className="me-1", value='yearly', n_clicks=0)
                ]),
                dcc.Download(id='download-income2')
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
            dbc.Col(
                html.H2("Revenues by Workers Remittances. Chihuahua, Juarez.", style={'color':'#041E42'})
            )
        ]),
        dbc.Row([
            dbc.Col(
                dcc.Graph(id='line-rev', figure={})
            )
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
                        html.P('Last Update: April 2022', style={'color':blue, 'font-weight':'bold'})
                    ], width=3),
                    dbc.Col([
                        html.P('Source: USA Gov', style={'color':blue, 'font-weight':'bold'})
                    ], width=3),
                    dbc.Col([
                html.Div([
                    dbc.Button('Download Dataset', id='download-bttn-income3', outline=True, color="primary", className="me-1", value='yearly', n_clicks=0)
                ]),
                dcc.Download(id='download-income3')
            ],  style={'margin-left': '0px', 'margin-right':'1px'}, width=2)
                ], align='center', justify='center')
            ])
            ]),
        ], align='center', justify='center'),
        html.Br(),
    html.Br(),
    ]),
    
    
    
    
    
    
    
]

)
@app.callback(
    Output('download-income3','data'),
    Input('download-bttn-income3', 'n_clicks'),
    prevent_initial_call=True
)
def download_median(downloadB):

    return dcc.send_data_frame(df_revenues.to_excel, 'Revenues by Workers Remittances. Chihuahua, Juarez.xlsx')

@app.callback(
    Output('download-income2','data'),
    Input('download-bttn-income2', 'n_clicks'),
    prevent_initial_call=True
)
def download_median(downloadB):

    return dcc.send_data_frame(df_income.to_excel, 'Household Family Income by Zip Code.xlsx')

@app.callback(
    Output('download-income','data'),
    Input('download-bttn-income', 'n_clicks'),
    prevent_initial_call=True
)
def download_median(downloadB):

    return dcc.send_data_frame(df_median.to_excel, 'Median Household & Personal Income.xlsx')

@app.callback(
    [Output('sidebar-space-income','is_open'),
    Output('sidebar-title-income', 'children'),],
    [Input('edit-income', 'n_clicks'),
    Input('select-indicator','value'),
    Input('sidebar-space-income', 'hidden'),
    Input('chart-options-income', 'value'),
    Input('sidebar-title-income', 'children')]
)
def get_sidebar(button, indicatorValue, hideSideBar, graphMode, title):
    trigger_id=ctx.triggered_id
    
    if(trigger_id=='edit-income'):
        if(hideSideBar):
            hideSideBar=False
        else:
            hideSideBar=True
        title=incomeDatabag.getByName(indicatorValue).title
    
    
    incomeDatabag.getByName(indicatorValue).activateDataframe(graphMode)

    
    return hideSideBar, title

@app.callback(
    [Output(component_id='median-graph', component_property='figure'), Output(component_id='select-household', component_property='disabled'),
    Output(component_id='select-industry', component_property='disabled'), Output(component_id='line-rev', component_property='figure')],
    [Input(component_id='select-indicator', component_property='value'), Input(component_id='select-household', component_property='value'),
    Input(component_id='select-industry', component_property='value'), Input('chart-options-income', 'value')]
)
def update_median(ind, household, industry, chartType):
    drop1=True
    
    drop3=True
    
    dff=incomeDatabag.getByName(ind).getActive().copy()
    
    fig=make_subplots(rows=1, cols=1)
    if(ind=='Personal Per Capita Income'):
        drop1=True
        df_temp=dff[dff['Indicator']==ind]
        counties=df_temp['County'].unique()
        fig=create_subplot(fig, 1, 1, df_temp, 'Year', 'Income', 'County')
        fig.update_xaxes(rangeslider_visible=True)
        if(chartType=='PercentChange'):
            fig.update_yaxes(ticksuffix='%')
    
    if (ind=='Median Household Income'):
        drop1=False
        df_temp=dff[dff['Indicator']==ind]
        counties=df_temp['County'].unique()
        fig=create_subplot(fig, 1, 1, df_temp[df_temp['Household Type']==household], 'Year', 'Income', 'County')
        fig.update_xaxes(rangeslider_visible=True)
        if(chartType=='PercentChange'):
            fig.update_yaxes(ticksuffix='%')
    
    if (ind=='Earnings by Industry'):
        drop3=False
        df_temp=dff[dff['Indicator']==ind]
        df_temp=dff[dff['Industry']==industry]
        counties=df_temp['County'].unique()
        fig=create_subplot(fig, 1, 1, df_temp[df_temp['Industry']==industry], 'Year', 'Income', 'County')
        fig.update_xaxes(rangeslider_visible=True)
        if(chartType=='PercentChange'):
            fig.update_yaxes(ticksuffix='%')
        else:
            fig.update_yaxes(ticksuffix='M')
    dff_revenues=incomeDatabag.getByName('revenues').getActive().copy()
    fig3=px.line(dff_revenues, x='Date', y='Dollars in Millions')
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



