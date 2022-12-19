import dash
import dash_daq as daq
import dash_bootstrap_components as dbc
import os
import datetime
from dash import html
import pandas as pd
import plotly

# Generador de callbacks para click sobre tarjetas
def basicViewGraphCBGenerator(kpiName, eventName):
    def callback(_,__):
        triggeringCB = dash.callback_context.triggered_prop_ids
        print(dash.callback_context.triggered_id)

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
def queryDataFromDB(start_date=datetime.datetime.today() - datetime.timedelta(days=20), end_date=datetime.datetime.today()) -> pd.DataFrame:
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

cpu_kpi_list = dbc.ListGroup(children=[
    dbc.ListGroupItem(dash.html.Div(children=[
        'Mean ratio of the CPU usage of the main processor(%): ', thisWeekKPIs['Mean ratio of the CPU usage of the main processor(%)'].mean()
    ])) ,
    dbc.ListGroupItem(dash.html.Div(children=[
        'Duration of peak load of CPU usage of the main processor(s): ', round(thisWeekKPIs['Duration of peak load of CPU usage of the main processor(s)'].mean(), 3) 
    ]))
])

ip_kpi_list = dbc.ListGroup(children=[
    dbc.ListGroupItem(dash.html.Div(children=[
        'Number of assigned IP addresses in the PGW IP pool: ', round(thisWeekKPIs['Number of assigned IP addresses in the PGW IP pool'].mean(), 3) 
    ])),
    dbc.ListGroupItem(dash.html.Div(children=[
        'Total number of IP addresses in the PGW IP pool: ', round(thisWeekKPIs['Total number of IP addresses in the PGW IP pool'].mean(), 3) 
    ])),
])

dash.register_page(__name__)

layout = html.Div(children=[
    html.H1(children='xGW Page'),
    dash.dcc.Tabs(id="xGW-tabs", value='basicView', children=[
        dash.dcc.Tab(label='Basic view', value='basicView', children=[
            dash.html.Div(id='basicTab',children=[
                dash.html.Div(className='card_container', children=[
                    dash.html.Div(id='cpu_card',className='infoCard', children=[
                        dash.html.H3('CPU Usage'),
                        dash.html.H4('This week\'s summary (average)'),
                        dash.dcc.Graph(id='daily_cpu_usage', figure={'layout': {'height': 270, 'width':270, 'margin':{'t':50, 'r':10}, 'title': 'Mean daily CPU usage'}}, config={'displayModeBar':False, 'responsive':True, 'scrollZoom': True}), 
                        daq.Gauge(
                            color={"gradient":True, "ranges":{"green":[0,40], "yellow":[40,80], "red": [80,100]}},
                            value=kpiDF['Peak load of CPU usage of the main processor(%)'].mean(),
                            showCurrentValue=True,
                            units="%",
                            label='Peak load of CPU usage of the main processor',
                            max=100,
                            min=0,
                            size=200,
                        ),
                        cpu_kpi_list,
                    ]),

                    dash.html.Div(id='ip_pool_usage', className='infoCard', children=[
                        dash.html.H3('IP Usage'),
                        dash.html.H4('This week\'s summary (average)'),
                        dash.dcc.Graph(id='daily_ip_usage', figure={'layout': {'height': 270, 'width':270, 'margin':{'t':50, 'r':10}, 'title': 'Peak load of CPU usage of the main processor(%)'}}, config={'displayModeBar':False, 'responsive':True, 'scrollZoom': True}),
                        daq.Gauge(
                            color={"gradient":True, "ranges":{"green":[0,40], "yellow":[40,80], "red": [80,100]}},
                            value=kpiDF['IP Pool Usage(%)'].mean(),
                            showCurrentValue=True,
                            units="%",
                            label='IP Pool Usage(%)',
                            max=100,
                            min=0,
                            size=200,
                        ),
                        ip_kpi_list,
                        ]),
                    ])
                ])
            ]),
        dash.dcc.Tab(label='Advanced view', value='advancedView', id='advancedTabGraphTab',children=[
            html.Div(id='advancedTab', children=[
                html.Div(children=[
                    dash.dcc.DatePickerRange(
                        id='dateRange',
                        min_date_allowed=kpiDF['Start Time'].min() - datetime.timedelta(days=1),
                        max_date_allowed=kpiDF['Start Time'].max() + datetime.timedelta(days=1),
                        initial_visible_month=kpiDF['Start Time'].max(),
                        start_date=kpiDF['Start Time'].min().date(),
                        end_date=kpiDF['Start Time'].max().date() + datetime.timedelta(days=1),
                        ),
                    dash.html.Div(className='graphsContainer',children=[
                        dash.dcc.Graph(
                            id='advancedTabGraph',
                            figure={
                                'data':[{
                                    'type':'line'
                                    }],
                                'layout': {'margin':{'t':50, 'r':0}}
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
                    dash.html.Br(),
                    dash.html.Label('KPIs to be selected'),
                    dash.dcc.Dropdown(options=kpiDF.columns[5:], value=[kpiDF.columns[7]], multi=True, id='kpiSelector', placeholder="Select a KPI"),
                    ]),
                html.Div(id='statsContainer'),
                ]),
            ]),
        ]),
    ])
