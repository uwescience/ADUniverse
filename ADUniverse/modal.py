import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State

external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash("SeattleADU", external_stylesheets=external_stylesheets)

modal_address = html.Div(
    [
        dbc.Button("Open modal", id="open"),
        dbc.Modal(
            [
                dbc.ModalHeader("Header"),
                dbc.ModalBody("This is the content of the modal"),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close", className="ml-auto")
                ),
            ],
            id="modal",
        ),
    ]
)

app.layout = html.Div([
    modal_address,
    ])


@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

# # hide/show modal
# @app.callback(Output('modal', 'style'),
#               [Input('instructions-button', 'n_clicks')])
# def show_modal(n):
#     if n > 0:
#         return {"display": "block"}
#     return {"display": "none"}

# # Close modal by resetting info_button click to 0
# @app.callback(Output('instructions-button', 'n_clicks'),
#               [Input('modal-close-button', 'n_clicks')])
# def close_modal(n):
#     return 0



if __name__ == "__main__":
    app.run_server(debug=True, port=8888)

