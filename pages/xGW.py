import dash
import datetime
from dash import html

dash.register_page(__name__)

layout = html.Div(children=[
    html.H1(children='This is our Home page'),
    html.Div(children=""" This is our home page. """),
    dash.dcc.Tabs(id="xGW-tabs", value='basicView', children=[
        dash.dcc.Tab(label='Basic view', value='basicView', children=[
            dash.html.Div(id='basicTab',children=[
                dash.html.Div(className='card_container', children=[
                    dash.html.Div(id='cpu_card',className='infoCard', children=[
                        dash.html.H3('CPU %'),
                        dash.html.Div('sample text'),
                        dash.dcc.Graph(id='daily_cpu_usage', figure={'layout': {'height': 300, 'width':300}}, config={'displayModeBar':False, 'responsive':True, 'scrollZoom': True}),
                        ]),
                    dash.html.Div(id='memory_card', className='infoCard', children=[
                        dash.html.H3('Memory %'),
                        dash.dcc.Graph(id='daily_cpu_usage', figure={'layout': {'height': 300, 'width':300}}, config={'displayModeBar':False, 'responsive':True, 'scrollZoom': True}),
                        ]),
                    ])
                ])
            ]),
        dash.dcc.Tab(label='Advanced view', value='advancedView', children=[
            html.Div(id='advancedTab', children=[
                html.Div(children=[
                    dash.dcc.DatePickerRange(
                        id='dateRange',
                        min_date_allowed=datetime.date(1995, 8, 5),
                        max_date_allowed=datetime.date(2017, 9, 19),
                        initial_visible_month=datetime.date(2017, 8, 5),
                        end_date=datetime.date(2017, 8, 25)
                        ),
                    dash.dcc.Graph(
                        id='advancedTabGraph',
                        figure={
                            'data':[{
                                'x': [1,2,3],
                                'y': [5,10,6],
                                'type':'bar'
                                }]
                            }
                        ),
                    dash.html.Label('KPIs to be selected'),
                    dash.dcc.Dropdown(['KPI1', 'KPI2', 'KPI3'], multi=True, id='kpiSelector',  placeholder="Select a city",),
                    ]),
                html.Div(id='statsContainer'),
                html.Div(id='testContainer'),
                ]),
                dash.dcc.Checklist(
                    options=[
                        'Linear regression',
                        'Polynomial regression', 
                        'Moving average filter', 
                        ],
                    id='statisticAnalysisSelector'
                    )
            ]),
        ]),
    ])

@dash.callback(
        dash.Output(component_id='statsContainer', component_property='children'),
        dash.Input('kpiSelector', 'value'),
        )
def stats_update_cb(selectedValues):
    if selectedValues:
        return [f"Variance value: {value}" for value in selectedValues]
    else:
        return None

@dash.callback(
        dash.Output(component_id='testContainer', component_property='children'),
        dash.Input(component_id='statisticAnalysisSelector', component_property='value'),
        dash.Input(component_id='advancedTabGraph', component_property='figure'),
        )
def data_processing_cb(selectedModels, figure):
    if selectedModels:
        return figure['data'][0]['x']
        # for model in selectedModels:
        #     pass
        # return selectedModels
    else:
        return None
