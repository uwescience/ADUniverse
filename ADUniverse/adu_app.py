import dash
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash("SeattleADU", external_stylesheets=external_stylesheets)
server = app.server
app.config.suppress_callback_exceptions = True
