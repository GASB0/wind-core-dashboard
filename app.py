from dash import Dash, html, dcc
import dash
import dash_bootstrap_components as dbc

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div(children=[
    html.Div(className='navBar', children=[
        html.Div(className='navLink', children=[
            dcc.Link(
                f"{page['name']}", href=page["relative_path"]
                )
            ])
            for page in dash.page_registry.values()
     ]   
    ),
    dash.page_container
])

if __name__ == '__main__':
   app.run_server(debug=True)
