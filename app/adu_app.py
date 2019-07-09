import pandas as pd



import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import make_map as make

make.make_map()

FILE = "Seattle_Real_Time_Fire_911_Calls.csv"
SEATTLE_COORDINATES = (47.6062, -122.3321)
zoom_start = 12
data = pd.read_csv(FILE)

# for speed purposes
MAX_RECORDS = 10


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

    # html.Div(id='intermediate-value', style={'display': 'none'}),
    html.Div(id='intermediate-value'),

    html.Div(id='output-container'),

    html.H3("tell me your lot size"),
    dcc.Input(id='my-id', value='initial value', type='number'),  # text
    # html.Div(id='my-div'),
    html.Table([
        html.Tr([html.Td(['lot_size']), html.Td(id='my-div')]),
        # html.Tr([html.Td(['intermediate']), html.Td(id='intermediate-value')]),
        html.Tr([html.Td(['ADU score']), html.Td(id='calculation')]),
    ]),

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
    dash.dependencies.Output('intermediate-value', 'children'),
    [dash.dependencies.Input('my-dropdown', 'value')]
)
def clean_data(value):
    # some expensive clean data step
    dff = data.loc[data['Address'] == value].head(1)
    cleaned_df = dff["Random Number"]

    # more generally, this line would be
    # json.dumps(cleaned_df)
    # return dff
    return cleaned_df.to_json(orient='split')
    # return cleaned_df.to_json(orient='values')
    # return 'You have selected_random number "{}"'.format(dff)


@app.callback(
    # dash.dependencies.Output('output-container-range-slider', 'children'),
    dash.dependencies.Output('output-container', 'children'),
    [dash.dependencies.Input('my-dropdown', 'value')]
)
# [dash.dependencies.Input('my-range-slider', 'value')])
def update_output(value):
    # dff = data[data.Address.str.contains('|'.join(value))]
    dff = data.loc[data['Address'] == value].head(1)
    dff = dff["Random Number"].values
    return 'You have selected_random number "{}"'.format(dff)
# def display_table(dropdown_value):
#     # import pdb
#     # pdb.set_trace()
#     if dropdown_value is None:
#         return generate_table(data, MAX_RECORDS)
#
#     dff = data[data.Address.str.contains('|'.join(dropdown_value))]
#     return generate_table(dff, MAX_RECORDS)


@app.callback(
    [Output(component_id='my-div', component_property='children'),
     Output(component_id='calculation', component_property='children')],
    [Input(component_id='my-id', component_property='value'),
     Input(component_id='intermediate-value', component_property='children')]
)
def update_output_div(input_value, json):  # orient='index'
    aux = pd.read_json(json, orient='values').values[0][1]
    # aux = pd.read_json(json, orient='values').iloc[0].values
    # aux = pd.read_json(json, orient='values')
    return 'You\'ve entered "{}" for lot size'.format(input_value), aux*input_value


# app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

# Anagha
# @app.callback(Output('output-keypress', 'children'),
#               [Input('input-1-keypress', 'value'),
#                Input('input-2-keypress', 'value')])
# def update_output(input1, input2):
#     return u'Input 1 is "{}" and Input 2 is "{}"'.format(input1, input2)



if __name__ == '__main__':
    app.run_server(debug=True)
