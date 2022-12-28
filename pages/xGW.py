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
kpiDF_xGW = uv.queryDataFromDB()
thisWeekKPIs = kpiDF_xGW.copy(deep=True)

dash.register_page(__name__)

layout = html.Div(children=[
    html.H1(children='xGW Page'),
    dash.dcc.Tabs(id="xGW-tabs", value='basicView', children=[
        dash.dcc.Tab(label='Basic view', value='basicView', children=[
            dash.html.Div(id='basicTab_xGW',children=[
                dash.html.Div(className='card_container', children=[
                    dash.html.Div(id='cpu_card_xGW',className='infoCard', children=[
                        dash.html.H3('CPU Usage'),
                        dash.html.H4('Latest measurements'),
                        dash.html.Div(children=[
                            dash.html.Div(children=[
                                dash.html.Div(children=[
                                    dash.html.H6('Mean ratio of the CPU usage of the main processor(%)'),
                                    daq.Gauge(
                                        color={"gradient":True, "ranges":{"green":[0,4], "yellow":[4,8], "red": [8,10]}},
                                        value=thisWeekKPIs['Mean ratio of the CPU usage of the main processor(%)'].iloc[-1],
                                        max=10,  # TODO: Averiguar cual es el máximo de este KPI
                                        min=0,
                                        size=100,
                                        ),
                                ], className='gaugeDiv'),
                                dash.html.Div(children=[
                                    dash.html.H6('Peak load of CPU usage of the main processor(%)'),
                                    daq.Gauge(
                                        color={"gradient":True, "ranges":{"green":[0,40], "yellow":[40,80], "red": [80,100]}},
                                        value=thisWeekKPIs['Peak load of CPU usage of the main processor(%)'].iloc[-1],
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
                                    dbc.ListGroupItem('Longest duration of CPU Peak: '+ str(thisWeekKPIs['Duration of peak load of CPU usage of the main processor(s)'].max())+' secs'),
                                    dbc.ListGroupItem('Percentage of longest duration: '+str(thisWeekKPIs['Peak load of CPU usage of the main processor(%)'].iloc[thisWeekKPIs['Duration of peak load of CPU usage of the main processor(s)'].argmax()])+"%")
                                ]),
                            ]),
                            dash.html.Br(),
                            dash.html.Div(children=[
                                dash.html.H5('Peak load of CPU(%)'),
                                dash.dcc.Graph(id='daily_cpu_usage_xGW', figure={}, config={'displayModeBar':False, 'responsive':True, 'scrollZoom': True}),
                            ], className='figureContainer')

                            ], className='infoCardDataContainer')
                    ]),


                    dash.html.Div(id='ip_card_xGW',className='infoCard', children=[
                        dash.html.H3('IP Usage'),
                        dash.html.Div(children=[
                            dash.html.Div(children=[
                                dash.html.Div(children=[
                                    dash.html.H6('IP Pool Usage(%)'),
                                    daq.Gauge(
                                        color={"gradient":True, "ranges":{"green":[0,40], "yellow":[40,80], "red": [80,100]}},
                                        value=thisWeekKPIs['IP Pool Usage(%)'].iloc[-1],
                                        max=100,  # TODO: Averiguar cual es el máximo de este KPI
                                        min=0,
                                        size=100,
                                        ),
                                ], className='gaugeDiv'),
                                ], className='gaugeContainer'),
                            dash.html.Br(),
                            dash.html.H4('Week summary'),
                            dash.html.Div(children=[
                                dash.html.H5('Asigned IP addresses in the PGW'),
                                dbc.ListGroup(children=[
                                    dbc.ListGroupItem('Max Number of assigned IP addresses in the PGW IP pool: '+ str(thisWeekKPIs['Number of assigned IP addresses in the PGW IP pool'].max())),
                                    # dbc.ListGroupItem('Percentage of longest duration: '+str(thisWeekKPIs['Peak load of CPU usage of the main processor(%)'].iloc[thisWeekKPIs['Duration of peak load of CPU usage of the main processor(s)'].argmax()])+"%")
                                ]),
                            ]),
                            dash.html.Br(),
                            dash.html.Div(children=[
                                dash.html.H5('IP Pool Usage%'),
                                dash.dcc.Graph(id='daily_ip_usage_xGW', figure={}, config={'displayModeBar':False, 'responsive':True, 'scrollZoom': True}),
                            ], className='figureContainer')

                            ], className='infoCardDataContainer')
                    ]),

                    ]),
                ])
            ]),
        dash.dcc.Tab(label='Advanced view', value='advancedView', id='advancedTabGraphTab_xGW',children=[
            html.Div(id='advancedTab_xGW', children=[
                html.Div(children=[
                    dash.html.H5('Selected KPIs'),
                    dash.dcc.Dropdown(options=kpiDF_xGW.columns[5:], value=[kpiDF_xGW.columns[7]], multi=True, id='kpiSelector_xGW', placeholder="Select a KPI"),
                    dash.html.Br(),
                    dash.html.H5('Date range selector'),
                    dash.dcc.DatePickerRange(
                        id='dateRange_xGW',
                        min_date_allowed=kpiDF_xGW['Start Time'].min() - datetime.timedelta(days=1),
                        max_date_allowed=kpiDF_xGW['Start Time'].max() + datetime.timedelta(days=1),
                        initial_visible_month=kpiDF_xGW['Start Time'].max(),
                        start_date=kpiDF_xGW['Start Time'].min().date(),
                        end_date=kpiDF_xGW['Start Time'].max().date() + datetime.timedelta(days=1),
                        ),
                    dash.html.Br(),
                    dash.html.Div(className='graphsContainer',children=[
                        dash.dcc.Graph(
                            id='advancedTabGraph_xGW',
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
                            id='dailyGraph_xGW',
                            figure={
                                'data':[{
                                    'type':'line'
                                    }],
                                'layout': {'margin':{'t':50, 'r':0}}
                                })
                        ]),
                    dash.html.Label('Statistical information'),
                    dash.dcc.Checklist(options=['std'], id='metricsCheckList_xGW', value=[]),
                    ]),
                html.Div(id='statsContainer_xGW'),
                ]),
            ]),
        ]),
    ])


# Refrescado del grafico primario
dash.callback(
        dash.Output('advancedTabGraph_xGW', 'figure'),
        dash.Input('dateRange_xGW', 'start_date'),
        dash.Input('dateRange_xGW', 'end_date'),
        dash.Input('kpiSelector_xGW', 'value'),
        dash.Input('metricsCheckList_xGW', 'value')
        )(uv.dateChangeCBGen(kpiDF_xGW))

## Refrescado del grafico secundario
dash.callback(
        dash.Output('dailyGraph_xGW', 'figure'),
        dash.Input('advancedTabGraph_xGW', 'clickData'),
        dash.State('advancedTabGraph_xGW', 'figure'),
        dash.Input('kpiSelector_xGW', 'value'),
        )(uv.clickedDatapointCBGen(kpiDF_xGW, 'advancedTabGraph_xGW.clickData'))

# Callbacks para los graficos de las cartas
## Tarjeta para el uso de CPU
dash.callback(
                dash.Output('daily_cpu_usage_xGW', 'figure'),
                dash.Input('daily_cpu_usage_xGW', 'figure'),
                dash.Input('daily_cpu_usage_xGW', 'clickData'),
                )(uv.basicViewGraphCBGenerator('Peak load of CPU usage of the main processor(%)', 'daily_cpu_usage.clickData', thisWeekKPIs, kpiDF_xGW))

## Tarjeta para el uso de IP
dash.callback(
                dash.Output('daily_ip_usage_xGW', 'figure'),
                dash.Input('daily_ip_usage_xGW', 'figure'),
                dash.Input('daily_ip_usage_xGW', 'clickData'),
                )(uv.basicViewGraphCBGenerator('IP Pool Usage(%)', 'daily_ip_usage.clickData', thisWeekKPIs, kpiDF_xGW))
