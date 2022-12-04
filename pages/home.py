import dash
from dash import html

dash.register_page(__name__, path='/')

layout = html.Div(children=[
    html.H1('General CORE status'),
    html.Div(id='temperature_card', children=[]),
    html.Div(className='card_container', children=[
        html.Div(id='MME_card', className='infoCard', children=[
            html.H3('MME')
            ]),
        html.Div(id='xGW_card', className='infoCard', children=[
            html.H3('xGW')
            ]),
        html.Div(id='USPP_card', className='infoCard', children=[
            html.H3('USPP')
            ]),
        html.Div(id='RCP_card', className='infoCard', children=[
            html.H3('RCP')
            ]),
        ])
    ])
