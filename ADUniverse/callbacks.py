import financials as fin
import update_map as updt
import adusql as ads

from adu_app import app
from constant import SEATTLE, INIT_ZOOM
from dash.dependencies import Input, Output, State
import dash_core_components as dcc

import collections

from common_data import app_data

import pandas as pd


# input slider for square foot

def toggle_modal(n1, n2, is_open):

    # return not is_open
    return is_open


app.callback(
    Output("modalBlog", "is_open"),
    [Input("closeBlog", "n_clicks"), Input("closeBlog", "n_clicks")],
    [State("modalBlog", "is_open")],
)(toggle_modal)


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
    # print("attempted zip ", zp)
    # print("dropdown zipcode ", zipcode)
    if (zipcode is None):
        try:
            format(zipc)
        except NameError:
            return fin.returns(buildSize, format('98105'))
        else:
            print("later zp ", zipc)
            print(type(zipc))
            print(type(float(format(zipc))))
            print(type(buildSize))
            return fin.returns(buildSize, format(zipc))
    else:
        return fin.returns(buildSize, format(zipcode))


# def returns(buildSize, zipcode):
#     return fin.returns(buildSize, str(common_data.zipcode))

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
# def update_page1(value):
#     global df
#     df = pd.DataFrame()
    
#     if value != None:
#         adunit = ads.Connection("adunits.db")
#         df = adunit.getParcelCoords(value)


    # return update_page(outpt)

# calculating loans


@app.callback(
    [Output(component_id='LoanAmount', component_property='children'),
     Output(component_id='MonthlyPayment', component_property='children')],
    [Input(component_id='LoanInput', component_property='value')]
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


