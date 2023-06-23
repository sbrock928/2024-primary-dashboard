from dash import html
import dash_bootstrap_components as dbc


about_me_layout = html.Div(
    [
        html.H2(
            "About Me",
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
            src="assets/stephen_brock_resume.pdf",
            width="75%",
            height="750vh",
        ),
    ]
)
