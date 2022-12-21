import dash
import dash_daq as daq
import dash_bootstrap_components as dbc
import os
import datetime
from dash import html
import pandas as pd
import plotly
import plotly.express as px

# Generador de callbacks para click sobre tarjetas
def basicViewGraphCBGenerator(kpiName, eventName):
    def callback(_,__):
        triggeringCB = dash.callback_context.triggered_prop_ids

        fig = plotly.graph_objs.Figure()
        lastWeekMeanSeries = thisWeekKPIs.groupby([thisWeekKPIs['Start Time'].dt.date])[kpiName].mean()
        df = pd.DataFrame({'Start Time':lastWeekMeanSeries.index, lastWeekMeanSeries.name: lastWeekMeanSeries.values})

        fig.update_layout(
            title={
                'text':kpiName if kpiName else "",
                'font':{'size':10}
                },
            autosize=False,
            width=300,
            height=300,
            margin={'t':50, 'r':10, 'l':10, 'autoexpand':True,},
            xaxis={'fixedrange':True},
            yaxis={'fixedrange':True},
        )

        fig.add_trace(
            plotly.graph_objs.Scatter(
                x=df['Start Time'],
                y=df[lastWeekMeanSeries.name],
                )
            )

        if len(triggeringCB.keys()) and (list(triggeringCB.keys())[0] == eventName):
            print(triggeringCB.keys())
            return fig

        return fig

    return callback

# Cargado del dataframe de donde se va a sacar la data
def queryDataFromDB(start_date=datetime.datetime.today() - datetime.timedelta(days=30), end_date=datetime.datetime.today()) -> pd.DataFrame:
    """
    TODO: Termina de implementarme.
    Esta funcion hace un query hacia la base de datos para obtener la data que se encuentra dentro del 
    rango de fechas especificado
    """
    root = 'assets/data/'
    dfs = []
    for _, _, names in os.walk(root):
        for name in names:
            path = root+name
            dfs.append(pd.read_csv(path))

    df = pd.concat(dfs, ignore_index=True)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['IP Pool Usage(%)'] = df['IP Pool Usage(%)'].str.rstrip('%').astype(float)
    return df[df['Start Time'] > start_date][df['Start Time'] < end_date]

kpiDF = queryDataFromDB()

thisWeekKPIs = kpiDF.copy(deep=True)

# Implementacion del grafico de las cargas pico de CPU y sus duraciones:
strList = list[str]
def figCombinator(columns: strList, argDF:pd.DataFrame=None)->dash.dcc.Graph:
    if len(columns) > 1:
        fig = px.scatter(argDF, x="Start Time", y=columns[0], color=columns[1],
                         title=columns[0], width=1000, height=500)
        fig.update_coloraxes(
                colorbar_title={
                    'side':'right'
                    })
    else:
        fig = px.scatter(argDF, x="Start Time", y=columns[0],
                         title=columns[0], width=1000, height=500)

    fig.update_layout(title_font_size=30)

    return dash.dcc.Graph(figure=fig, config={'displayModeBar':False, 'responsive':True, 'scrollZoom': True})

dash.register_page(__name__)

layout = html.Div(children=[
    html.H1(children='xGW Page'),
    dash.dcc.Tabs(id="xGW-tabs", value='basicView', children=[
        dash.dcc.Tab(label='Basic view', value='basicView', children=[
            dash.html.Div(id='basicTab',children=[
                dash.html.Div(className='card_container', children=[
                    dash.html.Div(id='cpu_card',className='infoCard', children=[
                        dash.html.H3('CPU Usage'),
                        dash.html.H4('Latest measurement'),
                        dash.html.Div(children=[
                            dash.html.Div(children=[
                                daq.Gauge(
                                    color={"gradient":True, "ranges":{"green":[0,4], "yellow":[4,8], "red": [8,10]}},
                                    value=thisWeekKPIs['Mean ratio of the CPU usage of the main processor(%)'].iloc[-1],
                                    label={'label':'Latest mean ratio of the CPU usage of the main processor(%)', 'style':{'font-size':'10px'}},
                                    max=10,  # TODO: Averiguar cual es el máximo de este KPI
                                    min=0,
                                    size=150,
                                    ),
                                daq.Gauge(
                                    color={"gradient":True, "ranges":{"green":[0,40], "yellow":[40,80], "red": [80,100]}},
                                    value=thisWeekKPIs['Peak load of CPU usage of the main processor(%)'].iloc[-1],
                                    label={'label':'Latest peak load of CPU usage of the main processor(%)', 'style':{'font-size':'10px'}},
                                    units='%',
                                    max=100,  # TODO: Averiguar cual es el máximo de este KPI
                                    min=0,
                                    size=150,
                                    ),
                                ], className='gaugeContainer'),

                            dash.html.Div(children=[
                                dash.html.H5('Longest duration of CPU Peak'),
                                dash.html.P(str(thisWeekKPIs['Duration of peak load of CPU usage of the main processor(s)'].max())+' secs'),
                                dash.html.P('at '+str(thisWeekKPIs['Peak load of CPU usage of the main processor(%)'].iloc[thisWeekKPIs['Duration of peak load of CPU usage of the main processor(s)'].argmax()])+"%"),
                                ], className='dataCard')
                            ], className='infoCardDataContainer')
                    ]),

                    dash.html.Div(id='ip_pool_usage', className='infoCard', children=[
                        dash.html.H3('IP Usage'),
                        dash.html.H4('Latest measurement'),

                        dash.html.Div(children=[
                            dash.html.Div(children=[
                                daq.Gauge(
                                    color={"gradient":True, "ranges":{"green":[0,40], "yellow":[40,80], "red": [80,100]}},
                                    value=thisWeekKPIs['IP Pool Usage(%)'].iloc[-1],
                                    label={'label':'IP Pool Usage(%)', 'style':{'font-size':'30px'}},
                                    max=100,  # TODO: Averiguar cual es el máximo de este KPI
                                    min=0,
                                    size=150,
                                    ),
                                ], className='progressDiv'),

                            dash.html.Div(children=[
                                dash.html.Div(children=[
                                    dash.html.H5('Total number of IP addresses in the PGW IP pool'),
                                    dash.html.P(str(thisWeekKPIs['Total number of IP addresses in the PGW IP pool'].mean())),
                                    dash.html.P('Δ'+str(thisWeekKPIs['Total number of IP addresses in the PGW IP pool'].std())),
                                    # dash.html.P('∇')
                                    ], className='dataCard'),
                                dash.html.Div(children=[
                                    dash.html.H5('Total number of IP addresses in the PGW IP pool'),
                                    dash.html.P(str(round(thisWeekKPIs['Number of assigned IP addresses in the PGW IP pool'].mean(), 2))),
                                    dash.html.P('Δ'+str(round(thisWeekKPIs['Number of assigned IP addresses in the PGW IP pool'].std(),2))),
                                    ], className='dataCard')
                                ], className='cardContainer')
                            ], className='infoCardDataContainer')
                        ]),
                    ]),
                    dash.html.Br(),
                    dash.html.Br(),
                    dash.html.H2('Latest week statistics'),
                    figCombinator(['Peak load of CPU usage of the main processor(%)','Duration of peak load of CPU usage of the main processor(s)'], thisWeekKPIs),
                    figCombinator(['Mean ratio of the CPU usage of the main processor(%)'], thisWeekKPIs),
                    figCombinator(['IP Pool Usage(%)', 'Number of assigned IP addresses in the PGW IP pool'], thisWeekKPIs),
                    figCombinator(['Total number of IP addresses in the PGW IP pool'], thisWeekKPIs),
                ])
            ]),
        dash.dcc.Tab(label='Advanced view', value='advancedView', id='advancedTabGraphTab',children=[
            html.Div(id='advancedTab', children=[
                html.Div(children=[
                    dash.html.H5('Selected KPIs'),
                    dash.dcc.Dropdown(options=kpiDF.columns[5:], value=[kpiDF.columns[7]], multi=True, id='kpiSelector', placeholder="Select a KPI"),
                    dash.html.Br(),
                    dash.html.H5('Date range selector'),
                    dash.dcc.DatePickerRange(
                        id='dateRange',
                        min_date_allowed=kpiDF['Start Time'].min() - datetime.timedelta(days=1),
                        max_date_allowed=kpiDF['Start Time'].max() + datetime.timedelta(days=1),
                        initial_visible_month=kpiDF['Start Time'].max(),
                        start_date=kpiDF['Start Time'].min().date(),
                        end_date=kpiDF['Start Time'].max().date() + datetime.timedelta(days=1),
                        ),
                    dash.html.Br(),
                    dash.html.Div(className='graphsContainer',children=[
                        dash.dcc.Graph(
                            id='advancedTabGraph',
                            figure={
                                'data':[{
                                    'type':'line'
                                    }],
                                'layout': {
                                    'margin':{'t':50, 'r':0},
                                    }
                                }
                            ),
                        dash.dcc.Graph(
                            id='dailyGraph',
                            figure={
                                'data':[{
                                    'type':'line'
                                    }],
                                'layout': {'margin':{'t':50, 'r':0}}
                                })
                        ]),
                    dash.html.Label('Statistical information'),
                    dash.dcc.Checklist(options=['std'], id='metricsCheckList', value=[]),
                    ]),
                html.Div(id='statsContainer'),
                ]),
            ]),
        ]),
    ])


# Refrescado del grafico primario
@dash.callback(
        dash.Output('advancedTabGraph', 'figure'),
        dash.Input('dateRange', 'start_date'),
        dash.Input('dateRange', 'end_date'),
        dash.Input('kpiSelector', 'value'),
        dash.Input('metricsCheckList', 'value')
        )
def dateChange_cb(start_date: datetime.datetime, end_date: datetime.datetime, selector: list, checklistOptions: list):
    kpiDF = queryDataFromDB(start_date, end_date)
    fig = plotly.graph_objs.Figure()

    fig.update_layout(title={
        'text':'Averaged view',
        'font':{
            'size':35
            }
        })

    if len(selector) > 0:
        for _, value in enumerate(selector):
            meanSeries = kpiDF.groupby([kpiDF['Start Time'].dt.date])[value].mean()
            stdSeries = kpiDF.groupby([kpiDF['Start Time'].dt.date])[value].std()
            df = pd.DataFrame({'Start Time':meanSeries.index, meanSeries.name: meanSeries.values, 'std': stdSeries.values})
            
            fig.add_trace(
                    plotly.graph_objs.Scatter(
                        x=df['Start Time'],
                        y=df[value],
                        error_y=dict(
                            type='data',
                            array=df['std'],
                            visible=True) if 'std' in checklistOptions else None
                        )
                    )
    return fig

# Refrescado del grafico secundario
@dash.callback(
        dash.Output('dailyGraph', 'figure'),
        dash.Input('advancedTabGraph', 'clickData'),
        dash.State('advancedTabGraph', 'figure'),
        dash.Input('kpiSelector', 'value'),
        )
def clicked_datapoint_cb(clickData, aggFigure, selector):
    triggeringCB = dash.callback_context.triggered_prop_ids
    fig = plotly.graph_objs.Figure()
    fig.update_layout(title={
        'text':'Daily detail',
        'font':{
            'size':35
            }
        })

    try:
        if list(triggeringCB.keys())[0] == 'advancedTabGraph.clickData':
            dateToInspect = pd.to_datetime(clickData['points'][0]['x']).date()
        else:
            dateToInspect = pd.to_datetime(aggFigure['data'][0]['x'][-1]).date()
    except:
        return fig

    if selector:
        filteredDF = kpiDF[ kpiDF['Start Time'].apply(lambda x: pd.to_datetime(x).date()) == dateToInspect]
        for _, value in enumerate(selector):
            fig.add_trace(plotly.graph_objs.Scatter(
                x=filteredDF['Start Time'],
                y=filteredDF[value],
                ))

    return fig
