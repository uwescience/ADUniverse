
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


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
)

app.layout = html.Div(
    [navb]
)

if __name__ == "__main__":
    app.run_server(debug=True, port=8888)

# @app.callback(Output("page-content", "children"), [Input("url", "pathname")])
# def render_page_content(pathname):
#     if pathname in ["/", "/map"]:
#         return html.P("This is the content of page 1!")
#     elif pathname == "/finances":
#         return html.P("This is the content of page 2. Yay!")
#     elif pathname == "/more-info":
#         return html.P("Oh cool, this is page 3!")
#     elif pathname == "/transparency":
#         return html.P("Oh cool, this is page 4!")
#     # If the user tries to reach a different page, return a 404 message
#     return dbc.Jumbotron(
#         [
#             html.H1("404: Not found", className="text-danger"),
#             html.Hr(),
#             html.P(f"The pathname {pathname} was not recognised..."),
#         ]
#     )
