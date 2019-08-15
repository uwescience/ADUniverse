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

def update_criteria_details(df):

    if (df.iloc[0]["zone_ind"] == 0):
        value1 = "Your home does not qualify."
    else:
        value1 = "Your home qualifies!"

    if (df.iloc[0]["ls_indic"] == 0):
        value2 = "Your lot is {} and therefore does not qualify.".format(df.iloc[0]["sqftlot"])
    else:
        value2 = "Your lot is {} square feet and therefore qualifies!".format(df.iloc[0]["sqftlot"])

    if (df.iloc[0]["sqftlot"] >= 5000):
        if (df.iloc[0]["lotcoverage"] <= 0.35):
            value3 = "Your {} square foot lot with a lot coverage of {:0.2f}% qualifies!".format(
                df.iloc[0]["sqftlot"], 100*df.iloc[0]["lotcoverage"])
        else:
            value3 = "Your {} square foot lot with a lot coverage of {:0.2f}% does not qualify.".format(
                df.iloc[0]["sqftlot"], 100*df.iloc[0]["lotcoverage"])
    else:
        if (df.iloc[0]["lotcoverage"] <= df.iloc[0]["sm_lotcov"]):
            value3 = "Your {} square foot lot with a lot coverage of {:0.2f}% is less than the threshold of {} \
                and therefore qualifies!".format(df.iloc[0]["sqftlot"], 100*df.iloc[0]["lotcoverage"], df.iloc[0]["sm_lotcov"])
        else:
            value3 = "Your {} square foot lot with a lot coverage of {:0.2f}% is greater than the threshold of {} \
             and therefore does not qualify.".format(df.iloc[0]["sqftlot"], 100*df.iloc[0]["lotcoverage"], df.iloc[0]["sm_lotcov"])

    if (df.iloc[0]["shoreline_ind"] == 1):
        value4 = "Your lot borders a shoreline. Unfortunately, no DADU can be built here."
    else:
        value4 = "Your lot does not border a shoreline. You are good to go."

    if (not pd.isna(df.iloc[0]["ADU"])):
        value_adu = "There is already at least one existing ADU on this \
        property. You may build upto one more."
    else:
        value_adu = "There are no existing ADUs on this property. You are good to go."

    if not df.empty:
        output = html.Div([
            html.H4("Core Eligibility Details", style={'textAlign': 'center'}),
            html.Div([html.Div(["Zoning"], style={'textAlign': 'center'}),
                      html.Div(["Your home must be in a single family lot to build an AADU or DADU"]),
                      html.Div(value1), ], className='white-box'),
            html.Div([html.Div(["Lot Size"], style={'textAlign': 'center'}),
                      html.Div([" Your lot must be at least 3200 square feet for a DADU"]),
                      html.Div(value2)], className='white-box yellow-box'),
            html.Div([html.Div(["Lot Coverage"], style={'textAlign': 'center'}),
                      html.Div(["If lot is larger than 5000 feet, no more than 35% \
                should be covered. If lot is smaller, no more than 1000 plus 15% should be covered."], style={}),
                      html.Div(value3)], className='white-box'),
            html.Div([html.Div(["Shoreline"], style={'textAlign': 'center'}),
                      html.Div(["Your home must not border a shoreline to build a DADU"]),
                      html.Div(value4)], className='white-box yellow-box'),
            html.Div([html.Div(["Existing ADUs"], style={'textAlign': 'center'}),
                      html.Div(["You may build upto 2 ADUs on a single property"]),
                      html.Div(value_adu)], className='white-box'),

            html.Div("Want even more information? Please see the Transparency \
                section for more details on these terms", style={
                'textAlign': 'center'}),
        ])

    return output


def update_advantage_details(df):
    if (df.iloc[0]["zone_ind"] == 1):
        value1 = value2 = value3 = value4 = value5 = value6 = None
        if (df.iloc[0]["alley_lot"] == 1):
            value1 = html.Div(["Your home in on a lot neighboring an alley. Renters, being able to enter through \
            a separate entrance, would consider this advantageous."], className='white-box')

        # if (df.iloc[0]["corner_lot"] == 1)

        if (not pd.isna(df.iloc[0]["sqftfinbasement"])):
            value2 = html.Div(["You have a sizable basement that could be converted to an AADU. \
                It is a finished basement r home in on a lot neighboring an alley. Renters, being able to enter through \
            a separate entrance, would consider this advantageous."], className='white-box')
            # Basement (presence, size, year built, finished/unfinished, daylight) ## GARAGES

        if (not pd.isna(df.iloc[0]["miles_nearest_bus"]) == 1):
            value3 = html.Div(["Your home is near a frequent transit stop, making it attractive \
                to renters of AADUs and DADUs."], className='white-box')

        if not df.empty:
            output = html.Div([
                html.H5("Here are potential advantages of your lot", style={'textAlign': 'center'}),
                value1, value2, value3, value4, value5, value6,
            ])
        return output


def update_dis_details(df):
    if (df.iloc[0]["zone_ind"] == 1):
        value1 = value3 = value4 = None
        value2 = ""
            # Year built? Before 1950s????? find an inspector 1959 # could change
            # Size of house? 


        if (df.iloc[0]["treecanopy_prct"] > 30):
            value1 = html.Div(
                ["Your home may have significant tree canopy cover that may restrict your ability to build a DADU"], className='white-box')

        if (df.iloc[0]["parcel_steepslope"] == 1):
            value2 += "Steep slopes; "
        if (df.iloc[0]["parcel_flood"] == 1):
            value2 += "Flood prone areas; "
        if (df.iloc[0]["parcel_poteslide"] == 1):
            value2 += "Potential slide area; "
        if (df.iloc[0]["parcel_landf"] == 1):
            value2 += "On or close to a landfill; "
        if (df.iloc[0]["parcel_peat"] == 1):
            value2 += "Peat settlements; "
        if (df.iloc[0]["parcel_riparian"] == 1):
            value2 += "Riparian corridor; "

        if (df.iloc[0]["side_sewer_conflict"] == 1):
            value3 = html.Div(["Your home has a conflicting side sewer crossing \
                another lot. You may need to reroute or construct a new side sewer \
                for a DADU. Additionally, being a landlocked parcel, you may have \
                to run a new side sewer through another's lot while constructing an ADU. \
                You may need to talk to your neighbor about your options."], className='white-box')
        else:
            if (df.iloc[0]["intersecting_sewer"] == 1):
                value3 = html.Div(["Your home has a side sewer that crosses another lot. \
                    You may need to reroute or construct a new side sewer for a DADU"], className='white-box')
                # 
            if (df.iloc[0]["landlocked_parcel"] == 1):
                value4 = html.Div(["Being a landlocked parcel, you may have to \
                    run a new side sewer through another's lot while constructing an ADU. \
                    You may need to talk to your neighbor about your options"], className='white-box')

            # Landfills?
        if not df.empty:
            output = html.Div([
                html.H5("Here are potential disadvantages of your lot",
                        style={'textAlign': 'center'}),
                value1,
                html.Div([html.Div(["Environmentally Critical Areas"], style={'textAlign': 'center'}),
                          html.Div(["Your parcel lies on the following environmentally critical areas that \
                    may make it more costly to permit and build a DADU: (If list empty, there are none)"]),
                          value2], className='white-box'),
                value3,
                value4,
            ])

        return output


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
        #Output('zip_code', 'children'),
        Output('eligibilityDetails', 'children'),
        Output('addGoodDetails', 'children'),
        Output('addBadDetails', 'children'),
        Output('adu_around', 'children'),
        Output('next_page', 'children'),
        #Output('zipcode', 'label')
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
        # update_zipcode(zipc),
        update_criteria_details(df),
        update_advantage_details(df),
        update_dis_details(df),
        neighbor_adu(value, df, neighbors),
        show_new_page(value),
        # default_zipcode(zipc)
    ]
