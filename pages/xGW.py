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

dash.register_page(__name__)

layout = html.Div(children=[
    html.H1(children='xGW Page'),
    html.H5(id='latestUpdated_xGW'),
    dash.dcc.Tabs(id="xGW-tabs", value='basicView', children=[
        dash.dcc.Tab(label='Basic view', value='basicView', children=[
            dash.html.Div(id='basicTab_xGW',children=[
                dash.html.Div(className='card_container', children=[
                    dash.html.Div(id='cpu_card_xGW',className='infoCard', children=[
                        dash.html.H3('CPU Usage'),
                        dash.html.H4(f"Latest measurements"),
                        dash.html.Div(children=[
                            dash.html.Div(children=[
                                dash.html.Div(children=[
                                    dash.html.H6('Mean ratio of the CPU usage of the main processor(%)'),
                                    daq.Gauge(
                                        color={"gradient":True, "ranges":{"green":[0,40], "yellow":[40,80], "red": [80,100]}},
                                        # value=thisWeekKPIs_xGW['Mean ratio of the CPU usage of the main processor'].iloc[-1],
                                        value=0,
                                        max=100,  # TODO: Averiguar cual es el máximo de este KPI
                                        min=0,
                                        size=100,
                                        id='mean_ratio_of_the_CPU_usage_of_the_main_processor',
                                        ),
                                ], className='gaugeDiv'),
                                dash.html.Div(children=[
                                    dash.html.H6('Peak load of CPU usage of the main processor(%)'),
                                    daq.Gauge(
                                        color={"gradient":True, "ranges":{"green":[0,40], "yellow":[40,80], "red": [80,100]}},
                                        value=0,
                                        units='%',
                                        max=100,  # TODO: Averiguar cual es el máximo de este KPI
                                        min=0,
                                        size=100,
                                        id='peak_load_of_CPU_usage_of_the_main_processor',
                                        ),
                                ], className='gaugeDiv'),
                                ], className='gaugeContainer'),
                                dash.html.Br(),
                                dash.html.H4('Week summary'),
                            dash.html.Div(children=[
                                dash.html.H5('General CPU load'),
                                dbc.ListGroup(children=[
                                ], id='longestCPUDuration'),
                            ]),
                            dash.html.Br(),
                            # dash.html.Div(children=[
                            #     dash.html.H5('Average load of CPU(%)'),
                            #     dash.dcc.Graph(id='daily_average_cpu_usage_xGW', figure={}, config={'displayModeBar':False, 'responsive':True, 'scrollZoom': True}),
                            # ], className='figureContainer'),

                            dash.html.Div(children=[
                                dash.html.H5('Peak load of CPU(%)'),
                                dash.dcc.Graph(id='daily_peak_cpu_usage_xGW', figure={}, config={'displayModeBar':False, 'responsive':True, 'scrollZoom': True}),
                            ], className='figureContainer')

                            ], className='infoCardDataContainer')
                    ]),

                    dash.html.Div(id='ip_card_xGW',className='infoCard', children=[
                        dash.html.H3('IP Usage'),
                        dash.html.Div(children=[
                            dash.html.H4(f"Latest measurements"),
                            dash.html.Div(children=[
                                dash.html.Div(children=[
                                    dash.html.H6('IP Pool Usage(%)'),
                                    daq.Gauge(
                                        color={"gradient":True, "ranges":{"green":[0,40], "yellow":[40,80], "red": [80,100]}},
                                        value=0,
                                        max=100,  # TODO: Averiguar cual es el máximo de este KPI
                                        min=0,
                                        size=100,
                                        id='IP_Pool_Usage',
                                        ),
                                ], className='gaugeDiv'),
                                ], className='gaugeContainer'),
                            dash.html.Br(),
                            dash.html.H4('Week summary'),
                            dash.html.Div(children=[
                                dash.html.H5('Asigned IP addresses in the PGW'),
                                dbc.ListGroup(children=[
                                ], id='asignedIPinPGW'),
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
                    dash.dcc.Dropdown(id='kpiSelector_xGW', multi=True, placeholder="Select a KPI"),
                    dash.html.Br(),
                    dash.html.H5('Date range selector'),
                    dash.dcc.DatePickerRange(
                        initial_visible_month=datetime.datetime.now(),
                        start_date=datetime.datetime.today() - datetime.timedelta(days=30),
                        end_date=datetime.datetime.now().date() + datetime.timedelta(days=1),
                        id='dateRange_xGW'),
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
    dash.Input('metricsCheckList_xGW', 'value'),
    dash.Input('xGWMemory', 'data'),
    )(uv.dateChangeCBGen())

## Refrescado del grafico secundario
dash.callback(
    dash.Output('dailyGraph_xGW', 'figure'),
    dash.Input('advancedTabGraph_xGW', 'clickData'),
    dash.State('advancedTabGraph_xGW', 'figure'),
    dash.Input('kpiSelector_xGW', 'value'),
    dash.Input('xGWMemory', 'data'),
    )(uv.clickedDatapointCBGen('advancedTabGraph_xGW.clickData'))

# Callbacks para los graficos de las cartas
## Tarjeta para el uso de CPU
dash.callback(
    dash.Output('daily_peak_cpu_usage_xGW', 'figure'),
    dash.Input('daily_peak_cpu_usage_xGW', 'figure'),
    dash.Input('daily_peak_cpu_usage_xGW', 'clickData'),
    dash.Input('xGWMemory', 'data'),
    )(uv.basicViewGraphCBGenerator('Peak load of CPU usage of the main processor', 'daily_cpu_usage.clickData'))

## Tarjeta para el uso de IP
dash.callback(
    dash.Output('daily_ip_usage_xGW', 'figure'),
    dash.Input('daily_ip_usage_xGW', 'figure'),
    dash.Input('daily_ip_usage_xGW', 'clickData'),
    dash.Input('xGWMemory', 'data'),
    )(uv.basicViewGraphCBGenerator('IP Pool Usage', 'daily_ip_usage.clickData'))

# Actualizacion de la data de los graficos
# TODO: Rescribir esta parte del código de forma menos confusa
# Generacion de callbacks para cada uno de los gauges y graficos
widgetDic = {
    'mean_ratio_of_the_CPU_usage_of_the_main_processor':'Mean ratio of the CPU usage of the main processor',
    'peak_load_of_CPU_usage_of_the_main_processor':'Peak load of CPU usage of the main processor',
    'IP_Pool_Usage':'IP Pool Usage',
}
for index, key in enumerate(widgetDic.keys()):
    if index == 0:
        @dash.callback(
            dash.Output(key, 'value'),
            dash.Output('latestUpdated_xGW', 'children'),
            dash.Input('xGWMemory', 'data'),
        )
        def onDataLoad(kpiData):
            kpiDF = pd.read_json(kpiData)
            kpiDF['Start Time']= pd.to_datetime(kpiDF['Start Time']).dt.tz_localize(None)
            return kpiDF[widgetDic[key]].iloc[-1], f"Latest updated {kpiDF['Start Time'].iloc[-1]}"
    else:
        @dash.callback(
            dash.Output(key, 'value'),
            dash.Input('xGWMemory', 'data'),
        )
        def onDataLoad(kpiData):
            kpiDF = pd.read_json(kpiData)
            kpiDF['Start Time']= pd.to_datetime(kpiDF['Start Time']).dt.tz_localize(None)
            return kpiDF[widgetDic[key]].iloc[-1]

# Generacion de los callbacks para las listas
@dash.callback(
    dash.Output('longestCPUDuration', 'children'),
    dash.Input('xGWMemory', 'data'),
)
def listCallBack(kpiData):
    kpiDF = pd.read_json(kpiData)
    kpiDF['Start Time']= pd.to_datetime(kpiDF['Start Time']).dt.tz_localize(None)
    kpiDF['End Time']= pd.to_datetime(kpiDF['End Time']).dt.tz_localize(None)
    thisWeekKPIs = kpiDF[kpiDF['Start Time'] >= (datetime.datetime.now() - datetime.timedelta(days=7))]
    content = dbc.ListGroupItem(children=['Longest duration of CPU Peak: '+ str(thisWeekKPIs['Duration of peak load of CPU usage of the main processor'].max())+' secs'+'@' +str(thisWeekKPIs['Peak load of CPU usage of the main processor'].iloc[thisWeekKPIs['Duration of peak load of CPU usage of the main processor'].argmax()])+"%"])
    return [content]

@dash.callback(
    dash.Output('asignedIPinPGW', 'children'),
    dash.Input('xGWMemory', 'data'),
)
def otherListCallback(kpiData):
    kpiDF = pd.read_json(kpiData)
    kpiDF['Start Time']= pd.to_datetime(kpiDF['Start Time']).dt.tz_localize(None)
    kpiDF['End Time']= pd.to_datetime(kpiDF['End Time']).dt.tz_localize(None)
    thisWeekKPIs = kpiDF[kpiDF['Start Time'] >= (datetime.datetime.now() - datetime.timedelta(days=7))]
    content = [dbc.ListGroupItem('Max Number of assigned IP addresses in the PGW IP pool: '+ str(thisWeekKPIs['Number of assigned IP addresses in the PGW IP pool'].max()))]
    return content


@dash.callback(
    dash.Output('kpiSelector_xGW', 'options'),
    dash.Output('kpiSelector_xGW', 'value'),
    dash.Input('xGWMemory', 'data'),
)
def selectorValueLoader(kpiData):
    kpiDF = pd.read_json(kpiData)
    kpiDF['Start Time']= pd.to_datetime(kpiDF['Start Time']).dt.tz_localize(None)
    kpiDF['End Time']= pd.to_datetime(kpiDF['End Time']).dt.tz_localize(None)

    options=kpiDF.columns[4:-1]
    value=[kpiDF.columns[-3]]

    return options, value