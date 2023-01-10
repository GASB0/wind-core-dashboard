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
kpiDF_RCP = uv.queryDataFromDB(start_date=datetime.datetime(year=2022, month=10, day=1), element='RCP')
thisWeekKPIs_RCP = uv.queryDataFromDB(element='RCP')

dash.register_page(__name__)

layout = html.Div(children=[
    html.H1(children='RCP (PCRF) Page'),
    html.H5(id='latestUpdated_RCP'),
    dash.dcc.Tabs(id="RCP-tabs", value='basicView', children=[
        dash.dcc.Tab(label='Basic view', value='basicView', children=[
            dash.html.Div(id='basicTab_RCP',children=[
                dash.html.Div(className='card_container', children=[
                    dash.html.Div(id='cpu_card_RCP',className='infoCard', children=[
                        dash.html.H3('CPU Usage'),
                        dash.html.H4(f"Latest measurements"),
                        dash.html.Div(children=[
                            dash.html.Div(children=[
                                dash.html.Div(children=[
                                    dash.html.H6('Average CPU Utilization(%)'),
                                    daq.Gauge(
                                        color={"gradient":True, "ranges":{"green":[0,40], "yellow":[40,80], "red": [80,100]}},
                                        value=0,
                                        units='%',
                                        max=100,  # TODO: Averiguar cual es el máximo de este KPI
                                        min=0,
                                        size=100,
                                        id='average_CPU_utilization',
                                        ),
                                ], className='gaugeDiv'),
                                dash.html.Div(children=[
                                    dash.html.H6('Peak CPU Utilization(%)'),
                                    daq.Gauge(
                                        color={"gradient":True, "ranges":{"green":[0,40], "yellow":[40,80], "red": [80,100]}},
                                        value=0,
                                        max=100,  # TODO: Averiguar cual es el máximo de este KPI
                                        min=0,
                                        size=100,
                                        id='peak_CPU_utilization',
                                        ),
                                ], className='gaugeDiv'),
                                ], className='gaugeContainer'),
                            dash.html.Br(),
                            dash.html.H4('Week summary'),
                            dash.html.Div(children=[
                                dash.html.H5('General CPU load'),
                                dbc.ListGroup(children=[
                                ], id='cpuLoadList_RCP'),
                            ]),
                            dash.html.Br(),
                            dash.html.Div(children=[
                                dash.html.H5('Average CPU Utilization(%)'),
                                dash.dcc.Graph(id='daily_average_cpu_usage_RCP', figure={}, config={'displayModeBar':False, 'responsive':True, 'scrollZoom': True}),
                            ], className='figureContainer'),

                            dash.html.Div(children=[
                                dash.html.H5('Peak load of CPU(%)'),
                                dash.dcc.Graph(id='daily_peak_cpu_usage_RCP', figure={}, config={'displayModeBar':False, 'responsive':True, 'scrollZoom': True}),
                            ], className='figureContainer')

                            ], className='infoCardDataContainer')
                    ]),

                    dash.html.Div(id='memory_card_RCP',className='infoCard', children=[
                        dash.html.H3('Memory Usage'),
                        dash.html.H4(f"Latest measurements"),
                        dash.html.Div(children=[
                            dash.html.Div(children=[
                                dash.html.Div(children=[
                                    dash.html.H6('Average Memory Utilization(%)'),
                                    daq.Gauge(
                                        color={"gradient":True, "ranges":{"green":[0,40], "yellow":[40,80], "red": [80,100]}},
                                        value=0,
                                        max=100,  # TODO: Averiguar cual es el máximo de este KPI
                                        min=0,
                                        size=100,
                                        id='average_memory_utilization',
                                        ),
                                ], className='gaugeDiv'),
                                dash.html.Div(children=[
                                    dash.html.H6('Peak Memory Utilization(%)'),
                                    daq.Gauge(
                                        color={"gradient":True, "ranges":{"green":[0,40], "yellow":[40,80], "red": [80,100]}},
                                        value=0,
                                        units='%',
                                        max=100,  # TODO: Averiguar cual es el máximo de este KPI
                                        min=0,
                                        size=100,
                                        id='peak_memory_utilization',
                                        ),
                                ], className='gaugeDiv'),
                                ], className='gaugeContainer'),
                            dash.html.Br(),
                            dash.html.H4('Week summary'),
                            dash.html.Div(children=[
                                dash.html.H5('General memory load'),
                                dbc.ListGroup(children=[
                                ], id='memoryLoadList_RCP'),
                            ]),
                            dash.html.Br(),

                            dash.html.Div(children=[
                                dash.html.H5('Average Memory Utilization(%)'),
                                dash.dcc.Graph(id='daily_average_memory_usage_RCP', figure={}, config={'displayModeBar':False, 'responsive':True, 'scrollZoom': True}),
                            ], className='figureContainer'),

                            dash.html.Div(children=[
                                dash.html.H5('Peak Memory Utilization(%)'),
                                dash.dcc.Graph(id='daily_peak_memory_usage_RCP', figure={}, config={'displayModeBar':False, 'responsive':True, 'scrollZoom': True}),
                            ], className='figureContainer'),

                            ], className='infoCardDataContainer')
                    ]),

                    ]),
                ])
            ]),
        dash.dcc.Tab(label='Advanced view', value='advancedView', id='advancedTabGraphTab_RCP',children=[
            html.Div(id='advancedTab_RCP', children=[
                html.Div(children=[
                    dash.html.H5('Selected KPIs'),
                    dash.dcc.Dropdown(options=kpiDF_RCP.columns[3:-1], value=[kpiDF_RCP.columns[-3]], multi=True, id='kpiSelector_RCP', placeholder="Select a KPI"),
                    dash.html.Br(),
                    dash.html.H5('Date range selector'),
                    dash.dcc.DatePickerRange(
                        id='dateRange_RCP',
                        min_date_allowed=kpiDF_RCP['Start Time'].min() - datetime.timedelta(days=1),
                        max_date_allowed=kpiDF_RCP['Start Time'].max() + datetime.timedelta(days=1),
                        initial_visible_month=kpiDF_RCP['Start Time'].max(),
                        start_date=datetime.datetime.today() - datetime.timedelta(days=30),
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

# Callbacks para los widgets
widgetDic = {
    'average_CPU_utilization':'Average CPU Utilization',
    'peak_CPU_utilization':'Peak CPU Utilization',
    'average_memory_utilization':'Average Memory Utilization',
    'peak_memory_utilization':'Peak Memory Utilization'
}
for index, key in enumerate(widgetDic.keys()):
    if index == 0:
        @dash.callback(
            dash.Output(key, 'value'),
            dash.Output('latestUpdated_RCP', 'children'),
            dash.Input('RCPMemory', 'data'),
        )
        def onDataLoad(kpiData):
            kpiDF = pd.read_json(kpiData)
            kpiDF['Start Time']= pd.to_datetime(kpiDF['Start Time']).dt.tz_localize(None)
            return kpiDF[widgetDic[key]].iloc[-1], f"Latest updated {kpiDF['Start Time'].iloc[-1]}"
    else:
        @dash.callback(
            dash.Output(key, 'value'),
            dash.Input('RCPMemory', 'data'),
        )
        def onDataLoad(kpiData):
            kpiDF = pd.read_json(kpiData)
            kpiDF['Start Time']= pd.to_datetime(kpiDF['Start Time']).dt.tz_localize(None)
            return kpiDF[widgetDic[key]].iloc[-1]


# Generacion de los callbacks para las listas
@dash.callback(
    dash.Output('cpuLoadList_RCP', 'children'),
    dash.Input('RCPMemory', 'data'),
)
def cpuLoadList_RCP_CB(kpiData):
    kpiDF = pd.read_json(kpiData)
    kpiDF['Start Time']= pd.to_datetime(kpiDF['Start Time']).dt.tz_localize(None)
    kpiDF['End Time']= pd.to_datetime(kpiDF['End Time']).dt.tz_localize(None)
    thisWeekKPIs = kpiDF[kpiDF['Start Time'] >= (datetime.datetime.now() - datetime.timedelta(days=7))]
    content = []
    content.append(dbc.ListGroupItem(children=['Average CPU Utilization: ' + str(round(thisWeekKPIs['Average CPU Utilization'].mean(), 2)) + '%']))
    content.append(dbc.ListGroupItem(children=['Mean peak CPU utilization: ' + str(round(thisWeekKPIs['Peak CPU Utilization'].mean(), 2)) + '%']))
    return content

@dash.callback(
    dash.Output('memoryLoadList_RCP', 'children'),
    dash.Input('RCPMemory', 'data'),
)
def memoryLoadList_RCP_CB(kpiData):
    kpiDF = pd.read_json(kpiData)
    kpiDF['Start Time']= pd.to_datetime(kpiDF['Start Time']).dt.tz_localize(None)
    kpiDF['End Time']= pd.to_datetime(kpiDF['End Time']).dt.tz_localize(None)
    thisWeekKPIs = kpiDF[kpiDF['Start Time'] >= (datetime.datetime.now() - datetime.timedelta(days=7))]
    content = []

    content.append(dbc.ListGroupItem('Average Memory Utilization: '+ str(round(thisWeekKPIs['Average Memory Utilization'].mean(), 2))+"%"))
    content.append(dbc.ListGroupItem('Mean peak Memory utilization: '+ str(thisWeekKPIs['Peak Memory Utilization'].mean())+'%'))

    return content

# Callbacks para el advancedView
## Refrescado del grafico primario
dash.callback(
    dash.Output('advancedTabGraph_RCP', 'figure'),
    dash.Input('dateRange_RCP', 'start_date'),
    dash.Input('dateRange_RCP', 'end_date'),
    dash.Input('kpiSelector_RCP', 'value'),
    dash.Input('metricsCheckList_RCP', 'value'),
    dash.Input('RCPMemory', 'data'),
    )(uv.dateChangeCBGen())

## Refrescado del grafico secundario
dash.callback(
    dash.Output('dailyGraph_RCP', 'figure'),
    dash.Input('advancedTabGraph_RCP', 'clickData'),
    dash.State('advancedTabGraph_RCP', 'figure'),
    dash.Input('kpiSelector_RCP', 'value'),
    dash.Input('RCPMemory', 'data'),
    )(uv.clickedDatapointCBGen('advancedTabGraph_RCP.clickData'))

# Callbacks para los graficos de las cartas
## Tarjeta para el uso de CPU
dash.callback(
    dash.Output('daily_average_cpu_usage_RCP', 'figure'),
    dash.Input('daily_average_cpu_usage_RCP', 'figure'),
    dash.Input('daily_average_cpu_usage_RCP', 'clickData'),
    dash.Input('RCPMemory', 'data'),
    )(uv.basicViewGraphCBGenerator('Average CPU Utilization', 'daily_average_cpu_usage.clickData'))

dash.callback(
    dash.Output('daily_peak_cpu_usage_RCP', 'figure'),
    dash.Input('daily_peak_cpu_usage_RCP', 'figure'),
    dash.Input('daily_peak_cpu_usage_RCP', 'clickData'),
    dash.Input('RCPMemory', 'data'),
    )(uv.basicViewGraphCBGenerator('Peak CPU Utilization', 'daily_peak_cpu_usage.clickData'))

## Tarjeta para el uso de memoria
dash.callback(
    dash.Output('daily_average_memory_usage_RCP', 'figure'),
    dash.Input('daily_average_memory_usage_RCP', 'figure'),
    dash.Input('daily_average_memory_usage_RCP', 'clickData'),
    dash.Input('RCPMemory', 'data'),
    )(uv.basicViewGraphCBGenerator('Average Memory Utilization', 'daily_average_memory_usage_RCP.clickData'))

dash.callback(
    dash.Output('daily_peak_memory_usage_RCP', 'figure'),
    dash.Input('daily_peak_memory_usage_RCP', 'figure'),
    dash.Input('daily_peak_memory_usage_RCP', 'clickData'),
    dash.Input('RCPMemory', 'data'),
    )(uv.basicViewGraphCBGenerator('Peak Memory Utilization', 'daily_peak_memory_usage_RCP.clickData'))