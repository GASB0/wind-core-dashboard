import dash
import dash_daq as daq
import sys
import datetime
from dash import html
import pandas as pd

sys.path.insert(1,'./pages')
import utilidadesVarias as uv

widgetList = {
    'successful_rate_of_dedicated_bearer_activation_home': ['Successful rate of dedicated bearer activation', 'MMEMemory'],
    'successful_rate_of_EPS_bearer_modification_home': ['Successful rate of EPS bearer modification', 'MMEMemory'],
    'successful_ratio_of_BOSS_operation_home': ['Successful Ratio of BOSS Operation', 'USPPMemory'],
    'ip_pool_usage_home': ['IP Pool Usage', 'xGWMemory'],
    'number_of_SPR_subscribers': ['Number of SPR Subscribers', 'USPPMemory'],
}

def callbackGen(kpiName):
    def callback(kpiData):
        kpiDF = pd.read_json(kpiData)
        value = kpiDF[kpiName].iloc[-1]
        return value

    return callback
    
for widgetID in widgetList.keys():
    kpiName = widgetList[widgetID][0]
    storage = widgetList[widgetID][1]
    dash.callback(
        dash.Output(widgetID, 'value'),
        dash.Input(storage, 'data'))(callbackGen(kpiName))

thisWeekKPIs_USPP = uv.queryDataFromDB(element='USPP')

dash.register_page(__name__, path='/')

layout = html.Div(children=[
    dash.html.H1('General CORE status'),
    dash.html.H2(f"Latest measurements"),
    dash.html.Div(id='homeContent', children=[
        # MME Part
        dash.html.Div(children=[
            dash.html.H6('Successful rate of dedicated bearer activation(%)'),
            daq.Gauge(
                color={"gradient":True, "ranges":{"red":[0,40], "yellow":[40,80], "green": [80,100]}},
                value=0,
                units='%',
                max=100,  # TODO: Averiguar cual es el máximo de este KPI
                min=0,
                size=100,
                id='successful_rate_of_dedicated_bearer_activation_home',
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
                id='successful_rate_of_EPS_bearer_modification_home',
                ),
        ], className='gaugeDiv'),

        # xGW part
        # Sustituir este gauge por un progressbar
        dash.html.Div(children=[
            dash.html.H6('IP Pool Usage(%)'),
            daq.GraduatedBar(
                value=0,
                max=100,  # TODO: Averiguar cual es el máximo de este KPI
                min=0,
                id='ip_pool_usage_home'
            )
        ], className='gaugeDiv'),

        # Uspp part
        dash.html.Div(children=[
            dash.html.H6('CRM Operation Success'),                        
            daq.Gauge(
                color={"gradient": True, "ranges": { "red": [0, 40], "yellow":[40, 80], "green": [80, 100]}},
                value=0,
                max=100,
                min=0,
                size=150,
                id='successful_ratio_of_BOSS_operation_home',
            ),
        ], className='gaugeDiv'),
        dash.html.Div(children=[
            dash.html.H6('SPR Registered Users'),
            daq.Gauge(
                value=0,
                max=round(thisWeekKPIs_USPP['Number of SPR Subscribers'].max()),
                min=0,
                size=150,
                id='number_of_SPR_subscribers'
            ),
        ], className='gaugeDiv'),
    ]),
    ])