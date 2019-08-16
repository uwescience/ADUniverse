import app_modules as mdl
import dash_html_components as html


Map_layout = html.Div([
    html.Div([
        html.H3("Help us find your home:", style={'textAlign': 'center'}),
        mdl.AddressDropdown,
        html.H3(""),
        html.H3(""),
        html.H4("Let's find an ADU around you!", style={'textAlign': 'center'}),
        html.Div(id='adu_around'),
        mdl.OutputDetails,
        html.Div(id='next_page'),

    ], className="five columns"),
    html.Div([
        mdl.MapBlock,
        mdl.AdditionalGoodDetails,
        mdl.AdditionalBadDetails,

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
