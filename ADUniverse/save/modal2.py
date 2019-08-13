import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
# import plotly
# import plotly.plotly as py
# import plotly.graph_objs as go

external_stylesheets =['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
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

app.layout = html.Div([Modal_address], style={'backgroundColor':'black'})

def toggle_modal(n1, n2, is_open):

    #return not is_open
    return is_open
app.callback(
     Output("modalBlog", "is_open"),
    [Input("closeBlog", "n_clicks"),Input("closeBlog", "n_clicks")],
    [State("modalBlog", "is_open")],
)(toggle_modal)


if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
