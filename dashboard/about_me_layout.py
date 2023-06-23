from dash import html
import dash_bootstrap_components as dbc


about_me_layout = html.Div(
    [
        html.H2(
            "About Me",
            style={
                "padding-left": 25,
                "padding-top": 10,
                "padding-bottom": 5,
                "background-color": "#FF0000",
                "color": "white",
                "border-bottom": "black",
            },
        ),
        html.Div(
            [
                dbc.NavLink(
                    "Linkedin",
                    href="https://www.linkedin.com/in/stephen-brock/",
                    external_link=True,
                    target="blank",
                ),
            ]
        ),
        html.Iframe(
            id="embedded-pdf",
            src="../assets/stephen_brock_resume.pdf",
            width="75%",
            height="750vh",
        ),
    ]
)
