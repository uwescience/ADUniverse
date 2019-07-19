import adusql as ads
import dash
import dash_core_components as dcc
import dash_html_components as html
import folium
import financials
import geojson
import json
import pandas as pd
import sys

from dash.dependencies import Input, Output
from folium.plugins import Search
import nltk
nltk.download('punkt')

# FILE = "adudata_UnivDist_small.csv"
SEATTLE_COORDINATES = (47.6062, -122.3321)
init_zoom = 12
# data = pd.read_csv(FILE)

adunit = ads.Connection("adunits.db")
adunit.connect()
addresses = adunit.select("address")
adunit.disconnect()

# create empty map zoomed in on Seattle
map = folium.Map(location=SEATTLE_COORDINATES,
                 zoom_start=12, control_scale=True)


# regular style of polygons
def style_function(feature):
    return {
        'weight': 2,
        'dashArray': '5, 5',
        'fillOpacity': 0,
        'lineOpacity': 1,
    }

# when polygon is selected, its style
def highlight_function(feature):
    return {
        'fillColor': 'blue',
        'weight': 2,
        'lineColor': 'black',
        'lineWeight': 2,
        'dashArray': '5, 5',
        'fillOpacity': 0.5,
        'lineOpacity': 1,
    }


# for speed purposes
MAX_RECORDS = 100

map.save("map.html")

# Dashify

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash("SeattleADU",
                external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1("Seattle ADU Feasibility"),

    html.H3("Find your home"),
    dcc.Dropdown(
        id='addressDropdown',
        options=[
            {'label': i, 'value': i} for i in addresses.address.unique()
        ],
        placeholder='Type your house address here...'),

    # Not intuitively named
    html.Div(id='intermediate-value', style={'display': 'none'}),

    # Not intuitively named
    html.Div(id='output-container'),

    html.Iframe(id='map', srcDoc=open("map.html", "r").read(),
                width="100%", height="550"),

    html.H2("Why are you thinking of building an ADU?"),
    dcc.Dropdown(
        # Not intuitively named
        id='my-dropdown',
        options=[
            {'label': 'Build one more unit for rental income', 'value': 'income'},
            {'label': 'A Relative needs some housing', 'value': 'support'},
        ],
        value='purposes'
    ),
    # Not intuitively named
    html.Div(id='output_drop'),

    html.H2("Let's do the numbers! (DADU)",
            style={'textAlign': 'center', 'color': '#7FDBFF'}),


    html.Div([
        html.Div([
            html.H3('Cost Breakdown'),
            html.H4('How large (square foot) will be your ADU?'),
            dcc.Input(id='BuildSizeInput', value='0', type='number'),
            html.Table([
                html.Tr([html.Td(['Construction Cost']), html.Td(id='ConstructCost')]),
                html.Tr([html.Td(['+ Sewer Capacity Charge ']), html.Td(11268)]),
                html.Tr([html.Td(['+  Permit Fee']), html.Td(4000)]),
                html.Tr([html.Td(['+  Architecture Fee']), html.Td(id='DesignCost')]),
                html.Tr([html.Td(['=  Estimated Cost']), html.Td(id='TotalCost')])])
        ], className="six columns"),

        html.Div([
            html.H3("How much do you want to borrow?"),
            dcc.Input(id='LoanInput', value='0', type='number'),
            html.Table([
                html.Tr([html.Td(['Total']), html.Td(id='LoanAmount')]),
                html.Tr([html.Td(['Monthly Payment']), html.Td(id='MortgageCalculator')])
            ]),

            html.H3("Where do you live?"),
            dcc.Dropdown(
                id='neighbor_dropdown',
                options=[  # data from zillow 2019/may rent per square foot
                    {'label': 'Ballard', 'value': '3.277945619'},
                    {'label': 'Capitol Hill', 'value': '3.22537112'},
                    {'label': 'Downtown', 'value': '3.861445783'},
                    {'label': 'Fremont', 'value': '3'}, ],
                value='3'),
            html.H3("Your expected monthly rental income"),
            html.Div(id='rental'),
        ], className="six columns"),

    ], className="row"),

    html.H2("Financial Feasibility", style={'textAlign': 'center'}),
    html.Div(id='ConcludeFinance', style={'textAlign': 'center'}),


    dcc.Markdown('''
    # **Frequently Asked Questions**
    # How to be a good landlord?
    here are some useful information.
    [Rental Housing Association of Washington](https://www.rhawa.org/)
    # More financial information?
    here are the home equity loan informations
    *Disclaimer: We help to gether useful informtions to facilitate your decisions *
    '''),
])

# calculate cost breakdown


@app.callback(
    [Output('ConstructCost', 'children'),
     Output('DesignCost', 'children'),
     Output('TotalCost', 'children')],
    [Input('BuildSizeInput', 'value')])
def cost_breakdown(value):
    # 'Total amount of loan is "{0:12,.0f}"'.format(loan)
    return financials.cost_breakdown(value)

# calculate the rental income


@app.callback(
    Output('rental', 'children'),
    [Input('BuildSizeInput', 'value'),
     Input('neighbor_dropdown', 'value')])
def rents(value1, value2):
    return float(value1)*float(value2)

# cost benefit analysis


@app.callback(
    Output('ConcludeFinance', 'children'),
    [Input('rental', 'children'),
     Input('MortgageCalculator', 'children')])
def decide_finance(benifit, cost):
    return financials.decide_finance(benifit, cost)


# dynamically updates the map based on the address selected


@app.callback(
    [Output('output-container', 'children'),
     Output('map', 'srcDoc')],
    [Input('addressDropdown', 'value')]
)
def update_map(value, coords=SEATTLE_COORDINATES, zoom=init_zoom):
    yearbuilt = 1

    if value != None:
        yearbuilt = 1
        # long = addresses.loc[addresses.address == value].reset_index()['INTPTLA'][0]
        # lat = addresses.loc[addresses.address == value].reset_index()['INTPTLO'][0]
        adunit = ads.Connection("adunits.db")
        adunit.connect()
        newCoords = adunit.getCoords(value)
        print(adunit.getParcelCoords(value))
        df = adunit.getParcelCoords(value)
        df.to_csv("df.csv")
        adunit.disconnect()
        coords = (newCoords.intptla[0], newCoords.intptlo[0])
        zoom = 14

    new_map = folium.Map(location=coords, zoom_start=zoom)

    def df_to_geojson(df, properties, lat='latitude', lon='longitude'):
        geojson = {'type': 'FeatureCollection', 'features': []}
        feature = {'type': 'Feature',
                   'properties': {},
                   'geometry': {'type': 'Polygon',
                                'coordinates': []}}
        for _, row in df.iterrows():
            feature['geometry']['coordinates'].append([row[lon], row[lat]])
            for prop in properties:
                feature['properties'][prop] = row[prop]
            geojson['features'] = feature
        return geojson

    cols = ['PIN', 'sqftlot']
    geojson = df_to_geojson(df, cols, lat='coordY', lon='coordX')

    parcel = folium.map.FeatureGroup(name="parcel",
                                     overlay=True, control=True, show=True,)

    for i in range(0, len(geojson["features"])):
        feature = folium.features.GeoJson(geojson["features"][i]["geometry"],
                                          name=(geojson["features"][i]["properties"]["PIN"]),
                                          style_function=style_function,
                                          highlight_function=highlight_function,)
        folium.Popup("PIN: " + geojson["features"][i]["properties"]["PIN"] + " " +
                     "Square feet of lot: " + geojson["features"][i]["properties"]["sqftlot"], max_width=200).add_to(feature)
        parcel.add_child(feature)

    parcel.add_to(map)

    new_map.save("map.html")
    # map.render()
    return 'The home you selected was built in year "{}"'.format(yearbuilt), open("map.html", "r").read()

# space holder for some features


@app.callback(
    Output('intermediate-value', 'children'),
    [Input('addressDropdown', 'value')]
)
def get_features(value):
    # if value != None:
        # output = data.loc[data['ADDRESS'] == value].reset_index()['YRBUILT'][0]
        # output = addresses.loc[addresses.address == value].reset_index()['YRBUILT'][0]
    output = 0
    return output

# caculating loans


@app.callback(
    [Output(component_id='LoanAmount', component_property='children'),
     Output(component_id='MortgageCalculator', component_property='children')],
    [Input(component_id='LoanInput', component_property='value'),
     Input(component_id='intermediate-value', component_property='children')]
)
def loan_calculator(loan, feature):
    return financials.loan_calculator(loan, feature)

# print out


@app.callback(
    Output('output_drop', 'children'),
    [Input('my-dropdown', 'value')])
def update_purpose(value):
    return 'You are builing this ADU for "{}"'.format(value)


if __name__ == '__main__':
    app.run_server(debug=True)
