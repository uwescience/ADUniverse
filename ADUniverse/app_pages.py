import app_modules as mdl
import dash_html_components as html


Map_layout = html.Div([
    #html.H1("Seattle ADU Feasibility", style={'textAlign': 'center'}),
    html.H2("Find your home"),
    mdl.AddressDropdown,
    mdl.MapBlock,
    html.H2("Why are you thinking of building an ADU?"),
    mdl.PurposeDropdown,

    # Purpose output
    html.Div(id='output_purpose'),

    ],
)

Finance_layout = html.Div([
    #html.H1("Seattle ADU Feasibility", style={'textAlign': 'center'}),
    html.H2("Let's do the numbers!",
            style={'textAlign': 'center', 'color': '#7FDBFF'}, className="valuablys"),

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
