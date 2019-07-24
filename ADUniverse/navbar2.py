
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


navb = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Map", href="/map")),
        dbc.NavItem(dbc.NavLink("Financial Feasibility", href="/finances")),
        dbc.NavItem(dbc.NavLink("Additional Information", href="/more-info")),
        dbc.NavItem(dbc.NavLink("Transparency", href="/transparency")),

    ],
    brand="Seattle ADU Feasibility",
    brand_href="http://www.seattle.gov/services-and-information/city-planning-and-development",
    brand_external_link=True,
    color="primary",
    dark=True,
    fluid=True,
    id="navbar",
    className="",

)

app.layout = html.Div(
    [navb]
)

if __name__ == "__main__":
    app.run_server(debug=True, port=8888)

