import pandas as pd
import plotly
import dash
import plotly.express as px
import os
import datetime
import sys
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

sys.path.insert(1,'C:/Users/Administrator/Documents/Scripts/databaseLoader/')
import dbLoader

# Generador de callbacks para click sobre tarjetas
def basicViewGraphCBGenerator(kpiName, eventName):
    def callback(_,__, kpiData):
        kpiDF = pd.read_json(kpiData)
        kpiDF['Start Time']= pd.to_datetime(kpiDF['Start Time']).dt.tz_localize(None)
        kpiDF['End Time']= pd.to_datetime(kpiDF['End Time']).dt.tz_localize(None)
        thisWeekKPIs = kpiDF[kpiDF['Start Time'] >= (datetime.datetime.now() - datetime.timedelta(days=7))]

        triggeringCB = dash.callback_context.triggered_prop_ids

        fig = plotly.graph_objs.Figure()
        lastWeekMeanSeries = thisWeekKPIs.groupby([thisWeekKPIs['Start Time'].dt.date])[kpiName].mean()
        df = pd.DataFrame({'Start Time':lastWeekMeanSeries.index, lastWeekMeanSeries.name: lastWeekMeanSeries.values})

        fig.update_layout(
            autosize=False,
            width=400,
            height=200,
            margin={'t':0, 'r':10, 'l':10, 'autoexpand':True,},
            xaxis={'fixedrange':True},
            yaxis={'fixedrange':True},
        )

        stdSeries = kpiDF.groupby([thisWeekKPIs['Start Time'].dt.date])[lastWeekMeanSeries.name].std()

        fig.add_trace(
            plotly.graph_objs.Scatter(
                x=df['Start Time'],
                y=df[lastWeekMeanSeries.name],
                error_y=dict(
                    type='data',
                    array=stdSeries,
                    visible=True)
                )
            )

        if len(triggeringCB.keys()) and (list(triggeringCB.keys())[0] == eventName):
            return fig

        return fig

    return callback

def dateChangeCBGen():
    def callback(start_date: datetime.datetime, end_date: datetime.datetime, selector: list, checklistOptions: list, kpiData):
        kpiDF = pd.read_json(kpiData)
        kpiDF['Start Time']= pd.to_datetime(kpiDF['Start Time']).dt.tz_localize(None)
        kpiDF['End Time']= pd.to_datetime(kpiDF['End Time']).dt.tz_localize(None)

        tempDF = kpiDF[(kpiDF['Start Time'] >= start_date) & (kpiDF['End Time'] < end_date)]
        fig = plotly.graph_objs.Figure()
        fig.update_layout(title={
            'text':'Averaged view',
            'font':{
                'size':35
                }
            })

        if len(selector) > 0:
            for _, value in enumerate(selector):
                meanSeries = tempDF.groupby([tempDF['Start Time'].dt.date])[value].mean()
                stdSeries = tempDF.groupby([tempDF['Start Time'].dt.date])[value].std()
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
    return callback

def clickedDatapointCBGen(event):
    def callback(clickData, aggFigure, selector, kpiData):
        kpiDF = pd.read_json(kpiData)
        kpiDF['Start Time']= pd.to_datetime(kpiDF['Start Time']).dt.tz_localize(None)
        kpiDF['End Time']= pd.to_datetime(kpiDF['End Time']).dt.tz_localize(None)

        triggeringCB = dash.callback_context.triggered_prop_ids
        fig = plotly.graph_objs.Figure()
        fig.update_layout(title={
            'text':'Daily detail',
            'font':{
                'size':35
                }
            })

        try:
            if list(triggeringCB.keys())[0] == event:
                dateToInspect = pd.to_datetime(clickData['points'][0]['x']).date()
            else:
                dateToInspect = pd.to_datetime(aggFigure['data'][0]['x'][-1]).date()
        except:
            return fig

        if selector:
            filteredDF = kpiDF[ kpiDF['Start Time'].apply(lambda x: pd.to_datetime(x).date()) == dateToInspect]
            for _, value in enumerate(selector):
                fig.add_trace(plotly.graph_objs.Scatter(
                    x=filteredDF['Start Time'],
                    y=filteredDF[value],
                    ))

        return fig

    return callback

def figCombinator(columns, argDF=None)->dash.dcc.Graph:
    if len(columns) > 1:
        fig = px.scatter(argDF, x="Start Time", y=columns[0], color=columns[1],
                         title=columns[0], width=1000, height=500)
        fig.update_coloraxes(
                colorbar_title={
                    'side':'right'
                    })
        fig.add_traces(plotly.graph_objs.Scatter(x=argDF["Start Time"], y=argDF[columns[0]], mode='line'))
    else:
        fig = px.scatter(argDF, x="Start Time", y=columns[0],
                         title=columns[0], width=1000, height=500)

    fig.update_layout(title_font_size=30)

    return dash.dcc.Graph(figure=fig, config={'displayModeBar':False, 'responsive':True, 'scrollZoom': True})

# Cargado del dataframe de donde se va a sacar la data
def queryDataFromDB(start_date=datetime.datetime.today() - datetime.timedelta(days=7), end_date=datetime.datetime.now(), element='xGW') -> pd.DataFrame:
    # Conexion y preparativos con la base de datos
    Base = automap_base()
    Base.prepare(autoload_with=dbLoader.engine, reflect=True)

    table = ''

    for tableName in Base.classes.keys():
        if element.lower() in tableName:
            table = Base.classes.get(tableName)

    if table == '':
        return None

    # Query y generacion del dataframe relevante
    session = Session(dbLoader.engine)
    res = session.query(table).filter(table.Start_Time < end_date , table.Start_Time >= start_date)
    df = pd.read_sql(res.statement, res.session.bind)

    # Correccion del nombre de las columnas
    df.rename(columns=dict(zip(df.columns, df.columns.map(lambda arg: arg.replace('_', " ")))), inplace=True)

    return df

def queryCallbackGen(element: str):
    def callback(arg):
        kpiDF = queryDataFromDB(start_date=datetime.datetime(year=2022, month=10, day=1), element=element)
        return kpiDF.to_json(orient='records', date_format='iso')

    return callback


def selectorValueLoader(kpiData):
    kpiDF = pd.read_json(kpiData)
    kpiDF['Start Time']= pd.to_datetime(kpiDF['Start Time']).dt.tz_localize(None)
    kpiDF['End Time']= pd.to_datetime(kpiDF['End Time']).dt.tz_localize(None)

    options=kpiDF.columns[4:-1]
    value=[kpiDF.columns[-3]]

    return options, value

def widgetCBGen(widgetDic: dict, key:str):
    def callback(kpiData):
        kpiDF = pd.read_json(kpiData)
        kpiDF['Start Time']= pd.to_datetime(kpiDF['Start Time']).dt.tz_localize(None)
        return kpiDF[widgetDic[key]].iloc[-1]

    return callback
