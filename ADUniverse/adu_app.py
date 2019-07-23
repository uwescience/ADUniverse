import update_map as update
import adusql as ads
import constant as C
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq  # requires dash_daq version 0.1.0
import folium
import financials as fin
import numpy as np
import pandas as pd
import sys

from dash.dependencies import Input, Output, State
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
            {'label': i, 'value': j} for i, j in zip(addresses.address, addresses.PIN)
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
                marks={
                    250: '250 SF (Studio)',
                    500: '500 SF (1 Bed)',
                    750: '750 SF (2 Bed)',
                },
                value=500,),
            html.H2("  "),
            html.Div(id='BuildSizeOutput', style={'textAlign': 'center'}),
            html.Table([
                html.Tr([html.Td(['Construction Cost']), html.Td(id='ConstructCost')]),
                html.Tr([html.Td(['+ Sewer Capacity Charge ']), html.Td(id='SewerCharge')]),
                html.Tr([html.Td(['+  Permit Fee']), html.Td("4,000")]),
                html.Tr([html.Td(['+  Architecture Fee']), html.Td(id='DesignCost')]),
                html.Tr([html.Td(['=  Estimated Cost']), html.Td(id='TotalCost')])])
        ], className="six columns"),

        html.Div([
            html.H3("How much will you borrow?"),
            dcc.Slider(
                id='LoanInput',
                min=100000,
                max=500000,
                step=5000,
                marks={
                    150000: '150 K',
                    300000: '300 K',
                    450000: '450 K',
                },
                value=150000,
            ),
            html.Table([
                html.Tr([html.Td(['Total Loan']), html.Td(id='LoanAmount')]),
                html.Tr([html.Td(['Monthly Payment']), html.Td(id='MonthlyPayment')])
            ]),

            dcc.Markdown('''Assumptions:
            APR 6.9% for a 15-year fixed-rate home equity loan.
            Bank typical requires debt-to-income ratio > 30%.
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
            dcc.Markdown('''
            Be part of the [Solution for Affordable Housing Crisis!](https://www.seattlehousing.org/housing/housing-choice-vouchers/landlords)
            '''),
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
    return '{0:4,.0f}'.format(float(buildSize)*float(neighbor))


# dynamically updates the map based on the address selected
@app.callback(
    [Output('output-container', 'children'),
     Output('map', 'srcDoc')],
    [Input('addressDropdown', 'value')]
)
def update_map(value, coords=C.SEATTLE, zoom=C.INIT_ZOOM):
    return update.update_map(value, coords=coords, zoom=zoom)

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
