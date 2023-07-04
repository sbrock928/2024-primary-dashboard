import dash_bootstrap_components as dbc
from dash import html

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
                dbc.NavLink(
                    "Github",
                    href="https://github.com/sbrock928/professional-portfolio",
                    external_link=True,
                    target="blank",
                ),
            ]
        ),
        html.Iframe(
            id="embedded-pdf",
            src="../assets/stephen_brock_resume_07_23.pdf",
            width="90%",
            height="750vh",
        ),
    ]
)
