import dash
import dash_daq as daq
import sys
import pandas as pd
from dash import html
import dash_bootstrap_components as dbc
import datetime
import plotly

sys.path.insert(1,'./pages')
import utilidadesVarias as uv

dash.register_page(__name__)

layout = html.Div(children=[
    html.H1(children='MME Page'),
    html.H5(id='latestUpdated_MME'),
    dash.dcc.Tabs(id="MME-tabs", value='basicView', children=[
        dash.dcc.Tab(label='Basic view', value='basicView', children=[
            dash.html.Div(id='basicTab_MME',children=[
                dash.dcc.Interval(id='interval-component_MME', interval=1000, n_intervals=0),
                dash.html.Div(id='placeholder', style={'display':'none'}),
                dash.html.Div(className='card_container', children=[
                    dash.html.Div(id='cpu_card_MME',className='infoCard', children=[
                        dash.html.H3('CPU Usage'),
                        dash.html.H4(f"Latest measurements"),
                        dash.html.Div(children=[
                            dash.html.Div(children=[
                                dash.html.Div(children=[
                                    dash.html.H6('Mean ratio of the CPU usage(%)'),
                                    daq.Gauge(
                                        color={"gradient":True, "ranges":{"green":[0,40], "yellow":[40,80], "red": [80,100]}},
                                        # value=thisWeekKPIs_MME['Mean ratio of the CPU usage'].iloc[-1],
                                        value=0,
                                        max=100,  # TODO: Averiguar cual es el máximo de este KPI
                                        min=0,
                                        size=100,
                                        id='mean_ratio_of_the_CPU_usage',
                                        ),
                                ], className='gaugeDiv'),
                                dash.html.Div(children=[
                                    dash.html.H6('Peak load of main processor(%)'),
                                    daq.Gauge(
                                        color={"gradient":True, "ranges":{"green":[0,40], "yellow":[40,80], "red": [80,100]}},
                                        # value=thisWeekKPIs_MME['Peak load of CPU usage of the main processor'].iloc[-1],
                                        value=0,
                                        units='%',
                                        max=100,  # TODO: Averiguar cual es el máximo de este KPI
                                        min=0,
                                        size=100,
                                        id='peak_load_of_CPU_usage_of_the_main_processor_MME'
                                        ),
                                ], className='gaugeDiv'),
                                ], className='gaugeContainer'),
                            dash.html.Br(),
                            dash.html.H4('Week summary'),
                            dash.html.Div(children=[
                                dash.html.H5('Peak load of CPU(%)'),
                                dash.dcc.Graph(id='daily_cpu_usage_MME', figure={}, config={'displayModeBar':False, 'responsive':True, 'scrollZoom': True}),
                            ], className='figureContainer')

                            ], className='infoCardDataContainer')
                    ]),

                    dash.html.Div(id='bearer_card_MME',className='infoCard', children=[
                        dash.html.H3('Bearer Usage'),
                        dash.html.H4(f"Latest measurements"),
                        dash.html.Div(children=[
                            dash.html.Div(children=[
                                dash.html.Div(children=[
                                    dash.html.H6('Successful rate of bearer activation(%)'),
                                    daq.Gauge(
                                        color={"gradient":True, "ranges":{"red":[0,40], "yellow":[40,80], "green": [80,100]}},
                                        value=0,
                                        max=100,  # TODO: Averiguar cual es el máximo de este KPI
                                        min=0,
                                        size=100,
                                        id='successful_rate_of_bearer_activation'
                                        ),
                                ], className='gaugeDiv'),
                                dash.html.Div(children=[
                                    dash.html.H6('Successful rate of dedicated bearer activation(%)'),
                                    daq.Gauge(
                                        color={"gradient":True, "ranges":{"red":[0,40], "yellow":[40,80], "green": [80,100]}},
                                        value=0,
                                        units='%',
                                        max=100,  # TODO: Averiguar cual es el máximo de este KPI
                                        min=0,
                                        size=100,
                                        id='successful_rate_of_dedicated_bearer_activation',
                                        ),
                                ], className='gaugeDiv'),
                                dash.html.Div(children=[
                                    dash.html.H6('Successful rate of EPS bearer modification(%)'),
                                    daq.Gauge(
                                        color={"gradient":True, "ranges":{"red":[0,40], "yellow":[40,80], "green": [80,100]}},
                                        value=0,
                                        units='%',
                                        max=100,  # TODO: Averiguar cual es el máximo de este KPI
                                        min=0,
                                        size=100,
                                        id='successful_rate_of_EPS_bearer_modification'
                                        ),
                                ], className='gaugeDiv'),
                                ], className='gaugeContainer'),

                            dash.html.Br(),
                            dash.html.H4('Week summary'),
                            dash.html.Div(children=[
                                dash.html.H5('Bearer activation/setup time'),
                                dbc.ListGroup(children=[
                                ], id='bearerInfo_MME'),
                            ]),

                            dash.html.Br(),
                            dash.html.Div(children=[
                                dash.html.H5('Successful rate of bearer activation(%)'),
                                dash.dcc.Graph(id='daily_bearer_usage', figure={}, config={'displayModeBar':False, 'responsive':True, 'scrollZoom': True}),
                            ], className='figureContainer'),

                            ], className='infoCardDataContainer')
                    ]),

                    dash.html.Div(id='eps_card_MME',className='infoCard', children=[
                        dash.html.H3('EPS'),
                        dash.html.H4(f"Latest measurements"),
                        dash.html.Div(children=[
                            dash.html.Div(children=[
                                dash.html.Div(children=[
                                    dash.html.H6('Successful rate of EPS Paging(%)'),
                                    daq.Gauge(
                                        color={"gradient":True, "ranges":{"red":[0,40], "yellow":[40,80], "green": [80,100]}},
                                        value=0,
                                        units='%',
                                        max=100,  # TODO: Averiguar cual es el máximo de este KPI
                                        min=0,
                                        size=100,
                                        id='successful_rate_of_EPS_Paging'
                                        ),
                                ], className='gaugeDiv'),
                                dash.html.Div(children=[
                                    dash.html.H6('Successful rate of EPS attach(%)'),
                                    daq.Gauge(
                                        color={"gradient":True, "ranges":{"red":[0,40], "yellow":[40,80], "green": [80,100]}},
                                        value=0,
                                        units='%',
                                        max=100,  # TODO: Averiguar cual es el máximo de este KPI
                                        min=0,
                                        size=100,
                                        id='successful_rate_of_EPS_attach'
                                        ),
                                ], className='gaugeDiv'),
                                ], className='gaugeContainer'),

                            dash.html.Br(),
                            dash.html.H4('Week summary'),
                            dash.html.Div(children=[
                                dash.html.H5('Successful rate of EPS Paging(%)'),
                                dash.dcc.Graph(id='daily_eps_usage_paging', figure={}, config={'displayModeBar':False, 'responsive':True, 'scrollZoom': True}),
                            ], className='figureContainer'),

                            dash.html.Div(children=[
                                dash.html.H5('Successful rate of EPS attach(%)'),
                                dash.dcc.Graph(id='daily_eps_usage', figure={}, config={'displayModeBar':False, 'responsive':True, 'scrollZoom': True}),
                            ], className='figureContainer'),

                            ], className='infoCardDataContainer')
                    ]),

                    ]),
                ])
            ]),
        dash.dcc.Tab(label='Advanced view', value='advancedView', id='advancedTabGraphTab_MME',children=[
            html.Div(id='advancedTab_MME', children=[
                html.Div(children=[
                    dash.html.H5('Selected KPIs'),
                    dash.dcc.Dropdown(multi=True, id='kpiSelector_MME', placeholder="Select a KPI"),
                    dash.html.Br(),
                    dash.html.H5('Date range selector'),
                    dash.dcc.DatePickerRange(
                        id='dateRange_MME',
                        initial_visible_month=datetime.datetime.now(),
                        start_date=datetime.datetime.today() - datetime.timedelta(days=30),
                        end_date=datetime.datetime.now().date() + datetime.timedelta(days=1),
                        ),
                    dash.html.Br(),
                    dash.html.Div(className='graphsContainer',children=[
                        dash.dcc.Graph(
                            id='advancedTabGraph_MME',
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
                            id='dailyGraph_MME',
                            figure={
                                'data':[{
                                    'type':'line'
                                    }],
                                'layout': {'margin':{'t':50, 'r':0}}
                                })
                        ]),
                    dash.html.Label('Statistical information'),
                    dash.dcc.Checklist(options=['std'], id='metricsCheckList_MME', value=[]),
                    ]),
                html.Div(id='statsContainer_MME'),
                ]),
            ]),
        ]),
    ])

# Callbacks para los widgets
widgetDic = {
    'mean_ratio_of_the_CPU_usage':'Mean ratio of the CPU usage',
    'peak_load_of_CPU_usage_of_the_main_processor_MME':'Peak load of CPU usage of the main processor',
    'successful_rate_of_bearer_activation':'Successful rate of bearer activation',
    'successful_rate_of_dedicated_bearer_activation':'Successful rate of dedicated bearer activation',
    'successful_rate_of_EPS_bearer_modification':'Successful rate of EPS bearer modification',
    'successful_rate_of_EPS_Paging':'Successful rate of EPS Paging',
    'successful_rate_of_EPS_attach':'Successful rate of EPS attach',
}

for index, key in enumerate(widgetDic.keys()):
        dash.callback(
            dash.Output(key, 'value'),
            dash.Input('MMEMemory', 'data'),
        )(uv.widgetCBGen(widgetDic, key))

# Generacion de los callbacks para las listas
@dash.callback(
    dash.Output('bearerInfo_MME', 'children'),
    dash.Input('MMEMemory', 'data'),
)
def bearerInfoList_CB(kpiData):
    kpiDF = pd.read_json(kpiData)
    kpiDF['Start Time']= pd.to_datetime(kpiDF['Start Time']).dt.tz_localize(None)
    kpiDF['End Time']= pd.to_datetime(kpiDF['End Time']).dt.tz_localize(None)
    thisWeekKPIs = kpiDF[kpiDF['Start Time'] >= (datetime.datetime.now() - datetime.timedelta(days=7))]
    content = []

    content.append(dbc.ListGroupItem("Mean of bearer activation time(ms): " + str(thisWeekKPIs['Mean of bearer activation time'].max())))
    content.append(dbc.ListGroupItem("Mean of dedicated bearer set-up time(ms): " + str(thisWeekKPIs['Mean of dedicated bearer set-up time'].max())))

    return content

# Callbacks para el advancedView
## Refrescado del grafico primario
dash.callback(
        dash.Output('advancedTabGraph_MME', 'figure'),
        dash.Input('dateRange_MME', 'start_date'),
        dash.Input('dateRange_MME', 'end_date'),
        dash.Input('kpiSelector_MME', 'value'),
        dash.Input('metricsCheckList_MME', 'value'),
        dash.Input('MMEMemory', 'data'),
        )(uv.dateChangeCBGen())

## Refrescado del grafico secundario
dash.callback(
        dash.Output('dailyGraph_MME', 'figure'),
        dash.Input('advancedTabGraph_MME', 'clickData'),
        dash.State('advancedTabGraph_MME', 'figure'),
        dash.Input('kpiSelector_MME', 'value'),
        dash.Input('MMEMemory', 'data'),
        )(uv.clickedDatapointCBGen('advancedTabGraph_MME.clickData'))

# Refrescado del grafico de las tarjetas del basicView
## Tarjeta para el uso de CPU
dash.callback(
                dash.Output('daily_cpu_usage_MME', 'figure'),
                dash.Input('daily_cpu_usage_MME', 'figure'),
                dash.Input('daily_cpu_usage_MME', 'clickData'),
                dash.Input('MMEMemory', 'data'),
                )(uv.basicViewGraphCBGenerator('Peak load of CPU usage of the main processor', 'daily_cpu_usage_MME.clickData'))

## Tarjeta para el uso de memoria
dash.callback(
                dash.Output('daily_bearer_usage', 'figure'),
                dash.Input('daily_bearer_usage', 'figure'),
                dash.Input('daily_bearer_usage', 'clickData'),
                dash.Input('MMEMemory', 'data'),
                )(uv.basicViewGraphCBGenerator('Successful rate of bearer activation', 'daily_bearer_usage.clickData'))

## Tarjeta para el uso de EPS
dash.callback(
                dash.Output('daily_eps_usage', 'figure'),
                dash.Input('daily_eps_usage', 'figure'),
                dash.Input('daily_eps_usage', 'clickData'),
                dash.Input('MMEMemory', 'data'),
                )(uv.basicViewGraphCBGenerator('Successful rate of EPS attach', 'daily_eps_usage.clickData'))
dash.callback(
                dash.Output('daily_eps_usage_paging', 'figure'),
                dash.Input('daily_eps_usage_paging', 'figure'),
                dash.Input('daily_eps_usage_paging', 'clickData'),
                dash.Input('MMEMemory', 'data'),
                )(uv.basicViewGraphCBGenerator('Successful rate of EPS Paging', 'daily_eps_usage_paging.clickData'))

dash.callback(
    dash.Output('kpiSelector_MME', 'options'),
    dash.Output('kpiSelector_MME', 'value'),
    dash.Input('MMEMemory', 'data'),
)(uv.selectorValueLoader)