import app_modules as mdl
import dash_html_components as html



Map_layout = html.Div([
    html.Div([
        # mdl.Modal_address,
        # html.H1("Seattle ADU Feasibility", style={'textAlign': 'center'}),
        html.H3("Find your home", style={'textAlign': 'center'}),
        mdl.AddressDropdown,
        html.H3(""),
        html.H3(""),
        html.H4("Does your neighbor have an ADU?", style={'textAlign': 'center'}),
        html.Div(id='adu_around'),
        mdl.OutputDetails,

        html.Div(id='next_page'),

        #html.H4("What's your Zipcode?", style={'textAlign': 'center'}),
        #html.Div(id='zip_code'),  # style={'display': 'none'}
    ], className="five columns"),
    html.Div([
        mdl.MapBlock,
        mdl.AdditionalDetails,

    ], className="seven columns"),


], className="row", style={'margin-left': '25px', 'margin-right': '25px', })
# html.H1("Seattle ADU Feasibility", style={'textAlign': 'center'}),


Finance_layout = html.Div([
    #html.H1("Seattle ADU Feasibility", style={'textAlign': 'center'}),
    html.H2("Let's do the numbers!",
            style={'textAlign': 'center', 'color': '#7FDBFF'},),

    mdl.FinFeasibility,
],
)

FAQ_layout = html.Div([
    #html.H1("Seattle ADU Feasibility", style={'textAlign': 'center'}),
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
    html.H2("Home",
            style={'textAlign': 'center', 'color': '#7FDBFF'}),

    mdl.Home,
],
)

Testimonials_layout = html.Div([
    html.H2("Stories and Testimonials",
            style={'textAlign': 'center', 'color': '#7FDBFF'}),

    # mdl.Home,
],
)

Analysis_layout = html.Div([
    html.H2("Citywide Analysis",
            style={'textAlign': 'center', 'color': '#7FDBFF'}),

    mdl.Analysis,
],
)
