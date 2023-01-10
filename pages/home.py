import dash
import dash_daq as daq
import sys
import datetime
from dash import html
import pandas as pd

sys.path.insert(1,'./pages')
import utilidadesVarias as uv

# kpiDF_MME = uv.queryDataFromDB(start_date=datetime.datetime(year=2022, month=10, day=1), element='MME')
thisWeekKPIs_MME = uv.queryDataFromDB(element='MME')

# kpiDF_xGW = uv.queryDataFromDB(start_date=datetime.datetime(year=2022, month=10, day=1), element='xGW')
thisWeekKPIs_xGW = uv.queryDataFromDB(element='xGW')

# kpiDF_RCP = uv.queryDataFromDB(start_date=datetime.datetime(year=2022, month=10, day=1), element='RCP')
thisWeekKPIs_RCP = uv.queryDataFromDB(element='RCP')

# kpiDF_USPP = uv.queryDataFromDB(start_date=datetime.datetime(year=2022, month=10, day=1), element='USPP')
thisWeekKPIs_USPP = uv.queryDataFromDB(element='USPP')

dash.register_page(__name__, path='/')

layout = html.Div(children=[
    dash.html.H1('General CORE status'),
    dash.html.H2(f"Latest measurements ({thisWeekKPIs_USPP['Start Time'].iloc[-1]})"),
    dash.html.Div(id='homeContent', children=[
        # MME Part
        dash.html.Div(children=[
            dash.html.H6('Successful rate of dedicated bearer activation(%)'),
            daq.Gauge(
                color={"gradient":True, "ranges":{"red":[0,40], "yellow":[40,80], "green": [80,100]}},
                value=thisWeekKPIs_MME['Successful rate of dedicated bearer activation'].iloc[-1],
                units='%',
                max=100,  # TODO: Averiguar cual es el máximo de este KPI
                min=0,
                size=100,
                ),
        ], className='gaugeDiv'),
        dash.html.Div(children=[
            dash.html.H6('Successful rate of EPS bearer modification(%)'),
            daq.Gauge(
                color={"gradient":True, "ranges":{"red":[0,40], "yellow":[40,80], "green": [80,100]}},
                value=thisWeekKPIs_MME['Successful rate of EPS bearer modification'].iloc[-1],
                units='%',
                max=100,  # TODO: Averiguar cual es el máximo de este KPI
                min=0,
                size=100,
                ),
        ], className='gaugeDiv'),
        dash.html.Div(children=[
            dash.html.H6('Successful rate of EPS bearer modification(%)'),
            daq.Gauge(
                color={"gradient":True, "ranges":{"red":[0,40], "yellow":[40,80], "green": [80,100]}},
                value=thisWeekKPIs_MME['Successful rate of EPS bearer modification'].iloc[-1],
                units='%',
                max=100,  # TODO: Averiguar cual es el máximo de este KPI
                min=0,
                size=100,
                ),
        ], className='gaugeDiv'),

        # xGW part
        # Sustituir este gauge por un progressbar
        dash.html.Div(children=[
            dash.html.H6('IP Pool Usage(%)'),
            daq.GraduatedBar(
                value=thisWeekKPIs_xGW['IP Pool Usage'].iloc[-1],
                max=100,  # TODO: Averiguar cual es el máximo de este KPI
                min=0,
            )
        ], className='gaugeDiv'),

        # Uspp part
        dash.html.Div(children=[
            dash.html.H6('CRM Operation Success'),                        
            daq.Gauge(
                color={"gradient": True, "ranges": {
                    "red": [0, 40], "yellow":[40, 80], "green": [80, 100]}},
                value=int(
                    thisWeekKPIs_USPP['Successful Ratio of BOSS Operation'].iloc[-1]),
                max=100,
                min=0,
                size=150,
            ),
        ], className='gaugeDiv'),
        dash.html.Div(children=[
            dash.html.H6('SPR Registered Users'),
            daq.Gauge(
                value=int(
                    thisWeekKPIs_USPP['Number of SPR Registered User'].iloc[-1]),
                max=round(
                    thisWeekKPIs_USPP['Number of SPR Subscribers'].max()),
                min=0,
                size=150,
            ),
        ], className='gaugeDiv'),
    ]),

    dash.html.Iframe(src=r"http://10.7.33.4/Reports4G/powerbi/WIND%204G%20RAN/WIND_KPI_RF?rs:embed=true",
        style={"height": "1067px", "width": "100%"}) 
    ])