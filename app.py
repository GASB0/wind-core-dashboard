from dash import Dash, html, dcc
import dash
import dash_bootstrap_components as dbc
import sys
import datetime

sys.path.insert(1,'./pages')
import utilidadesVarias as uv

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

memoryStores = {'xGWMemory': 'xGW',
                 'RCPMemory':'RCP',
                 'MMEMemory': 'MME',
                 'USPPMemory': 'USPP'}

for store in memoryStores.keys():
    dash.callback(
        dash.Output(store, 'data'),
        dash.Input('dbQueryInterval', 'n_intervals') # Definir cual va a ser el evento con el que voy a estar refrescando la data
    )(uv.queryCallbackGen(memoryStores[store]))

def serve_layout():
    return html.Div(children=[
    html.Div(className='navBar', children=[
        html.Div(className='navLink', children=[
            dcc.Link(
                f"{page['name']}", href=page["relative_path"]
                )
            ])
            for page in dash.page_registry.values()
     ]   
    ),
    *[dash.dcc.Store(id=key) for key in memoryStores.keys()],
    dash.dcc.Interval(id='dbQueryInterval', interval=1000*60*10, n_intervals=0),
    dash.page_container
])

app.layout = serve_layout

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8050, debug=True)
