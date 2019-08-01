import callbacks
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pdb

from adu_app import app
from app_modules import NavigationBar
from app_pages import Map_layout, Finance_layout, FAQ_layout, Transparency_layout, Home_layout, Testimonials_layout

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
        return Home_layout
    elif pathname == '/map':
        return Map_layout
    elif pathname == '/finances':
        return Finance_layout
    elif pathname == '/faq':
        return FAQ_layout
    elif pathname == '/transparency':
        return Transparency_layout
    elif pathname == '/testimonials':
        return Testimonials_layout
    else:
        return '404'


if __name__ == '__main__':
    app.run_server(debug=True)