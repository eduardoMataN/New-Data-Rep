
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
# type: ignore

PATH = pathlib.Path(__file__).parent #So this first line is going to the parent of the current path, which is the Multipage app. 
DATA_PATH = PATH.joinpath("../datasets").resolve() #Once we're on that path, we go into datasets. 
df_population= pd.read_excel(DATA_PATH.joinpath("Population by Language Spoken by County.xlsx"))
df_population['Value']=pd.to_numeric(df_population['Value'])
df_total= pd.read_excel(DATA_PATH.joinpath("Total Population.xlsx"))
df_total['Value']=pd.to_numeric(df_total['Value'])
df_pop_race=pd.read_excel(DATA_PATH.joinpath("Population Race.xlsx"))
df_pop_race['Population']=pd.to_numeric(df_pop_race['Population'])
df_fert=pd.read_excel(DATA_PATH.joinpath("Fertility Rates.xlsx"))

layout=html.Div(children=[
    dbc.Container(children=[
        dbc.Row([
            dbc.Col([
                html.H1(id='county-title1', children=['County'], style={'color':'#041E42'})  # type: ignore
            ]),
            dbc.Col([]),
            dbc.Col([
                html.H1(id='county-title2', children=['County'], style={'color':'#041E42'})  # type: ignore
            ])
        ]),
        dbc.Row([
            dbc.Col([
                daq.LEDDisplay(id='total-count1', value=10000, color='#FF8200') # type: ignore
            ]),
            dbc.Col([]),
            dbc.Col([
                daq.LEDDisplay(id='total-count2', value=10000, color='#FF8200') # type: ignore
            ])
        ]),
        dbc.Row([
            dbc.Col([
                html.H3(id='total-pop', children=['Total Population'], style={'color':'#FF8200'}) # type: ignore
            ]),
            dbc.Col([]),
            dbc.Col([
                html.H3(id='total-pop2', children='Total Population', style={'color':'#FF8200'}) # type: ignore
            ])
        ]),
        dbc.Row([
            dbc.Col([
                html.H2(children=['Population by Language Spoken'], style={'color':'#041E42'}) # type: ignore
            ])
        ]),
        dbc.Row([
            dbc.Col([
                html.Label(['County'], style={'font-weight':'bold'}), # type: ignore
                    dcc.Dropdown(id='select-county-pop', # type: ignore
                        options=[{'label':x, 'value':x} for x in sorted(df_population.County.unique())],
                        multi=False,
                        value=df_population['County'].unique()[0],
                        style={'width':'105%'},
                        optionHeight=90)
            ]),
            dbc.Col([
                html.Label(['Age'], style={'font-weight':'bold'}),
                dcc.Dropdown(id='select-age-pop',
                options=[{'label':x, 'value':x} for x in sorted(df_population.Age.unique())],
                multi=False,
                value=df_population['Age'].unique()[0],
                style={'width':'105%'},
                optionHeight=90)
            ]),
            dbc.Col([
                html.Label(['Language Spoken'], style={'font-weight':'bold'}),
                dcc.Dropdown(id='select-language-pop',
                options=[{'label':x, 'value':x} for x in sorted(df_population.Language.unique())],
                multi=False,
                value=df_population.Language.unique()[0],
                style={'width':'105%'},
                optionHeight=90)
            ]),
            dbc.Col([
                html.Label(['Year'], style={'font-weight':'bold'}),
                dcc.Dropdown(id='select-year-pop',
                options=[{'label':x, 'value':x}for x in sorted(df_population.Year.unique())],
                multi=False,
                value=df_population.Year.unique()[0],
                style={'width':'100%'},
                optionHeight=90)
            ], width=1),
            dbc.Col([
                html.Label(['County'], style={'font-weight':'bold'}),
                    dcc.Dropdown(id='select-county-pop2',
                        options=[{'label':x, 'value':x} for x in sorted(df_population.County.unique())],
                        multi=False,
                        value=df_population['County'].unique()[1],
                        style={'width':'105%'},
                        optionHeight=90)
            ]),
            dbc.Col([
                html.Label(['Age'], style={'font-weight':'bold'}),
                dcc.Dropdown(id='select-age-pop2',
                options=[{'label':x, 'value':x} for x in sorted(df_population.Age.unique())],
                multi=False,
                value=df_population['Age'].unique()[0],
                style={'width':'100%'},
                optionHeight=90)
            ]),
            dbc.Col([
                html.Label(['Language Spoken'], style={'font-weight':'bold'}),
                dcc.Dropdown(id='select-language-pop2',
                options=[{'label':x, 'value':x} for x in sorted(df_population.Language.unique())],
                multi=False,
                value=df_population.Language.unique()[0],
                style={'width':'100%'},
                optionHeight=90)
            ])
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col([
                daq.Tank(id='tank1',
                min=0,
                max=10,
                value=5,
                style={'margin-left': '225px'},
                height=250,
                label='Population',
                labelPosition='bottom',
                showCurrentValue=True,
                width=300)
            ]),
            dbc.Col([
                daq.Tank(id='tank2',
                min=0,
                max=10,
                value=5,
                style={'margin-left': '225px'},
                height=250,
                label='Population',
                labelPosition='bottom',
                showCurrentValue=True,
                width=300)
            ])
        ])
    ]),
    html.Br(),
    dbc.Container(children=[
        dbc.Row([
            dbc.Col(
                html.H2(children=['Population By Race'], style={'color':'#041E42'})
            ),
            dbc.Col([
                html.Label(['County'], style={'font-weight':'bold'}),
                    dcc.Dropdown(id='select-county-race',
                        options=[{'label':x, 'value':x} for x in sorted(df_pop_race.County.unique())],
                        multi=False,
                        value=df_pop_race['County'].unique()[0],
                        style={'width':'100%'},
                        optionHeight=90)
            ]),
            dbc.Col([
                html.Label(['Year'], style={'font-weight':'bold'}),
                dcc.Dropdown(id='select-year-race',
                options=[{'label':x, 'value':x}for x in sorted(df_pop_race.Year.unique())],
                multi=False,
                value=df_pop_race.Year.unique()[0],
                style={'width':'100%'},
                optionHeight=90)
            ])
        ]),
        dbc.Row([
            dbc.Col(
                html.H4(children=['White Alone'], style={'color':'#FF8200'})
            ),
            dbc.Col(
                html.H4(children=['Black or African American Alone'], style={'color':'#FF8200'})
            ),
            dbc.Col(
                html.H4(children=['American Indian and Alaska Native Alone'], style={'color':'#FF8200'})
            )
        ]),
        dbc.Row([
            dbc.Col(
                daq.Gauge(
                    id='gauge-white',
                    label='Population',
                    min=0,
                    max=10,
                    value=5,
                    showCurrentValue=True
                )
            ),
            dbc.Col(
                daq.Gauge(
                    id='gauge-black',
                    label='Population',
                    min=0,
                    max=10,
                    value=5,
                    showCurrentValue=True
                )
            ),
            dbc.Col(
                daq.Gauge(
                    id='gauge-indian',
                    label='Population',
                    min=0,
                    max=10,
                    value=5,
                    showCurrentValue=True
                )
            )
        ]),
        dbc.Row([
            dbc.Col(
                html.H4(children=['Asian Alone'], style={'color':'#FF8200'})
            ),
            dbc.Col(
                html.H4(children=['Native Hawaiian and Other Pacific Islander Alone'], style={'color':'#FF8200'})
            ), 
            dbc.Col(
                html.H4(children=['Some other race alone'], style={'color':'#FF8200'})
            )
        ]),
        dbc.Row([
            dbc.Col(
                daq.Gauge(
                    id='gauge-asian',
                    label='Population',
                    min=0,
                    max=10,
                    value=5,
                    showCurrentValue=True
                )
            ),
            dbc.Col(
                daq.Gauge(
                    id='gauge-hawai',
                    label='Population',
                    min=0,
                    max=10,
                    value=5,
                    showCurrentValue=True
                )
            ), 
            dbc.Col(
                daq.Gauge(
                    id='gauge-other',
                    label='Population',
                    min=0,
                    max=10,
                    value=5,
                    showCurrentValue=True
                )
            )
        ]),
        dbc.Row([
            dbc.Col(
                html.H4(children=['Two or more races'], style={'color':'#FF8200'})
            ),
            dbc.Col(
               html.H4(children=['Two races including some other race'], style={'color':'#FF8200'}) 
            ),
            dbc.Col(
                html.H4(children=['Two races excluding some other race, and three or more races'], style={'color':'#FF8200'})
            )
        ]),
        dbc.Row([
            dbc.Col(
                daq.Gauge(
                    id='gauge-two',
                    label='Population',
                    min=0,
                    max=10,
                    value=5,
                    showCurrentValue=True
                )
            ), 
            dbc.Col(
                daq.Gauge(
                    id='gauge-including',
                    label='Population',
                    min=0,
                    max=10,
                    value=5,
                    showCurrentValue=True
                )
            ),
            dbc.Col(
                daq.Gauge(
                    id='gauge-exclude',
                    label='Population',
                    min=0,
                    max=10,
                    value=5,
                    showCurrentValue=True
                )
            )
        ]),
        
       
    ]),
    dbc.Container(children=[
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H2(children=['Fertility Rates'], style={'color':'#041E42'})
                ])
                
            )
        ]),
        dbc.Row([
            dbc.Col([
                html.Label(['County'], style={'font-weight':'bold'}),
                dcc.Dropdown(id='select-county-fert',
                    options=[{'label':x, 'value':x} for x in sorted(df_fert.County.unique())],
                    multi=False,
                    value=df_fert['County'].unique()[0],
                    style={'width':'100%'},
                    optionHeight=90)
            ]),
            dbc.Col([
                html.Label(['Year'], style={'font-weight':'bold'}),
                dcc.Dropdown(id='select-year-fert',
                    options=[{'label':x, 'value':x}for x in sorted(df_fert.Year.unique())],
                    multi=False,
                    value=df_fert.Year.unique()[0],
                    style={'width':'100%'},
                    optionHeight=90)
            ]),
            dbc.Col([
                html.Label(['County'], style={'font-weight':'bold'}),
                dcc.Dropdown(id='select-county-fert2',
                    options=[{'label':x, 'value':x} for x in sorted(df_fert.County.unique())],
                    multi=False,
                    value=df_fert['County'].unique()[1],
                    style={'width':'100%'},
                    optionHeight=90)
            ])
            
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([
                    dcc.Graph(id='pie-fert-1', figure={})
                ])
            ),
            dbc.Col(
                html.Div([
                    dcc.Graph(id='pie-fert-2', figure={})
                ])
            )
        ])
    ])
])


@app.callback(
    [Output(component_id='tank1', component_property='value'), Output(component_id='tank1', component_property='max'),
    Output(component_id='tank2', component_property='value'), Output(component_id='tank2', component_property='max'),
    Output(component_id='county-title1', component_property='children'),
    Output(component_id='county-title2', component_property='children'),
    Output(component_id='total-count1', component_property='value'),
    Output(component_id='total-count2', component_property='value'),
    Output(component_id='gauge-white', component_property='value'), Output(component_id='gauge-white', component_property='max'), Output(component_id='gauge-white', component_property='min'),
    Output(component_id='gauge-black', component_property='value'), Output(component_id='gauge-black', component_property='max'), Output(component_id='gauge-black', component_property='min'),
    Output(component_id='gauge-indian', component_property='value'), Output(component_id='gauge-indian', component_property='max'), Output(component_id='gauge-indian', component_property='min'),
    Output(component_id='gauge-asian', component_property='value'), Output(component_id='gauge-asian', component_property='max'), Output(component_id='gauge-asian', component_property='min'),
    Output(component_id='gauge-hawai', component_property='value'), Output(component_id='gauge-hawai', component_property='max'), Output(component_id='gauge-hawai', component_property='min'),
    Output(component_id='gauge-other', component_property='value'), Output(component_id='gauge-other', component_property='max'), Output(component_id='gauge-other', component_property='min'),
    Output(component_id='gauge-two', component_property='value'), Output(component_id='gauge-two', component_property='max'), Output(component_id='gauge-two', component_property='min'),
    Output(component_id='gauge-including', component_property='value'), Output(component_id='gauge-including', component_property='max'), Output(component_id='gauge-including', component_property='min'),
    Output(component_id='gauge-exclude', component_property='value'), Output(component_id='gauge-exclude', component_property='max'), Output(component_id='gauge-exclude', component_property='min'),
    Output(component_id='pie-fert-1', component_property='figure'),
    Output(component_id='pie-fert-2', component_property='figure')],
    [Input(component_id='select-county-pop', component_property='value'),
    Input(component_id='select-county-pop2', component_property='value'),
    Input(component_id='select-age-pop', component_property='value'),
    Input(component_id='select-age-pop2', component_property='value'),
    Input(component_id='select-language-pop', component_property='value'),
    Input(component_id='select-language-pop2', component_property='value'),
    Input(component_id='select-year-pop', component_property='value'),
    Input(component_id='select-county-race', component_property='value'),
    Input(component_id='select-year-race', component_property='value'),
    Input(component_id='select-county-fert', component_property='value'),
    Input(component_id='select-year-fert', component_property='value'),
    Input(component_id='select-county-fert2', component_property='value')]
)
def update_data(county1, county2, age1, age2, language1, language2, year, countyR, yearR, countyF, yearF, countyF2):
    dfpop1=df_population.copy()
    dfpop2=df_population.copy()
    #Max, Min, Value
    categDic={'White alone':[], 'Black or African American alone':[], 'American Indian and Alaska Native alone':[], 'Asian alone':[], 'Native Hawaiian and Other Pacific Islander alone':[], 'Some other race alone':[], 'Two or more races:':[], 'Two races including Some other race':[], 'Two races excluding Some other race, and three or more races':[]}
    #test=dfpop1['Value'].max()
    #Tanks
    dfcount=df_total.copy()
    dfcount2=df_total.copy()
    dfpop1=dfpop1[(dfpop1['County']==county1)&(dfpop1['Age']==age1)&(dfpop1['Year']==year)]
    max1=dfpop1['Value'].max()
    dfpop1=dfpop1[dfpop1['Language']==language1]
    dfpop2=dfpop2[(dfpop2['County']==county2)&(dfpop2['Age']==age2)&(dfpop2['Year']==year)]
    max2=dfpop2['Value'].max()
    dfpop2=dfpop2[dfpop2['Language']==language2]
    dfcount=dfcount[(dfcount['County']==county1)&(dfcount['Year']==year)]
    dfcount2=dfcount2[(dfcount2['County']==county2)&(dfcount2['Year']==year)]

    #Gauges
    for category in categDic:
        df_race=df_pop_race.copy()
        df_race=df_race[(df_race['County']==countyR) & (df_race['Year']==yearR)]
        dfcount3=df_total.copy()
        dfcount3=dfcount3[(dfcount3['County']==countyR) & (dfcount3['Year']==yearR)]
        categDic[category].append(max(dfcount3['Value']))
        categDic[category].append(min(df_race['Population']))
        df_race=df_race[df_race['Race']==category]
        categDic[category].append(sum(df_race['Population']))

    #Pie Charts
    df_pie1=df_fert.copy()
    df_pie1=df_pie1[(df_pie1['County']==countyF) & (df_pie1['Year']==yearF)]
    fig=go.Figure(data=[go.Pie(labels=df_pie1['Age'], values=df_pie1['Percentage'])])

    df_pie2=df_fert.copy()
    df_pie2=df_pie2[(df_pie2['County']==countyF2) & (df_pie2['Year']==yearF)]
    fig2=go.Figure(data=[go.Pie(labels=df_pie2['Age'], values=df_pie2['Percentage'])])
        
    

    return sum(dfpop1['Value']), sum(dfcount['Value']), sum(dfpop2['Value']), sum(dfcount2['Value']), county1, county2, sum(dfcount['Value']), sum(dfcount2['Value']), categDic['White alone'][2], categDic['White alone'][0], 0, categDic['Black or African American alone'][2], categDic['Black or African American alone'][0], 0, categDic['American Indian and Alaska Native alone'][2], categDic['American Indian and Alaska Native alone'][0], 0, categDic['Asian alone'][2], categDic['Asian alone'][0], 0, categDic['Native Hawaiian and Other Pacific Islander alone'][2], categDic['Native Hawaiian and Other Pacific Islander alone'][0], 0, categDic['Some other race alone'][2], categDic['Some other race alone'][0],0, categDic['Two or more races:'][2],categDic['Two or more races:'][0], 0, categDic['Two races including Some other race'][2], categDic['Two races including Some other race'][0], 0, categDic['Two races excluding Some other race, and three or more races'][2], categDic['Two races excluding Some other race, and three or more races'][0], 0, fig, fig2