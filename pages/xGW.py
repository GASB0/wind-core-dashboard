import dash
import os
import datetime
from dash import html
import pandas as pd
import plotly

# Cargado del dataframe de donde se va a sacar la data
def queryDataFromDB(start_date=datetime.datetime.today() - datetime.timedelta(days=10), end_date=datetime.datetime.today()) -> pd.DataFrame:
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

dash.register_page(__name__)

layout = html.Div(children=[
    html.H1(children='xGW Page'),
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
                    dash.html.Label('Statistical information'),
                    dash.dcc.Checklist(options=['variance'], id='metricsCheckList', value=[]),
                    dash.html.Br(),
                    dash.html.Label('KPIs to be selected'),
                    dash.dcc.Dropdown(options=kpiDF.columns[5:], value=[kpiDF.columns[7]], multi=True, id='kpiSelector', placeholder="Select a KPI"),
                    ]),
                html.Div(id='statsContainer'),
                ]),
            ]),
        ]),
    ])


# Refrescado del grafico primario
@dash.callback(
        dash.Output('advancedTabGraph', 'figure'),
        dash.Input('dateRange', 'start_date'),
        dash.Input('dateRange', 'end_date'),
        dash.Input('kpiSelector', 'value'),
        dash.Input('metricsCheckList', 'value')
        )
def dateChange_cb(start_date, end_date, selector, checklistOptions):
    kpiDF = queryDataFromDB(start_date, end_date)
    fig = plotly.graph_objs.Figure()

    if len(selector) > 0:
        for _, value in enumerate(selector):
            meanSeries = kpiDF.groupby([kpiDF['Start Time'].dt.date])[value].mean()
            varianceSeries = kpiDF.groupby([kpiDF['Start Time'].dt.date])[value].var()
            df = pd.DataFrame({'Start Time':meanSeries.index, meanSeries.name: meanSeries.values, 'variance': varianceSeries.values})
            
            fig.add_trace(
                    plotly.graph_objs.Scatter(
                        x=df['Start Time'],
                        y=df[value],
                        error_y=dict(
                            type='data',
                            array=df['variance'],
                            visible=True) if 'variance' in checklistOptions else None
                        )
                    )
    return fig

# Refrescado del grafico secundario
@dash.callback(
        dash.Output('dailyGraph', 'figure'),
        dash.Input('advancedTabGraph', 'clickData'),
        dash.Input('advancedTabGraph', 'figure'),
        dash.Input('kpiSelector', 'value'),
        )
def clicked_datapoint_cb(clickData, aggFigure, selector):
    triggeringCB = dash.callback_context.triggered_prop_ids
    fig = plotly.graph_objs.Figure()

    try:
        if list(triggeringCB.keys())[0] == 'advancedTabGraph.clickData':
            dateToInspect = pd.to_datetime(clickData['points'][0]['x']).date()
        else:
            dateToInspect = pd.to_datetime(aggFigure['data'][0]['x'][-1]).date()
    except IndexError:
        return fig

    if selector:
        filteredDF = kpiDF[ kpiDF['Start Time'].apply(lambda x: pd.to_datetime(x).date()) == dateToInspect]
        for _, value in enumerate(selector):
            fig.add_trace(plotly.graph_objs.Scatter(
                x=filteredDF['Start Time'],
                y=filteredDF[value],
                ))

    return fig

# Refrescando los graficos de las tarjetas del basic view
@dash.callback(
        dash.Output('daily_cpu_usage', 'figure'),
        dash.Input('daily_cpu_usage', 'figure'),
        )
def basicCPUCB(_):
    kpiName = 'Peak load of CPU usage of the main processor(%)'
    fig = plotly.graph_objs.Figure()
    lastWeekMeanSeries = thisWeekKPIs.groupby([thisWeekKPIs['Start Time'].dt.date])[kpiName].mean()
    df = pd.DataFrame({'Start Time':lastWeekMeanSeries.index, lastWeekMeanSeries.name: lastWeekMeanSeries.values})
    
    fig.add_trace(
        plotly.graph_objs.Scatter(
            x=df['Start Time'],
            y=df[lastWeekMeanSeries.name],
            )
        )

    return fig

# Callback de la carta de IP usage
@dash.callback(
        dash.Output('daily_ip_usage', 'figure'),
        dash.Output('kpiSelector', 'value'),
        dash.Output('xGW-tabs', 'value'),
        dash.Input('daily_ip_usage', 'figure'),
        dash.Input('daily_ip_usage', 'clickData'),
        dash.State('xGW-tabs', 'value'),
        )
def basicIPCB(_, __, tabSelected):
    triggeringCB = dash.callback_context.triggered_prop_ids
    kpiName = 'IP Pool Usage(%)'

    fig = plotly.graph_objs.Figure()
    lastWeekMeanSeries = thisWeekKPIs.groupby([thisWeekKPIs['Start Time'].dt.date])[kpiName].mean()
    df = pd.DataFrame({'Start Time':lastWeekMeanSeries.index, lastWeekMeanSeries.name: lastWeekMeanSeries.values})
    
    fig.add_trace(
        plotly.graph_objs.Scatter(
            x=df['Start Time'],
            y=df[lastWeekMeanSeries.name],
            )
        )

    if len(triggeringCB.keys()) and (list(triggeringCB.keys())[0] == 'daily_ip_usage.clickData'):
        print(triggeringCB.keys())
        print(tabSelected)
        return fig, [kpiName], 'advancedView'

    return fig, [kpiName], tabSelected
