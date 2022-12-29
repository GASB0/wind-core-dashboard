import dash
import dash_daq as daq
import dash_bootstrap_components as dbc
import os
import datetime
from dash import html
import pandas as pd
import plotly
import sys

sys.path.insert(1,'./pages')
import utilidadesVarias as uv

kpiDF_USPP = uv.queryDataFromDB(element='USPP')
thisWeekKPIs_USPP = kpiDF_USPP.copy(deep=True)

spr_subs_kpi_list = dbc.ListGroup(children=[
    dbc.ListGroupItem(dash.html.Div(children=[
        'Number of Total SPR Subscribers: ', round(thisWeekKPIs_USPP['Number of SPR Subscribers'].mean()) 
    ])),
    # dbc.ListGroupItem(dash.html.Div(children=[
    #     'Total number of IP addresses in the PGW IP pool: ', round(thisWeekKPIs_USPP['Total number of IP addresses in the PGW IP pool'].mean(), 3) 
    # ])),
])

dash.register_page(__name__)

layout = html.Div(children=[
    html.H1(children='USPP (HSS/SPR)'),
    dash.dcc.Tabs(id="USPP-tabs", value='basicView', children=[
        dash.dcc.Tab(label='Basic view', value='basicView', children=[            
            dash.html.Div(id='basicTab',children=[
                dash.html.Div(className='card_container', children=[
                    
                    dash.html.Div(id='crm_operation_card',className='infoCard', children=[                        
                        dash.html.H3('CRM Operation'),
                        dash.html.H4('Latest measurements'),                        

                        dash.html.Div(children=[
                            dash.html.H6('CRM Operation Success (%)'),                        
                            daq.Gauge(
                                color={"gradient": True, "ranges": {
                                    "red": [0, 40], "yellow":[40, 80], "green": [80, 100]}},
                                value=int(
                                    kpiDF_USPP['Successful Ratio of BOSS Operation(%)'].mean()),
                                max=100,
                                min=0,
                                size=150,
                            ),
                        ], className='gaugeDiv'),
                        dash.html.H4('Week summary'),
                        dash.html.Div(children=[
                            dash.html.H5('Successful Ratio of BOSS Operation(%)'),
                            dash.dcc.Graph(id='weekly_crm_operation', figure={'layout': {'height': 270, 'width': 270, 'margin': { 't': 50, 'r': 10}, 'title': 'CRM Operation Success (%)'}}, config={'displayModeBar': False, 'responsive': True, 'scrollZoom': True}), ],
                        className='figureContainer'),
                    ]),

                    dash.html.Div(id='spr_subs', className='infoCard', children=[
                        dash.html.H3('SPR Registered Users'),
                        dash.html.H4('Latest measurements'),

                        dash.html.Div(children=[
                            dash.html.H6('SPR Registered Users'),
                            daq.Gauge(
                                value=int(
                                    kpiDF_USPP['Number of SPR Registered User'].iloc[-1]),
                                max=round(
                                    kpiDF_USPP['Number of SPR Subscribers'].mean()),
                                min=0,
                                size=150,
                            ),
                        ], className='gaugeDiv'),

                        dash.html.H4('Week summary'),

                        dash.html.H5('Number of subscribers info'),
                        dash.html.Br(),
                        spr_subs_kpi_list,
                        dash.html.Br(),
                        dash.html.Br(),

                        dash.html.Div(children=[
                            dash.html.H5('Number of SPR Registered User'),
                            dash.dcc.Graph(id='weekly_spr_users', figure={'layout': {'height': 270, 'width': 270, 'margin': { 't': 50, 'r': 10}, 'title': 'CRM Operation Success (%)'}}, config={'displayModeBar': False, 'responsive': True, 'scrollZoom': True}),
                        ], className='figureContainer'),

                        dash.html.Div(children=[
                            dash.html.H5('Number of SPR Subscribers'),
                            dash.dcc.Graph(id='spr_subs', figure={'layout': {'height': 270, 'width': 270, 'margin': { 't': 50, 'r': 10}, 'title': 'CRM Operation Success (%)'}}, config={'displayModeBar': False, 'responsive': True, 'scrollZoom': True}),
                        ], className='figureContainer'),
                    ]),
                    ])
                ])
            ]),
        
            dash.dcc.Tab(label='Advanced view', value='advancedView', id='advancedTabGraphTab',children=[
                html.Div(id='advancedTab', children=[
                    html.Div(children=[
                        dash.html.Label('KPIs to be selected'),
                        dash.dcc.Dropdown(options=kpiDF_USPP.columns[5:], value=[kpiDF_USPP.columns[7]], multi=True, id='kpiSelector', placeholder="Select a KPI"),
                        dash.html.Br(),
                        dash.dcc.DatePickerRange(
                            id='dateRange',
                            min_date_allowed=kpiDF_USPP['Start Time'].min() - datetime.timedelta(days=1),
                            max_date_allowed=kpiDF_USPP['Start Time'].max() + datetime.timedelta(days=1),
                            initial_visible_month=kpiDF_USPP['Start Time'].max(),
                            start_date=kpiDF_USPP['Start Time'].min().date(),
                            end_date=kpiDF_USPP['Start Time'].max().date() + datetime.timedelta(days=1),
                            ),
                        dash.html.Div(className='graphsContainer',children=[
                            dash.dcc.Graph(
                                id='advancedTabGraph_USPP',
                                figure={
                                    'data':[{
                                        'type':'line'
                                        }],
                                    'layout': {'margin':{'t':50, 'r':0}}
                                    }
                                ),
                            dash.dcc.Graph(
                                id='dailyGraph_USPP',
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
dash.callback(
        dash.Output('advancedTabGraph_USPP', 'figure'),
        dash.Input('dateRange', 'start_date'),
        dash.Input('dateRange', 'end_date'),
        dash.Input('kpiSelector', 'value'),
        dash.Input('metricsCheckList', 'value')
        )(uv.dateChangeCBGen(kpiDF_USPP))

# Refrescado del grafico secundario
dash.callback(
        dash.Output('dailyGraph_USPP', 'figure'),
        dash.Input('advancedTabGraph_USPP', 'clickData'),
        dash.State('advancedTabGraph_USPP', 'figure'),
        dash.Input('kpiSelector', 'value'),
        )(uv.clickedDatapointCBGen(kpiDF_USPP, 'advancedTabGraph_USPP.clickData'))

# Callbacks para los graficos de las cartas
dash.callback(
                dash.Output('weekly_crm_operation', 'figure'),
                dash.Input('weekly_crm_operation', 'figure'),
                dash.Input('weekly_crm_operation', 'clickData'),
                )(uv.basicViewGraphCBGenerator('Successful Ratio of BOSS Operation(%)', 'weekly_crm_operation.clickData', thisWeekKPIs_USPP, kpiDF_USPP))

dash.callback(
                dash.Output('weekly_spr_users', 'figure'),
                dash.Input('weekly_spr_users', 'figure'),
                dash.Input('weekly_spr_users', 'clickData'),
                )(uv.basicViewGraphCBGenerator('Number of SPR Registered User', 'weekly_spr_users.clickData', thisWeekKPIs_USPP, kpiDF_USPP))

dash.callback(
                dash.Output('spr_subs', 'figure'),
                dash.Input('spr_subs', 'figure'),
                dash.Input('spr_subs', 'clickData'),
                )(uv.basicViewGraphCBGenerator('Number of SPR Subscribers', 'spr_subs.clickData', thisWeekKPIs_USPP, kpiDF_USPP))