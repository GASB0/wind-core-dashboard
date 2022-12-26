import pandas as pd
import plotly
import dash
import plotly.express as px
import os
import datetime

# Generador de callbacks para click sobre tarjetas
def basicViewGraphCBGenerator(kpiName, eventName, thisWeekKPIs, kpiDF):
    def callback(_,__):
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
            print(triggeringCB.keys())
            return fig

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
def queryDataFromDB(start_date=datetime.datetime.today() - datetime.timedelta(days=30), end_date=datetime.datetime.today(), element='xGW') -> pd.DataFrame:
    """
    TODO: Termina de implementarme.
    Esta funcion hace un query hacia la base de datos para obtener la data que se encuentra dentro del 
    rango de fechas especificado
    """
    root = 'assets/data/'
    dfs = []
    for _, _, names in os.walk(root):
        for name in names:
            if element in name:
                dfs.append(pd.read_csv(root+name))

    df = pd.concat(dfs, ignore_index=True)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    if 'IP Pool Usage(%)' in df.columns:
        df['IP Pool Usage(%)'] = df['IP Pool Usage(%)'].str.rstrip('%').astype(float)

    return df[df['Start Time'] > start_date][df['Start Time'] < end_date]