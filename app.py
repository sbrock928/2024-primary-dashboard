import dash
import dash_bootstrap_components as dbc
import pandas as pd

from dash import html, dcc, Input, Output
from dashboard.layout import summary


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.config.suppress_callback_exceptions = True


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    dcc.Interval(
        id='interval-component',
        interval=30000,
        n_intervals=1
    )
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/summary' or pathname == '/summary/':
        return summary
    else:
        return summary



if __name__ == '__main__':
	app.run_server(debug=True)