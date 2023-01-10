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

kpiDF_USPP = uv.queryDataFromDB(start_date=datetime.datetime(year=2022, month=10, day=1), element='USPP')
thisWeekKPIs_USPP = uv.queryDataFromDB(element='USPP')

dash.register_page(__name__)

layout = html.Div(children=[
    html.H1(children='USPP (HSS/SPR)'),
    html.H5(id='latestUpdated_USPP'),
    dash.dcc.Tabs(id="USPP-tabs", value='basicView', children=[
        dash.dcc.Tab(label='Basic view', value='basicView', children=[            
            dash.html.Div(id='basicTab',children=[
                dash.html.Div(className='card_container', children=[
                    
                    dash.html.Div(id='crm_operation_card',className='infoCard', children=[                        
                        dash.html.H3('CRM Operation'),
                        dash.html.H4(f"Latest measurements ({thisWeekKPIs_USPP['Start Time'].iloc[-1]})"),

                        dash.html.Div(children=[
                            dash.html.H6('CRM Operation Success'),                        
                            daq.Gauge(
                                color={"gradient": True, "ranges": {"red": [0, 40], "yellow":[40, 80], "green": [80, 100]}},
                                value=0,
                                max=100,
                                min=0,
                                size=150,
                                id='successful_ratio_of_BOSS_operation',
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
                        dash.html.H4(f"Latest measurements ({thisWeekKPIs_USPP['Start Time'].iloc[-1]})"),

                        dash.html.Div(children=[
                            dash.html.H6('SPR Registered Users'),
                            daq.Gauge(
                                value=0,
                                max=round(kpiDF_USPP['Number of SPR Subscribers'].max()),
                                min=0,
                                size=150,
                                id='number_of_SPR_registered_user',
                            ),
                        ], className='gaugeDiv'),

                        dash.html.H4('Week summary'),

                        dash.html.H5('Number of subscribers info'),
                        dash.html.Br(),

                        dbc.ListGroup(children=[
                        ], id='sprSubsKPIList'),

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
                        dash.dcc.Dropdown(options=kpiDF_USPP.columns[4:-1], value=[kpiDF_USPP.columns[-3]], multi=True, id='kpiSelector', placeholder="Select a KPI"),
                        dash.html.Br(),
                        dash.dcc.DatePickerRange(
                            id='dateRange',
                            min_date_allowed=kpiDF_USPP['Start Time'].min() - datetime.timedelta(days=1),
                            max_date_allowed=kpiDF_USPP['Start Time'].max() + datetime.timedelta(days=1),
                            initial_visible_month=kpiDF_USPP['Start Time'].max(),
                            start_date=datetime.datetime.today() - datetime.timedelta(days=30),
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

# Callbacks para los widgets
widgetDic = {
    'successful_ratio_of_BOSS_operation':'Successful Ratio of BOSS Operation',
    'number_of_SPR_registered_user':'Number of SPR Registered User',
}
for index, key in enumerate(widgetDic.keys()):
    if index == 0:
        @dash.callback(
            dash.Output(key, 'value'),
            dash.Output('latestUpdated_USPP', 'children'),
            dash.Input('USPPMemory', 'data'),
        )
        def onDataLoad(kpiData):
            kpiDF = pd.read_json(kpiData)
            kpiDF['Start Time']= pd.to_datetime(kpiDF['Start Time']).dt.tz_localize(None)
            return kpiDF[widgetDic[key]].iloc[-1], f"Latest updated {kpiDF['Start Time'].iloc[-1]}"
    else:
        @dash.callback(
            dash.Output(key, 'value'),
            dash.Input('USPPMemory', 'data'),
        )
        def onDataLoad(kpiData):
            kpiDF = pd.read_json(kpiData)
            kpiDF['Start Time']= pd.to_datetime(kpiDF['Start Time']).dt.tz_localize(None)
            return kpiDF[widgetDic[key]].iloc[-1]


# Generacion de los callbacks para las listas
@dash.callback(
    dash.Output('sprSubsKPIList', 'children'),
    dash.Input('USPPMemory', 'data'),
)
def bearerInfoList_CB(kpiData):
    kpiDF = pd.read_json(kpiData)
    kpiDF['Start Time']= pd.to_datetime(kpiDF['Start Time']).dt.tz_localize(None)
    kpiDF['End Time']= pd.to_datetime(kpiDF['End Time']).dt.tz_localize(None)
    thisWeekKPIs = kpiDF[kpiDF['Start Time'] >= (datetime.datetime.now() - datetime.timedelta(days=7))]
    content = []
    content.append(dbc.ListGroupItem('Number of Total SPR Subscribers: '+str(round(thisWeekKPIs['Number of SPR Subscribers'].iloc[-1]))))

    return content

# Refrescado del grafico primario
dash.callback(
    dash.Output('advancedTabGraph_USPP', 'figure'),
    dash.Input('dateRange', 'start_date'),
    dash.Input('dateRange', 'end_date'),
    dash.Input('kpiSelector', 'value'),
    dash.Input('metricsCheckList', 'value'),
    dash.Input('USPPMemory', 'data'),
)(uv.dateChangeCBGen())

# Refrescado del grafico secundario
dash.callback(
    dash.Output('dailyGraph_USPP', 'figure'),
    dash.Input('advancedTabGraph_USPP', 'clickData'),
    dash.State('advancedTabGraph_USPP', 'figure'),
    dash.Input('kpiSelector', 'value'),
    dash.Input('USPPMemory', 'data'),
)(uv.clickedDatapointCBGen('advancedTabGraph_USPP.clickData'))

# Callbacks para los graficos de las cartas
dash.callback(
    dash.Output('weekly_crm_operation', 'figure'),
    dash.Input('weekly_crm_operation', 'figure'),
    dash.Input('weekly_crm_operation', 'clickData'),
    dash.Input('USPPMemory', 'data'),
)(uv.basicViewGraphCBGenerator('Successful Ratio of BOSS Operation', 'weekly_crm_operation.clickData'))

dash.callback(
    dash.Output('weekly_spr_users', 'figure'),
    dash.Input('weekly_spr_users', 'figure'),
    dash.Input('weekly_spr_users', 'clickData'),
    dash.Input('USPPMemory', 'data'),
)(uv.basicViewGraphCBGenerator('Number of SPR Registered User', 'weekly_spr_users.clickData'))

dash.callback(
    dash.Output('spr_subs', 'figure'),
    dash.Input('spr_subs', 'figure'),
    dash.Input('spr_subs', 'clickData'),
    dash.Input('USPPMemory', 'data'),
)(uv.basicViewGraphCBGenerator('Number of SPR Subscribers', 'spr_subs.clickData'))