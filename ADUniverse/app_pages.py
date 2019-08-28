import app_modules as mdl
import dash_html_components as html
from dash_daq import ToggleSwitch
import dash_core_components as dcc
import dash_dangerously_set_inner_html as dish
import dash_bootstrap_components as dbc


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
    html.Img(src="assets/adu-1.png", alt="Sample ADU from AARP Brochure",),
    html.Img(src="assets/adu-2.png", alt="Sample ADU from AARP Brochure",),
    html.Img(src="assets/adu-3.png", alt="Sample ADU from AARP Brochure",),
    dbc.Row([
                dbc.Col(dcc.Markdown('''
                    "What we were looking for in terms of a community and aging in place was \
                    right under our noses. Remove a fence and create a shared open space. Build \
                    a wall and create a second dwelling unit. It doesn’t have to be complicated."
                    ''') ),
                dbc.Col(dcc.Markdown('''
                    “We were looking for a way to live in our house for the rest of our lives and to \
                    generate at least some income in the process,” Robert Mercer and Jim Heuer wrote for the \
                    program guide of the annual Portland ADU Tour when their home was part of the lineup. “An ADU \
                    offers the possibility of caregiver lodging in the future or even a place for us to live \
                    while we rent out the main house if we get to the point where we can’t handle the stairs any longer.”
                    ''') ),
                dbc.Col(dcc.Markdown('''
                    Bertha and her son John talked about someday buying a house with a mother-in-law suite. \
                    “Then one day someone came along and wanted my house, so I up and sold it,” she explains. “But \
                    that left me homeless. I asked John if I could build a small house in his backyard and he agreed.
                    ''') ),
            ],
            ),

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
