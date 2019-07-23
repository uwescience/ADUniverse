import adusql as ads
import constant as C
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq # requires dash_daq version 0.1.0
import folium
import financials as fin
# import geojson
# import json
import numpy as np
import pandas as pd
import sys
# import numpy as np

from dash.dependencies import Input, Output, State
# from folium.plugins import Search
import nltk
nltk.download('punkt')

adunit = ads.Connection("adunits.db")
addresses = adunit.getAddresses()

# create empty map zoomed in on Seattle
map = folium.Map(location=C.SEATTLE,
                 zoom_start=C.INIT_ZOOM, control_scale=True)


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

map.save("map.html")

# Dashify

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash("SeattleADU",
                external_stylesheets=external_stylesheets)

app.layout = html.Div([

    html.H1("Seattle ADU Feasibility"),
    # navb,
    # html.Div(id='navb'),
    html.H3("Find your home"),
    dcc.Dropdown(
        id='addressDropdown',
        options=[
            {'label': i, 'value': j} for i,j in zip(addresses.address,addresses.PIN)
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
        id='aduPurposeDropdown',
        options=[
            {'label': 'Build one more unit for rental income', 'value': 'income'},
            {'label': 'A Relative needs some housing', 'value': 'support'},
        ],
        value='purposes'
    ),
    # Not intuitively named
    html.Div(id='output_drop'),

    html.H2("Let's do the numbers!",
            style={'textAlign': 'center', 'color': '#7FDBFF'}),


    html.Div([
        html.Div([
            daq.ToggleSwitch(
                id='build_dadu',
                label=['Attached ADU', 'Detached ADU'],
                style={'width': '350px', 'margin': 'auto'},
                value=False),
            html.H3('Cost Breakdown'),
            html.H4('How large will be your ADU?'),
            dcc.Slider(
                id='BuildSizeInput',
                min=0,
                max=1000,
                step=10,
                value=500,),
            html.Div(id='BuildSizeOutput', style={'textAlign': 'center'}),
            html.Table([
                html.Tr([html.Td(['Construction Cost']), html.Td(id='ConstructCost')]),
                html.Tr([html.Td(['+ Sewer Capacity Charge ']), html.Td(id='SewerCharge')]),
                html.Tr([html.Td(['+  Permit Fee']), html.Td(4000)]),
                html.Tr([html.Td(['+  Architecture Fee']), html.Td(id='DesignCost')]),
                html.Tr([html.Td(['=  Estimated Cost']), html.Td(id='TotalCost')])])
        ], className="six columns"),

        html.Div([
            html.H3("How much will you borrow?"),
            dcc.Slider(
                id='LoanInput',
                min=100000,
                max=300000,
                step=5000,
                value=200000,
            ),
            html.Table([
                html.Tr([html.Td(['Total Loan']), html.Td(id='LoanAmount')]),
                html.Tr([html.Td(['Monthly Payment']), html.Td(id='MonthlyPayment')])
            ]),

            dcc.Markdown('''
            Note: We assume APR 6.9% for a 15-year fixed-rate home equity loan.  \
                    Bank typical requires debt-to-income ratio > 30%.  \
                    Loan is likely to be approved if monthly income > 3*payment
            '''),

            html.H3("Where do you live?"),
            dcc.Dropdown(
                id='neighbor_dropdown',
                options=[  # data from zillow 2019/may rent per square foot
                    {'label': 'Ballard', 'value': '3.277945619'},
                    {'label': 'Capitol Hill', 'value': '3.22537112'},
                    {'label': 'Downtown', 'value': '3.861445783'},
                    {'label': 'Fremont', 'value': '3'}, ],
                value='3'),
            html.H3("Expected monthly rental income"),
            html.Div(id='rental'),
        ], className="six columns"),

    ], className="row"),

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

# input slider for square foot
@app.callback(
    Output('BuildSizeOutput', 'children'),
    [Input('BuildSizeInput', 'value')])
def update_output(value):
    return 'Your Future ADU Size: "{}" Square Feet '.format(value)

# calculate cost breakdown
@app.callback(
    [Output('ConstructCost', 'children'),
     Output('SewerCharge', 'children'),
     Output('DesignCost', 'children'),
     Output('TotalCost', 'children')],
    [Input('build_dadu', 'value'),
     Input('BuildSizeInput', 'value')])
def cost_breakdown(value1, value2):
    # 'Total amount of loan is "{0:12,.0f}"'.format(loan)
    return fin.cost_breakdown(value1, value2)

# calculate the rental income
@app.callback(
    Output('rental', 'children'),
    [Input('BuildSizeInput', 'value'),
     Input('neighbor_dropdown', 'value')])
def rents(buildSize, neighbor):
    return float(buildSize)*float(neighbor)


# dynamically updates the map based on the address selected
@app.callback(
    [Output('output-container', 'children'),
     Output('map', 'srcDoc')],
    [Input('addressDropdown', 'value')]
)
def update_map(value, coords=C.SEATTLE, zoom=C.INIT_ZOOM):
    yearbuilt = 1

    if value != None:
        yearbuilt = 1
        adunit = ads.Connection("adunits.db")
        df = adunit.getParcelCoords(value)
        # df.to_csv("df.csv")
        # coords = (newCoords.latitude[0], newCoords.longitude[0])
        coords = (df.coordY[0], df.coordX[0])
        # coords = (df.iloc[0]["coordY"]["coordX"])
        # float max digits is not long enough
        zoom = 18

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

        cols = ['adu_eligible', 's_hood', 'zone_ind', 'sqftlot',
                'ls_indic', 'lotcov_indic', 'lotcoverage', 'sm_lotcov_ind', 'sm_lotcov',
                'yrbuilt', 'daylightbasement', 'sqftfinbasement',  'shoreline_ind',
                'parcel_flood', 'parcel_landf', 'parcel_peat',
                'parcel_poteslide', 'parcel_riparian', 'parcel_steepslope',
                ]
        geojson = df_to_geojson(df, cols, lat='coordX', lon='coordY')

    new_map = folium.Map(location=coords, zoom_start=zoom)

    # with open('myfile.geojson', 'w') as f:
    #     json.dump(geojson, f)

    # with open('myfile2.geojson', 'w') as f2:
    #     geojson.write(f2)
    #     f2.close()
    if value != None:
        # parcel = folium.map.FeatureGroup(name="parcel",
        #                                  overlay=True, control=True, show=True,)

        # for i in range(0, len(geojson["features"])):
        #     print(len(geojson["features"]))
        #     print(i)
        #     print(geojson["features"][i]["geometry"])
        #     feature = folium.features.GeoJson(geojson["features"][i]["geometry"],
        #                                       name=(geojson["features"][i]["properties"]["sqftlot"]),
        #                                       style_function=style_function,
        #                                       highlight_function=highlight_function,)
        #     folium.Popup(
        #                  "Square feet of lot: " + geojson["features"][i]["properties"]["sqftlot"], max_width=200).add_to(feature)
        #     parcel.add_child(feature)

        # parcel = folium.features.GeoJson(geojson, style_function=style_function, highlight_function=highlight_function) #### Anag
        # print(geojson["features"][0]["geometry"])

        # folium.Popup()
        # folium.Marker(coords, popup=folium.Popup("<b><h4>Is this home ADU eligible? </h4></b>" +
        #     str(df.iloc[0]["adu_eligible"]) + "<br><h5><i>Details</i></h5>" +
        #     "<br>Neighborhood: " + str(df.iloc[0]["s_hood"]) +
        #     "<br>Is this a Single Family zoned home? " + str(df.iloc[0]["zone_ind"]) +
        #     "<br>Square feet of lot: " + str(df.iloc[0]["sqftlot"]) +
        #     "<br> ls_indic " + str(df.iloc[0]["ls_indic"]) +
        #     "<br> lotcov_indic " + str(df.iloc[0]["lotcov_indic"]) +
        #     "<br> lotcoverage " + str(df.iloc[0]["lotcoverage"]) +
        #     "<br> sm_lotcov_ind " + str(df.iloc[0]["sm_lotcov_ind"]) +
        #     "<br> sm_lotcov " + str(df.iloc[0]["sm_lotcov"]) +
        #     "<br> Year House Built " + str(df.iloc[0]["yrbuilt"]) +
        #     "<br> Does this home have a daylight basement? " + str(df.iloc[0]["daylightbasement"]) +
        #     "<br> Square foot in basement " + str(df.iloc[0]["sqftfinbasement"]) +
        #     "<br> Does this lot border a shoreline? " + str(df.iloc[0]["shoreline_ind"]) +
        #     "<br><i>Environmentally Critical Areas assessment</i>" +
        #     "<br>Is this parcel on a steep slope? " + str(df.iloc[0]["parcel_steepslope"]) +
        #     "<br>Is this parcel on a previously flooded area? " + str(df.iloc[0]["parcel_flood"]) +
        #     "<br>Is this parcel on a potential slide area? " + str(df.iloc[0]["parcel_poteslide"]),
        #     max_width=2000)
        #     ).add_to(new_map)

        # locations = geojson["features"]["geometry"]["coordinates"]

        locations = np.asarray(df[pd.Index(['coordY', 'coordX'])])
        # print(locations)

        folium.Polygon(locations=locations, color='blue', weight=6, fill_color='red',
                       fill_opacity=0.5, fill=True,
                       popup=folium.Popup("<b><h4>Is this home DADU eligible? </h4></b>" +
                                          str(df.iloc[0]["adu_eligible"]) + "<br><i>Details</i>" +
                                          "<br>Neighborhood: " + str(df.iloc[0]["s_hood"]) +
                                          "<br>Is this a Single Family zoned home? " + str(df.iloc[0]["zone_ind"]) +
                                          "<br>Square feet of lot: " + str(df.iloc[0]["sqftlot"]) +
                                          "<br> Is this lot large enough to house a DADU? " + str(df.iloc[0]["ls_indic"]) +
                                          "<br> For lots bigger than 5000 square feet, is lot coverage sufficient for a DADU? " + str(df.iloc[0]["lotcov_indic"]) +
                                          "<br> For lots bigger than 5000 square feet, what is the lot coverage? " + str(df.iloc[0]["lotcoverage"]) +
                                          "<br> For lots smaller than 5000 square feet, is lot coverage sufficient for a DADU? " + str(df.iloc[0]["sm_lotcov_ind"]) +
                                          "<br> For lots smaller than 5000 square feet, what is the lot coverage? " + str(df.iloc[0]["sm_lotcov"]) +
                                          "<br> Year House Built " + str(df.iloc[0]["yrbuilt"]) +
                                          # "<br> Does this home have a daylight basement? " + str(df.iloc[0]["daylightbasement"]) +
                                          # "<br> Square foot in basement " + str(df.iloc[0]["sqftfinbasement"]) +
                                          "<br> Does this lot border a shoreline? " + str(df.iloc[0]["shoreline_ind"]) +
                                          "<br><i>Environmentally Critical Areas assessment</i>" +
                                          "<br>Is this parcel on a steep slope? " + str(df.iloc[0]["parcel_steepslope"]) +
                                          "<br>Is this parcel on a previously flooded area? " + str(df.iloc[0]["parcel_flood"]) +
                                          "<br>Is this parcel on a potential slide area? " +
                                          str(df.iloc[0]["parcel_poteslide"]),
                                          max_width=2000),
                       tooltip='Click me!',).add_to(new_map)

        # feature = folium.features.GeoJson(geojson["features"]["geometry"],
        #     name=None, style_function=style_function, highlight_function=highlight_function,)
        # folium.Popup("Square feet of lot: " + str(geojson["features"]["properties"]["sqftlot"]), max_width=300).add_to(feature)
        # parcel.add_child(feature)
        # feature.add_to(new_map)

        # parcel.add_to(new_map)

    new_map.save("map.html")
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
     Output(component_id='MonthlyPayment', component_property='children')],
    [Input(component_id='LoanInput', component_property='value'),
     Input(component_id='intermediate-value', component_property='children')]
)
def loan_calculator(loan, feature):
    return fin.loan_calculator(loan, feature)

# print out
@app.callback(
    Output('output_drop', 'children'),
    [Input('aduPurposeDropdown', 'value')])
def update_purpose(value):
    return 'You are builing this ADU for "{}"'.format(value)


if __name__ == '__main__':
    app.run_server(debug=True)
