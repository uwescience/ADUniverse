import app_modules as mdl
import dash_html_components as html
from dash_daq import ToggleSwitch
import dash_core_components as dcc
import dash_dangerously_set_inner_html as dish

Map_layout = html.Div([
    html.Div([
        html.H3("Help us find your home:", style={'textAlign': 'center'}),
        html.Div(["This address bar only contains single family and multi-family residential parcels."],
                 style={'fontSize': '11px'}),
        html.Div(id='addressDropdown'),
        mdl.AddressDropdown,
        html.H3(""),
        html.H3(""),
        mdl.NeighborInfo,
        mdl.OutputDetails,
        html.Div(id='next_page'),

    ], className="five columns"),
    html.Div([
        mdl.MapBlock,
        mdl.AdditionalDetails,

    ], className="seven columns"),


], className="row", style={'margin-left': '25px', 'margin-right': '25px', })


Finance_layout = html.Div([
    html.H2("Let's do the numbers!",
            style={'textAlign': 'center', 'color': '#7FDBFF'},),

    mdl.FinFeasibility,
],
)

FAQ_layout = html.Div([
    html.H2("Frequently Asked Questions",
            style={'textAlign': 'center', 'color': '#7FDBFF'}),

    mdl.FAQ,
],style={'marginLeft': 15, 'marginRight': 15}
)

Transparency_layout = html.Div([
    html.H2("Transparency",
            style={'textAlign': 'center', 'color': '#7FDBFF'}),

    mdl.Transparency,
],
)

Home_layout = html.Div([

    mdl.Home,
],
)

Testimonials_layout = html.Div([
    html.H2("Stories and Testimonials",
            style={'textAlign': 'center', 'color': '#7FDBFF'}),

],
)

Analysis_layout = html.Div([
    html.H2("Citywide Analysis",
            style={'textAlign': 'center', 'color': '#7FDBFF'}),

    mdl.Analysis,
],
)

Neighborhood_layout = html.Div([
    html.H2("Neighborhood Analysis",
            style={'textAlign': 'center', 'color': '#7FDBFF'}),

    mdl.ADU_Counts,
],
)
