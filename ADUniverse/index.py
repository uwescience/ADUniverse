import callbacks
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pdb

from adu_app import app
from app_modules import NavigationBar
from app_pages import Map_layout, Finance_layout, FAQ_layout, Transparency_layout, Home_layout, Testimonials_layout

app.config.suppress_callback_exceptions = True
Modal_address = html.Div(children=[
        #dbc.Button("BLOG", id="openBlog", size="lg"),
        dbc.Modal(
        [
          dbc.ModalHeader("BLOG"),
          dbc.ModalBody("It's the body"),
          dbc.ModalFooter(dbc.Button("Close",id="closeBlog",className="ml-auto"),),
        ], id="modalBlog",is_open = True
        ),
    ],
)

def toggle_modal(n1, n2, is_open):

    #return not is_open
    return is_open
app.callback(
     Output("modalBlog", "is_open"),
    [Input("closeBlog", "n_clicks"),Input("closeBlog", "n_clicks")],
    [State("modalBlog", "is_open")],
)(toggle_modal)


app.layout = html.Div([
    Modal_address,
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
