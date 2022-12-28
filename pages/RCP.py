import dash
import sys
import dash_daq as daq
import dash_bootstrap_components as dbc
import datetime
from dash import html
import pandas as pd
import plotly

sys.path.insert(1,'./pages')
import utilidadesVarias as uv

# Carga de los dataframes de donde se va a obtener la data
kpiDF_RCP = uv.queryDataFromDB(element='RCP')
thisWeekKPIs_RCP = kpiDF_RCP.copy(deep=True)

dash.register_page(__name__)

layout = html.Div(children=[
    html.H1(children='RCP Page'),
    dash.dcc.Tabs(id="RCP-tabs", value='basicView', children=[
        dash.dcc.Tab(label='Basic view', value='basicView', children=[
            dash.html.Div(id='basicTab_RCP',children=[
                dash.html.Div(className='card_container', children=[
                    dash.html.Div(id='cpu_card_RCP',className='infoCard', children=[
                        dash.html.H3('CPU Usage'),
                        dash.html.H4('Latest measurements'),
                        dash.html.Div(children=[
                            dash.html.Div(children=[
                                dash.html.Div(children=[
                                    dash.html.H6('Peak CPU Utilization(%)(discarded)'),
                                    daq.Gauge(
                                        color={"gradient":True, "ranges":{"green":[0,40], "yellow":[40,80], "red": [80,100]}},
                                        value=thisWeekKPIs_RCP['Peak CPU Utilization(%)(discarded)'].iloc[-1],
                                        max=100,  # TODO: Averiguar cual es el máximo de este KPI
                                        min=0,
                                        size=100,
                                        ),
                                ], className='gaugeDiv'),
                                dash.html.Div(children=[
                                    dash.html.H6('Average CPU Utilization(%)(discarded)'),
                                    daq.Gauge(
                                        color={"gradient":True, "ranges":{"green":[0,40], "yellow":[40,80], "red": [80,100]}},
                                        value=thisWeekKPIs_RCP['Average CPU Utilization(%)(discarded)'].iloc[-1],
                                        units='%',
                                        max=100,  # TODO: Averiguar cual es el máximo de este KPI
                                        min=0,
                                        size=100,
                                        ),
                                ], className='gaugeDiv'),
                                ], className='gaugeContainer'),
                            dash.html.Br(),
                            dash.html.H4('Week summary'),
                            dash.html.Div(children=[
                                dash.html.H5('General CPU load'),
                                dbc.ListGroup(children=[
                                    dbc.ListGroupItem('Mean peak CPU utilization: '+ str(thisWeekKPIs_RCP['Peak CPU Utilization(%)(discarded)'].mean())+'%'),
                                    dbc.ListGroupItem('Average CPU Utilization: '+str(round(thisWeekKPIs_RCP['Average CPU Utilization(%)(discarded)'].mean(), 2))+"%")
                                ]),
                            ]),
                            dash.html.Br(),
                            dash.html.Div(children=[
                                dash.html.H5('Peak load of CPU(%) (week summary)'),
                                dash.dcc.Graph(id='daily_cpu_usage_RCP', figure={}, config={'displayModeBar':False, 'responsive':True, 'scrollZoom': True}),
                            ], className='figureContainer')

                            ], className='infoCardDataContainer')
                    ]),

                    dash.html.Div(id='memory_card_RCP',className='infoCard', children=[
                        dash.html.H3('Memory Usage'),
                        dash.html.H4('Latest measurements'),
                        dash.html.Div(children=[
                            dash.html.Div(children=[
                                dash.html.Div(children=[
                                    dash.html.H6('Average Memory Utilization(%)'),
                                    daq.Gauge(
                                        color={"gradient":True, "ranges":{"green":[0,40], "yellow":[40,80], "red": [80,100]}},
                                        value=thisWeekKPIs_RCP['Average Memory Utilization(%)'].iloc[-1],
                                        max=100,  # TODO: Averiguar cual es el máximo de este KPI
                                        min=0,
                                        size=100,
                                        ),
                                ], className='gaugeDiv'),
                                dash.html.Div(children=[
                                    dash.html.H6('Peak Memory Utilization(%)(discarded)'),
                                    daq.Gauge(
                                        color={"gradient":True, "ranges":{"green":[0,40], "yellow":[40,80], "red": [80,100]}},
                                        value=thisWeekKPIs_RCP['Peak Memory Utilization(%)(discarded)'].iloc[-1],
                                        units='%',
                                        max=100,  # TODO: Averiguar cual es el máximo de este KPI
                                        min=0,
                                        size=100,
                                        ),
                                ], className='gaugeDiv'),
                                ], className='gaugeContainer'),
                            dash.html.Br(),
                            dash.html.H4('Week summary'),
                            dash.html.Div(children=[
                                dash.html.H5('General memory load'),
                                dbc.ListGroup(children=[
                                    dbc.ListGroupItem('Mean peak Memory utilization: '+ str(thisWeekKPIs_RCP['Peak Memory Utilization(%)(discarded)'].mean())+'%'),
                                    dbc.ListGroupItem('Average Memory Utilization: '+str(round(thisWeekKPIs_RCP['Average Memory Utilization(%)'].mean(), 2))+"%")
                                ]),
                            ]),
                            dash.html.Br(),
                            dash.html.Div(children=[
                                dash.html.H5('Peak Memory Utilization(%)(discarded)'),
                                dash.dcc.Graph(id='daily_memory_usage_RCP', figure={}, config={'displayModeBar':False, 'responsive':True, 'scrollZoom': True}),
                            ], className='figureContainer')

                            ], className='infoCardDataContainer')
                    ]),

                    ]),
                ])
            ]),
        dash.dcc.Tab(label='Advanced view', value='advancedView', id='advancedTabGraphTab_RCP',children=[
            html.Div(id='advancedTab_RCP', children=[
                html.Div(children=[
                    dash.html.H5('Selected KPIs'),
                    dash.dcc.Dropdown(options=kpiDF_RCP.columns[5:], value=[kpiDF_RCP.columns[7]], multi=True, id='kpiSelector_RCP', placeholder="Select a KPI"),
                    dash.html.Br(),
                    dash.html.H5('Date range selector'),
                    dash.dcc.DatePickerRange(
                        id='dateRange_RCP',
                        min_date_allowed=kpiDF_RCP['Start Time'].min() - datetime.timedelta(days=1),
                        max_date_allowed=kpiDF_RCP['Start Time'].max() + datetime.timedelta(days=1),
                        initial_visible_month=kpiDF_RCP['Start Time'].max(),
                        start_date=kpiDF_RCP['Start Time'].min().date(),
                        end_date=kpiDF_RCP['Start Time'].max().date() + datetime.timedelta(days=1),
                        ),
                    dash.html.Br(),
                    dash.html.Div(className='graphsContainer',children=[
                        dash.dcc.Graph(
                            id='advancedTabGraph_RCP',
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
                            id='dailyGraph_RCP',
                            figure={
                                'data':[{
                                    'type':'line'
                                    }],
                                'layout': {'margin':{'t':50, 'r':0}}
                                })
                        ]),
                    dash.html.Label('Statistical information'),
                    dash.dcc.Checklist(options=['std'], id='metricsCheckList_RCP', value=[]),
                    ]),
                html.Div(id='statsContainer_RCP'),
                ]),
            ]),
        ]),
    ])

# Callbacks para el advancedView
## Refrescado del grafico primario
dash.callback(
        dash.Output('advancedTabGraph_RCP', 'figure'),
        dash.Input('dateRange_RCP', 'start_date'),
        dash.Input('dateRange_RCP', 'end_date'),
        dash.Input('kpiSelector_RCP', 'value'),
        dash.Input('metricsCheckList_RCP', 'value')
        )(uv.dateChangeCBGen(kpiDF_RCP))

## Refrescado del grafico secundario
dash.callback(
        dash.Output('dailyGraph_RCP', 'figure'),
        dash.Input('advancedTabGraph_RCP', 'clickData'),
        dash.State('advancedTabGraph_RCP', 'figure'),
        dash.Input('kpiSelector_RCP', 'value'),
        )(uv.clickedDatapointCBGen(kpiDF_RCP, 'advancedTabGraph_RCP.clickData'))

# Callbacks para los graficos de las cartas
## Tarjeta para el uso de CPU
dash.callback(
                dash.Output('daily_cpu_usage_RCP', 'figure'),
                dash.Input('daily_cpu_usage_RCP', 'figure'),
                dash.Input('daily_cpu_usage_RCP', 'clickData'),
                )(uv.basicViewGraphCBGenerator('Peak CPU Utilization(%)(discarded)', 'daily_cpu_usage.clickData', thisWeekKPIs_RCP, kpiDF_RCP))

## Tarjeta para el uso de memoria
dash.callback(
                dash.Output('daily_memory_usage_RCP', 'figure'),
                dash.Input('daily_memory_usage_RCP', 'figure'),
                dash.Input('daily_memory_usage_RCP', 'clickData'),
                )(uv.basicViewGraphCBGenerator('Average Memory Utilization(%)', 'daily_ip_usage.clickData', thisWeekKPIs_RCP, kpiDF_RCP))
