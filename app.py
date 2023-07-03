import dash
import dash_bootstrap_components as dbc

from dash import html, dcc, Input, Output, State
from dashboard.elections.layouts.main_layout import election_dashboard_layout
from dashboard.about_me import about_me_layout
from dashboard.sidebar import sidebar
from dash_bootstrap_templates import load_figure_template
from dashboard.elections.callbacks import get_callbacks

from typing import Any

dbc_css = (
    "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css"
)

load_figure_template("cosmo")

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.COSMO, dbc_css],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
server = app.server
app.config.suppress_callback_exceptions = True
get_callbacks(app)

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        dbc.Container(
            [sidebar, html.Div(id="page-content")], className="dbc", fluid=True
        ),
        dcc.Interval(
            id="interval-component", interval=1, n_intervals=0, max_intervals=1
        ),
    ]
)


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname: str) -> Any:
    """
    This callback supports URL routing within the dash app
    """

    if pathname == "/":
        return about_me_layout
    elif pathname == "/election-dashboard":
        return election_dashboard_layout

    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )


@app.callback(
    Output("sidebar", "className"),
    [Input("sidebar-toggle", "n_clicks")],
    [State("sidebar", "className")],
)
def toggle_classname(n: int, classname: str) -> Any:
    """
    This callback supports the show/hide of the sidebar
    """
    if n and classname == "":
        return "collapsed"
    return ""


@app.callback(
    Output("collapse", "is_open"),
    [Input("navbar-toggle", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n: int, is_open: str) -> Any:
    """
    This callback supports the show/hide of the sidebar
    """
    if n:
        return not is_open
    return is_open


if __name__ == "__main__":
    app.run_server(debug=False, host="0.0.0.0", port=8080)
