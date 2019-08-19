import app_modules as mdl
import dash_html_components as html
from dash_daq import ToggleSwitch
import dash_core_components as dcc

Map_layout = html.Div([
    html.Div([
        # dcc.Dropdown(
        #     id='demo',
        #     options=[
        #         {'label': 'Demonstration', 'value': 'False'},
        #         {'label': 'Full Database', 'value': 'True'},
        #     ],
        #     value='False'
        # ),
        # mdl.Modal_address,
        # html.H1("Seattle ADU Feasibility", style={'textAlign': 'center'}),
        html.H3("Help us find your home:", style={'textAlign': 'center'}),
        html.Div(["This address bar only contains single family and multi-family residential parcels."],
                 style={'fontSize': '11px'}),
        html.Div(id='addressDropdown'),
        mdl.AddressDropdown,
        html.H3(""),
        html.H3(""),
        # ToggleSwitch(
        #     id='demo',
        #     label=['Demo', 'Full'],
        #     style={'width': '350px', 'margin': 'auto'},
        #     value=False),

        html.H4("Let's find an ADU around you!", style={'textAlign': 'center'}),
        html.Div(id='adu_around'),
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
],
)

Transparency_layout = html.Div([
    html.H2("Transparency",
            style={'textAlign': 'center', 'color': '#7FDBFF'}),

    mdl.Transparency,
],
)

Home_layout = html.Div([

    mdl.Home,
    html.P(' © ADUniverse, DSSG 2019, eScience Institute, University of Washington'),
    html.P(' Project Leads: Rick Mohler, Nick Welch, Joseph Hellerstein'),
    html.P(' Fellows: Emily Finchum-Mason, Yuanhao Niu, Adrian Tullock, Anagha Uppal'),
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
