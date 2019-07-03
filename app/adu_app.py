import folium
import pandas as pd

import json
import sys

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

FILE = "Seattle_Real_Time_Fire_911_Calls.csv"
SEATTLE_COORDINATES = (47.6062, -122.3321)
zoom_start = 12
data = pd.read_csv(FILE)

# for speed purposes
MAX_RECORDS = 10

# create empty map zoomed in on San Francisco
map = folium.Map(location=SEATTLE_COORDINATES, zoom_start=zoom_start, control_scale=True)

# add neighborhoods on top of this. This is an experiment to be replaced with a polygon geojson
geo_json_data = json.load(open('neighborhoods.geojson'))
# folium.GeoJson(geo_json_data).add_to(map)

# regular style of polygons
def style_function(feature):
    return {
        'weight' : 2,
        'dashArray' : '5, 5',
        'fillOpacity' : 0,
        'lineOpacity' : 1,
    }

def highlight_function(feature):
    return {
        'fillColor' : 'blue',
        'weight' : 2,
        'lineColor' : 'black',
        'lineWeight' : 2,
        'dashArray' : '5, 5',
        'fillOpacity' : 0.5,
        'lineOpacity' : 1,
    }


# apply the neighborhood outlines to the map
folium.GeoJson(geo_json_data,
              style_function=style_function,
              highlight_function=highlight_function,
              ).add_to(map)

# print(geo_json_data[1,:])
geo_json_data_df = pd.DataFrame.from_dict(geo_json_data)

# add a marker for every record in the filtered data, use a clustered view
# for _, row in geo_json_data['features']:
#     for i in row['properties']:
#         popup = folium.Popup(i['name'])
#     # c.add_to(map)
map.save("map.html")

# Dashify

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash("SeattleADU",
                external_stylesheets=external_stylesheets)

# app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

# app.layout = html.Div([
#     html.H1("Seattle ADU Feasibility"),
#     html.Iframe(id='map', srcDoc=open("map.html", "r").read(),
#                 width="90%", height="400"),
#     html.H3("Lot Size"),
#     dcc.Slider(
#         id='my-range-slider',
#         min=1000,
#         max=20000,
#         step=100,
#         value=4000
#     ),
#     html.Div(id='output-container-range-slider'),
#     # html.Iframe(id="parent", srcDoc=html_frames, width="100%",
#     #    height="600"),
#     # html.Iframe(id='map', srcDoc=open("map.html", "r").read(),
#     #    width="100%", height="600")
# ])

# Dropdown for given cities
# app.layout = html.Div([
#     html.H1("Seattle ADU Feasibility"),
#     html.Iframe(id='map', srcDoc=open("map.html", "r").read(),
#                 width="90%", height="400"),
#     html.H3("Find your home"),
#     dcc.Dropdown(
#         id='my-dropdown',
#         options=[
#             {'label': 'New York City', 'value': 'NYC'},
#             {'label': 'Montreal', 'value': 'MTL'},
#             {'label': 'San Francisco', 'value': 'SF'}
#         ],
#         value='SF'
#     ),
#     html.Div(id='output-container')
# ])

# Dropdown base on the dataframe


# def generate_table(data, MAX_RECORDS):
#     return html.Table(
#         # Header
#         [html.Tr([html.Th(col) for col in data.Address])] +
#         # Body
#         [html.Tr([
#             html.Td(data.iloc[i][col]) for col in data.Address
#         ]) for i in range(min(len(data), MAX_RECORDS))]
#     )


app.layout = html.Div([
    html.H1("Seattle ADU Feasibility"),
    html.Iframe(id='map', srcDoc=open("map.html", "r").read(),
                width="100%", height="550"),
    html.H3("Find your home"),
    dcc.Dropdown(
        id='my-dropdown',

        options=[
            {'label': i, 'value': i} for i in data.Address.unique()
        ],
        placeholder='Filter by address...'),
    html.Div(id='output-container'),

    dcc.Input(id='my-id', value='initial value', type='text'),
    html.Div(id='my-div'),
    dcc.Markdown('''

    # **Frequently Asked Questions**

    # How to be a good landloard?

    here are some useful information.

    [Rental Housing Association of Washington](https://www.rhawa.org/)

    # More financial information?

    here are the home equity loan informations

    *Disclaimer: We help to gether useful informtions to facilitate your decisions *

    '''),
])


@app.callback(
    # dash.dependencies.Output('output-container-range-slider', 'children'),
    dash.dependencies.Output('output-container', 'children'),
    [dash.dependencies.Input('my-dropdown', 'value')]
)
# [dash.dependencies.Input('my-range-slider', 'value')])
def update_output(value):
    return 'You have selected "{}"'.format(value)
# def display_table(dropdown_value):
#     # import pdb
#     # pdb.set_trace()
#     if dropdown_value is None:
#         return generate_table(data, MAX_RECORDS)
#
#     dff = data[data.Address.str.contains('|'.join(dropdown_value))]
#     return generate_table(dff, MAX_RECORDS)


@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='my-id', component_property='value')]
)
def update_output_div(input_value):
    return 'You\'ve entered "{}" for lot size'.format(input_value)


# app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})


if __name__ == '__main__':
    app.run_server(debug=True)
