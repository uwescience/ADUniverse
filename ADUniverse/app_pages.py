import app_modules as mdl
import constant as C
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from folium import Map

# create empty map zoomed in on Seattle
map = Map(location=C.SEATTLE, zoom_start=C.INIT_ZOOM, control_scale=True)
map.save("map.html")

Original_Page = [
    dcc.Location(id='url'),
    #dcc.Link('Tab 1', href='/'),
    #html.Br(),
    #dcc.Link('Tab 2', href='/apps/app1'),
    html.Div(id="page-content", style={'display': 'none'}),

    mdl.NavigationBar,

    html.H1("Seattle ADU Feasibility", style={'textAlign': 'center'}),

    html.H3("Find your home"),

    mdl.AddressDropdown,

    # Not intuitively named
    html.Div(id='intermediate-value', style={'display': 'none'}),

    # Not intuitively named
    html.Div(id='output-container', style={'display': 'none'}),

    html.Iframe(id='map', srcDoc=open("map.html", "r").read(),
                width="100%", height="550"),

    html.H2("Why are you thinking of building an ADU?"),

    mdl.PurposeDropdown,

    # Purpose output
    html.Div(id='output_purpose'),

    html.H2("Let's do the numbers!",
            style={'textAlign': 'center', 'color': '#7FDBFF'}, className="valuablys"),

    mdl.FinFeasibility,

    dcc.Markdown('''
    # **Frequently Asked Questions**
    # How to be a good landlord?
    Here is some useful information.
    [Rental Housing Association of Washington](https://www.rhawa.org/)
    # More financial information?
    Here is the home equity loan information
    *Disclaimer: We help to gather useful informtion to facilitate your decisions *
    '''),
]


New_Page = [
    dcc.Location(id='url'),
    #dcc.Link('Tab 1', href='/'),
    #html.Br(),
    #dcc.Link('Tab 2', href='/apps/app1'),
    html.Div(id="page-content", style={'display': 'none'}),

    mdl.NavigationBar,

    html.H1("Test Page", style={'textAlign': 'center'}),

    html.H3("Find your home"),

    mdl.AddressDropdown,

    # Not intuitively named
    html.Div(id='intermediate-value', style={'display': 'none'}),

    # Not intuitively named
    html.Div(id='output-container', style={'display': 'none'}),

    html.Iframe(id='map', srcDoc=open("map.html", "r").read(),
                width="100%", height="550"),

    html.H2("Why are you thinking of building an ADU?"),

    mdl.PurposeDropdown,

    # Purpose output
    html.Div(id='output_purpose'),

    html.H2("Let's do the numbers!",
            style={'textAlign': 'center', 'color': '#7FDBFF'}, className="valuablys"),

    mdl.FinFeasibility,

    dcc.Markdown('''
    # **Frequently Asked Questions**
    # How to be a good landlord?
    Here is some useful information.
    [Rental Housing Association of Washington](https://www.rhawa.org/)
    # More financial information?
    Here is the home equity loan information
    *Disclaimer: We help to gather useful informtion to facilitate your decisions *
    '''),
]
