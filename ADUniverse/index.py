import app_pages as ap
import callbacks
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from adu_app import app
from app_modules import NavigationBar


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    NavigationBar,
    html.Div(id='page-content')
])

# Code for changing the page


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return ap.Home_layout
    elif pathname == '/map':
        return ap.Map_layout
    elif pathname == '/finances':
        return ap.Finance_layout
    elif pathname == '/faq':
        return ap.FAQ_layout
    elif pathname == '/transparency':
        return ap.Transparency_layout
    elif pathname == '/testimonials':
        return ap.Testimonials_layout
    elif pathname == '/analysis':
        return ap.Analysis_layout
    elif pathname == '/neighborhood':
        return ap.Neighborhood_layout
    else:
        return '404'


if __name__ == '__main__':
    app.run_server(debug=True)
