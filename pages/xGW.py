import dash
import json
import datetime
from dash import html
import pandas as pd

# Cargado del dataframe de donde se va a sacar la data
def queryDataFromDB(start_date=datetime.datetime.today() - datetime.timedelta(days=7), end_date=datetime.datetime.today()) -> pd.DataFrame:
        """
        TODO: Termina de implementarme.
        Esta funcion hace un query hacia la base de datos para obtener la data que se encuentra dentro del 
        rango de fechas especificado
        """
        df = pd.read_csv('assets/KPI Warehouse - xGW_10857_202211290500.csv')
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        return df[df['Start Time'] > start_date][df['Start Time'] < end_date]

kpiDF = queryDataFromDB()

dash.register_page(__name__)

layout = html.Div(children=[
    html.H1(children='This is our Home page'),
    html.Div(children=""" This is our home page. """),
    dash.dcc.Tabs(id="xGW-tabs", value='advancedView', children=[
        dash.dcc.Tab(label='Basic view', value='basicView', children=[
            dash.html.Div(id='basicTab',children=[
                dash.html.Div(className='card_container', children=[
                    dash.html.Div(id='cpu_card',className='infoCard', children=[
                        dash.html.H3('CPU %'),
                        dash.html.Div(children=[ 'Peak load of CPU:', ]),
                        dash.html.Div(children=[ 'Peak load of CPU:', ]),
                        dash.dcc.Graph(id='daily_cpu_usage', figure={'layout': {'height': 300, 'width':300, 'margin':{'t':50, 'r':10}, 'title': 'Mean daily CPU usage'}}, config={'displayModeBar':False, 'responsive':True, 'scrollZoom': True}),
                        ]),
                    dash.html.Div(id='memory_card', className='infoCard', children=[
                        dash.html.H3('Memory %'),
                        dash.dcc.Graph(id='daily_memory_usage', figure={'layout': {'height': 300, 'width':300, 'margin':{'t':50, 'r':10}, 'title': 'Mean daily memory usage'}}, config={'displayModeBar':False, 'responsive':True, 'scrollZoom': True}),
                        ]),
                    dash.html.Div(id='ip_pool_usage', className='infoCard', children=[
                        dash.html.H3('IP Pool Usage'),
                        dash.dcc.Graph(id='daily_ip_usage', figure={'layout': {'height': 300, 'width':300, 'margin':{'t':50, 'r':10}, 'title': 'Mean daily IP usage'}}, config={'displayModeBar':False, 'responsive':True, 'scrollZoom': True}),
                        ])
                    ])
                ])
            ]),
        dash.dcc.Tab(label='Advanced view', value='advancedView', children=[
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
                    dash.html.Label('KPIs to be selected'),
                    dash.dcc.Dropdown(options=kpiDF.columns[5:], value=[kpiDF.columns[6]], multi=True, id='kpiSelector', placeholder="Select a KPI",),
                    ]),
                html.Div(id='statsContainer'),
                html.Div(id='testContainer'),
                ]),
            ]),
        ]),
    ])


# Refrescado del grafico primario
@dash.callback(
        dash.Output('advancedTabGraph', 'figure'),
        dash.Input('dateRange', 'start_date'),
        dash.Input('dateRange', 'end_date'),
        dash.Input('advancedTabGraph', 'figure'),
        )
def dateChange_cb(start_date, end_date, figure):
    kpiDF = queryDataFromDB(start_date, end_date)
    for ind, _ in enumerate(figure['data']):
        figure['data'][ind]['x'] = kpiDF['Start Time'].unique()
    return figure

# Refrescado del grafico secundario
@dash.callback(
        dash.Output('dailyGraph', 'figure'),
        dash.Input('advancedTabGraph', 'clickData'),
        dash.Input('dailyGraph', 'figure'),
        dash.Input('dateRange', 'start_date'),
        dash.Input('dateRange', 'end_date'),
        dash.Input('kpiSelector', 'value'),
        )
def clicked_datapoint_cb(clickData, figure, start_date, end_date, selector):
    triggeringCB = dash.callback_context.triggered_id

    # Limpiando el grafico
    for ind, value in enumerate(figure['data']):
        figure['data'][ind]['x'] = []
        figure['data'][ind]['y'] = []
        figure['data'][ind]['type'] = 'line'

    # Revisando de donde es que se activa el callback
    if triggeringCB == 'advancedTabGraph':
        xdate = pd.to_datetime(clickData['points'][0]['x']).date()
        figure['layout']['title'] = f"Statistics of {xdate}"
    else:
        xdate = pd.to_datetime(end_date).date() - datetime.timedelta(days=1)
        figure['layout']['title'] = f"Statistics of {end_date}"

    # Dibujado de la nueva grafica
    newXAxis = kpiDF[kpiDF['Start Time'].apply(lambda row: row.date()) == xdate]['Start Time']
    for ind, value in enumerate(selector):
        newYAxis = kpiDF[kpiDF['Start Time'].apply(lambda row: row.date()) == xdate][value]
        figure['data'][ind]['x'] = list(newXAxis)
        figure['data'][ind]['y'] = list(newYAxis)
        figure['data'][ind]['type'] = 'line'

    return figure
