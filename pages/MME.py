import dash
import dash_daq as daq
import sys
import pandas as pd
from dash import html
import dash_bootstrap_components as dbc
import datetime
import plotly

sys.path.insert(1,'/home/gabriel/Documents/Projects/wind_dashboard/pages')
import utilidadesVarias as uv

kpiDF_MME = uv.queryDataFromDB(element='MME')
thisWeekKPIs_MME = kpiDF_MME.copy(deep=True)

print(kpiDF_MME.columns)

dash.register_page(__name__)

layout = html.Div(children=[
    html.H1(children='MME Page'),
    dash.dcc.Tabs(id="MME-tabs", value='basicView', children=[
        dash.dcc.Tab(label='Basic view', value='basicView', children=[
            dash.html.Div(id='basicTab_MME',children=[
                dash.html.Div(className='card_container', children=[
                    dash.html.Div(id='cpu_card_MME',className='infoCard', children=[
                        dash.html.H3('CPU Usage'),
                        dash.html.H4('Latest measurements'),
                        dash.html.Div(children=[
                            dash.html.Div(children=[
                                dash.html.Div(children=[
                                    dash.html.H6('Mean ratio of the CPU usage(%)'),
                                    daq.Gauge(
                                        color={"gradient":True, "ranges":{"green":[0,4], "yellow":[4,8], "red": [8,10]}},
                                        value=thisWeekKPIs_MME['Mean ratio of the CPU usage(%)'].iloc[-1],
                                        max=10,  # TODO: Averiguar cual es el máximo de este KPI
                                        min=0,
                                        size=100,
                                        ),
                                ], className='gaugeDiv'),
                                dash.html.Div(children=[
                                    dash.html.H6('Peak load of main processor(%)'),
                                    daq.Gauge(
                                        color={"gradient":True, "ranges":{"green":[0,40], "yellow":[40,80], "red": [80,100]}},
                                        value=thisWeekKPIs_MME['Peak load of CPU usage of the main processor(%)'].iloc[-1],
                                        units='%',
                                        max=100,  # TODO: Averiguar cual es el máximo de este KPI
                                        min=0,
                                        size=100,
                                        ),
                                ], className='gaugeDiv'),
                                ], className='gaugeContainer'),
                            dash.html.Br(),
                            dash.html.Div(children=[
                                dash.html.H5('Peak load of CPU(%) (week summary)'),
                                dash.dcc.Graph(id='daily_cpu_usage_MME', figure={}, config={'displayModeBar':False, 'responsive':True, 'scrollZoom': True}),
                            ], className='figureContainer')

                            ], className='infoCardDataContainer')
                    ]),

                    dash.html.Div(id='bearer_card_MME',className='infoCard', children=[
                        dash.html.H3('Bearer Usage'),
                        dash.html.H4('Latest measurements'),
                        dash.html.Div(children=[
                            dash.html.Div(children=[
                                dash.html.Div(children=[
                                    dash.html.H6('Successful rate of bearer activation(%)'),
                                    daq.Gauge(
                                        color={"gradient":True, "ranges":{"green":[0,40], "yellow":[40,80], "red": [80,100]}},
                                        value=thisWeekKPIs_MME['Successful rate of bearer activation(%)'].iloc[-1],
                                        max=100,  # TODO: Averiguar cual es el máximo de este KPI
                                        min=0,
                                        size=100,
                                        ),
                                ], className='gaugeDiv'),
                                dash.html.Div(children=[
                                    dash.html.H6('Successful rate of dedicated bearer activation(%)'),
                                    daq.Gauge(
                                        color={"gradient":True, "ranges":{"green":[0,40], "yellow":[40,80], "red": [80,100]}},
                                        value=thisWeekKPIs_MME['Successful rate of dedicated bearer activation(%)'].iloc[-1],
                                        units='%',
                                        max=100,  # TODO: Averiguar cual es el máximo de este KPI
                                        min=0,
                                        size=100,
                                        ),
                                ], className='gaugeDiv'),
                                dash.html.Div(children=[
                                    dash.html.H6('Successful rate of EPS bearer modification(%)'),
                                    daq.Gauge(
                                        color={"gradient":True, "ranges":{"green":[0,40], "yellow":[40,80], "red": [80,100]}},
                                        value=thisWeekKPIs_MME['Successful rate of EPS bearer modification(%)'].iloc[-1],
                                        units='%',
                                        max=100,  # TODO: Averiguar cual es el máximo de este KPI
                                        min=0,
                                        size=100,
                                        ),
                                ], className='gaugeDiv'),
                                ], className='gaugeContainer'),

                            dash.html.Div(children=[
                                dash.html.H5('Bearer activation/setup time'),
                                dbc.ListGroup(children=[
                                    dbc.ListGroupItem("Mean of bearer activation time(ms): "+str(thisWeekKPIs_MME['Mean of bearer activation time(ms)'].max())),
                                    dbc.ListGroupItem("Mean of dedicated bearer set-up time(ms): "+str(thisWeekKPIs_MME['Mean of dedicated bearer set-up time(ms)'].max())),
                                ]),
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
                        dash.html.H4('Latest measurements'),
                        dash.html.Div(children=[
                            dash.html.Div(children=[
                                dash.html.Div(children=[
                                    dash.html.H6('Successful rate of EPS bearer modification(%)'),
                                    daq.Gauge(
                                        color={"gradient":True, "ranges":{"green":[0,40], "yellow":[40,80], "red": [80,100]}},
                                        value=thisWeekKPIs_MME['Successful rate of EPS bearer modification(%)'].iloc[-1],
                                        max=100,  # TODO: Averiguar cual es el máximo de este KPI
                                        min=0,
                                        size=100,
                                        ),
                                ], className='gaugeDiv'),
                                dash.html.Div(children=[
                                    dash.html.H6('Successful rate of EPS Paging(%)'),
                                    daq.Gauge(
                                        color={"gradient":True, "ranges":{"green":[0,40], "yellow":[40,80], "red": [80,100]}},
                                        value=thisWeekKPIs_MME['Successful rate of EPS Paging(%)'].iloc[-1],
                                        units='%',
                                        max=100,  # TODO: Averiguar cual es el máximo de este KPI
                                        min=0,
                                        size=100,
                                        ),
                                ], className='gaugeDiv'),
                                dash.html.Div(children=[
                                    dash.html.H6('Successful rate of EPS attach(%)'),
                                    daq.Gauge(
                                        color={"gradient":True, "ranges":{"green":[0,40], "yellow":[40,80], "red": [80,100]}},
                                        value=thisWeekKPIs_MME['Successful rate of EPS attach(%)'].iloc[-1],
                                        units='%',
                                        max=100,  # TODO: Averiguar cual es el máximo de este KPI
                                        min=0,
                                        size=100,
                                        ),
                                ], className='gaugeDiv'),
                                ], className='gaugeContainer'),

                            dash.html.Br(),
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
                    dash.dcc.Dropdown(options=kpiDF_MME.columns[5:], value=[kpiDF_MME.columns[7]], multi=True, id='kpiSelector_MME', placeholder="Select a KPI"),
                    dash.html.Br(),
                    dash.html.H5('Date range selector'),
                    dash.dcc.DatePickerRange(
                        id='dateRange_MME',
                        min_date_allowed=kpiDF_MME['Start Time'].min() - datetime.timedelta(days=1),
                        max_date_allowed=kpiDF_MME['Start Time'].max() + datetime.timedelta(days=1),
                        initial_visible_month=kpiDF_MME['Start Time'].max(),
                        start_date=kpiDF_MME['Start Time'].min().date(),
                        end_date=kpiDF_MME['Start Time'].max().date() + datetime.timedelta(days=1),
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


# Refrescado del grafico primario
@dash.callback(
        dash.Output('advancedTabGraph_MME', 'figure'),
        dash.Input('dateRange_MME', 'start_date'),
        dash.Input('dateRange_MME', 'end_date'),
        dash.Input('kpiSelector_MME', 'value'),
        dash.Input('metricsCheckList_MME', 'value')
        )
def dateChange_cb(start_date: datetime.datetime, end_date: datetime.datetime, selector: list, checklistOptions: list):
    kpiDF = uv.queryDataFromDB(start_date, end_date, element='MME')
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
        dash.Output('dailyGraph_MME', 'figure'),
        dash.Input('advancedTabGraph_MME', 'clickData'),
        dash.State('advancedTabGraph_MME', 'figure'),
        dash.Input('kpiSelector_MME', 'value'),
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
        if list(triggeringCB.keys())[0] == 'advancedTabGraph_MME.clickData':
            dateToInspect = pd.to_datetime(clickData['points'][0]['x']).date()
        else:
            dateToInspect = pd.to_datetime(aggFigure['data'][0]['x'][-1]).date()
    except:
        return fig

    if selector:
        filteredDF = kpiDF_MME[ kpiDF_MME['Start Time'].apply(lambda x: pd.to_datetime(x).date()) == dateToInspect]
        for _, value in enumerate(selector):
            fig.add_trace(plotly.graph_objs.Scatter(
                x=filteredDF['Start Time'],
                y=filteredDF[value],
                ))

    return fig

dash.callback(
                dash.Output('daily_cpu_usage_MME', 'figure'),
                dash.Input('daily_cpu_usage_MME', 'figure'),
                dash.Input('daily_cpu_usage_MME', 'clickData'),
                )(uv.basicViewGraphCBGenerator('Peak load of CPU usage of the main processor(%)', 'daily_cpu_usage_MME.clickData', thisWeekKPIs_MME, kpiDF_MME))


dash.callback(
                dash.Output('daily_bearer_usage', 'figure'),
                dash.Input('daily_bearer_usage', 'figure'),
                dash.Input('daily_bearer_usage', 'clickData'),
                )(uv.basicViewGraphCBGenerator('Successful rate of bearer activation(%)', 'daily_bearer_usage.clickData', thisWeekKPIs_MME, kpiDF_MME))


dash.callback(
                dash.Output('daily_eps_usage', 'figure'),
                dash.Input('daily_eps_usage', 'figure'),
                dash.Input('daily_eps_usage', 'clickData'),
                )(uv.basicViewGraphCBGenerator('Successful rate of EPS attach(%)', 'daily_eps_usage.clickData', thisWeekKPIs_MME, kpiDF_MME))
