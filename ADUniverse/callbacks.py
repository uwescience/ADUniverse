import financials as fin
import update_map as updt
import adusql as ads

from adu_app import app
from constant import SEATTLE, INIT_ZOOM
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

import collections

from common_data import app_data

import pandas as pd

# def toggle_modal(n1, n2, is_open):
#
#     # return not is_open
#     return is_open
# app.callback(
#     Output("modalBlog", "is_open"),
#     [Input("closeBlog", "n_clicks"), Input("closeBlog", "n_clicks")],
#     [State("modalBlog", "is_open")],
# )(toggle_modal)

# input slider for square foot


@app.callback(
    Output('BuildSizeOutput', 'children'),
    [Input('BuildSizeInput', 'value')])
def update_output(value):
    return 'Your Future ADU Size: "{}" Square Feet '.format(value)

# calculate cost breakdown


@app.callback(
    [Output('ConstructCost', 'children'),
     Output('Tax', 'children'),
     Output('SewerCharge', 'children'),
     Output('PermitFee', 'children'),
     Output('DesignCost', 'children'),
     Output('TotalCost', 'children'),
     Output('PropertyTax', 'children')],
    [Input('build_dadu', 'value'),
     Input('BuildSizeInput', 'value')])
def cost_breakdown(value1, value2):
    return fin.cost_breakdown(value1, value2)

# calculate the returns(rental + value added)

# Zipcode is changed

# Checks to see first if you got anything from zipcode dropdown
# If there's nothing, next it checks if anything came out of address dropdown
# If nothing there either, it feeds a default value to fin functions
# If something there, it uses the map address zipcode
# User can override map zip with self-selected zip


@app.callback(
    [Output('rental', 'children'),
     Output('sales', 'children')],
    [Input('BuildSizeInput', 'value'),
     Input('zipcode', 'value')])
def returns(buildSize, zipcode):
    if (zipcode is None):
        try:
            format(zipc)
        except NameError:
            return fin.returns(buildSize, format('98105'))
        else:
            return fin.returns(buildSize, format(zipc))

    else:
        return fin.returns(buildSize, format(zipcode))


# dynamically updates the map based on the address selected


# @app.callback(
#     Output('map', 'srcDoc'),
#     [Input('addressDropdown', 'value')]
# )
def update_map(df, neighbors, coords=SEATTLE, zoom=INIT_ZOOM):
    # global df
    # df = pd.DataFrame()
    # global neighbors
    # neighbors = pd.DataFrame()
    # if value != None:
    #     print("True")
    #     adunit = ads.Connection("adunits.db")
    #     df = adunit.getParcelCoords(value)
    #     df.to_csv("df.csv")
    #     neighbors = adunit.getNeighbors(value)

    return updt.update_map(df, neighbors, coords=coords, zoom=zoom)


# @app.callback(
#     Output('eligibilityDetails', 'children'),
#     [Input('addressDropdown', 'value')]
# )
<< << << < HEAD
# def update_page1(value):
#     global df
#     df = pd.DataFrame()

#     if value != None:
#         adunit = ads.Connection("adunits.db")
#         df = adunit.getParcelCoords(value)

# return update_page(outpt)
== == == =


def update_page1(df):

    if not df.empty:
        output = html.Div([
            html.H4("Eligibility Details", style={'textAlign': 'center'}),
            html.Div([html.Div(["Zoning"], style={'textAlign': 'center'}),
                      html.Div(
                          ["Your home must be in a single family lot to build an AADU or DADU"], style={}),
                      html.Div(["Your home qualifies!/does not qualify :("], style={}),

                      ], style={'border': '2px solid #4C3C1B', 'font-size': '12px', 'font-family': 'Arial',
                                'padding': '12px', 'border-width': 'thin', 'border-radius': '5px'}),
            html.Div([html.Div(["Lot Size"], style={'textAlign': 'center'}),
                      html.Div(["Your home must be at least __ for a DADU"], style={}),
                      html.Div(["Your home qualifies!/does not qualify :("], style={}),

                      ], style={'border': '2px solid #4C3C1B', 'background-color': '#EFEECB',
                                'padding': '10px', 'border-width': 'thin', 'border-radius': '5px',
                                'font-size': '12px', 'font-family': 'Arial', }),
            html.Div([html.Div(["Lot Coverage"], style={'textAlign': 'center'}),
                      html.Div(["Your home must be at least __ for a DADU"], style={}),
                      html.Div(["Your home qualifies!/does not qualify :("], style={}),
                      ], style={'border': '2px solid #4C3C1B',
                                'padding': '10px', 'border-width': 'thin', 'border-radius': '5px',
                                'font-size': '12px', 'font-family': 'Arial', }),
            html.Div([html.Div(["Shoreline"], style={'textAlign': 'center'}),
                      html.Div(
                          ["Your home must not border a shoreline to build an AADU or a DADU"], style={}),
                      html.Div(["Your home qualifies!/does not qualify :("], style={}),
                      ], style={'border': '2px solid #4C3C1B', 'background-color': '#EFEECB',
                                'padding': '10px', 'border-width': 'thin', 'border-radius': '5px',
                                'font-size': '12px', 'font-family': 'Arial', }),

            html.Div("Want even more information? Please see the Transparency section for more details on these terms", style={
                'textAlign': 'center'}),
        ])

    return output


>>>>>> > f3a4163555d1e82d276c9622eff2005870d82601

# calculating loans


@app.callback(
    [Output('LoanAmount', 'children'),
     Output('MonthlyPayment', 'children')],
    [Input('LoanInput', 'value')]
)
def loan_calculator(loan):
    return fin.loan_calculator(loan)


# @app.callback(
#     Output('showDets', 'children'),
#     [Input('addressDropdown', 'value')])
# def show_eligDetails(PIN):
#     return 0

# # find out if neighbor has an adu and where


# @app.callback(
#     Output('adu_around', 'children'),
#     [Input('addressDropdown', 'value')])
def neighbor_adu(PIN, df, neighbors):
    return fin.neighbor_adu(PIN, df, neighbors)


# @app.callback(
#     Output('next_page', 'children'),
#     [Input('addressDropdown', 'value')])
def show_new_page(PIN):
    if PIN != None:
        return dcc.Link("Figure out your financial options on the next page", href='/finances')


# Zip code lookup
# @app.callback(
#     Output('zip_code', 'children'),
#     [Input('addressDropdown', 'value')])
def update_zipcode(value):  #
    # if value != None:
        # adunit = ads.Connection("adunits.db")
        # zp_data = adunit.getZipcode(value)

    if value == None:
        return "Type your address first"
    else:
        # global zp
        # zp = zp_data.loc[0, 'zipcode']
        # print("original zp ", zp)
        # print(type(zp))
        # app_data.zipcode = zp
        # print("original app_data zp ", app_data.zipcode)
        # # common_data.change(zp)
        return 'Your zipcode is {}'.format(value)
    # else:
    #     return "Type your address first"


def default_zipcode(value):
    if value != None:
        return str(value)

# Master Callback!


@app.callback(
    [
        Output('map', 'srcDoc'),
        Output('zip_code', 'children'),
        #    Output('eligibilityDetails', 'children'),
        Output('adu_around', 'children'),
        Output('next_page', 'children')
    ],
    [Input('addressDropdown', 'value')])
def master_callback(value):
    df = pd.DataFrame()
    neighbors = pd.DataFrame()
    global zipc
    zipc = None
    if value != None:
        adunit = ads.Connection("adunits.db")
        df = adunit.getParcelCoords(value)
        df.to_csv("df.csv")
        neighbors = adunit.getNeighbors(df)
        neighbors.to_csv("neighbors.csv")
        zipc = df.iloc[0]["zipcode"]
    return [
        update_map(df, neighbors, coords=SEATTLE, zoom=INIT_ZOOM),
        update_zipcode(zipc),
        #        update_page1(value),
        neighbor_adu(value, df, neighbors),
        show_new_page(value)
    ]
