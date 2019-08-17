import financials as fin
import update_map as updt
import adusql as ads
import numpy as np

from adu_app import app
from constant import SEATTLE, INIT_ZOOM
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

import collections

from common_data import app_data

import pandas as pd


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

def update_map(df, neighbors, coords=SEATTLE, zoom=INIT_ZOOM):
    return updt.update_map(df, neighbors, coords=coords, zoom=zoom)


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
                      html.Div(value1), ], className='white-box yellow-box'),
            html.Div([html.Div(["Lot Size"], style={'textAlign': 'center'}),
                      html.Div([" Your lot must be at least 3200 square feet for a DADU"]),
                      html.Div(value2)], className='white-box yellow-box'),
            html.Div([html.Div(["Lot Coverage"], style={'textAlign': 'center'}),
                      html.Div(["If lot is larger than 5000 feet, no more than 35% \
                should be covered. If lot is smaller, no more than 1000 plus 15% should be covered."], style={}),
                      html.Div(value3)], className='white-box yellow-box'),
            html.Div([html.Div(["Shoreline"], style={'textAlign': 'center'}),
                      html.Div(["Your home must not border a shoreline to build a DADU"]),
                      html.Div(value4)], className='white-box yellow-box'),
            html.Div([html.Div(["Existing ADUs"], style={'textAlign': 'center'}),
                      html.Div(["You may build upto 2 ADUs on a single property"]),
                      html.Div(value_adu)], className='white-box yellow-box'),

            html.Div("Want even more information? Please see the Transparency \
                section for more details on these terms", style={
                'textAlign': 'center'}),
        ])

    return output


def update_details(df):
    if (df.iloc[0]["zone_ind"] == 1):
        value_alley = value_basement = value_bus = value_corner = None
        value_tree = value_sewer = value_lock = value_age = None
        value_eca = ""

        if (df.iloc[0]["alley_lot"] == 1):
            value_alley = html.Div([dcc.Markdown("Your home in on a lot **neighboring an alley**. Renters, being able to enter through \
            a separate entrance, would consider this advantageous.")], className='white-box green-box')

        # if (df.iloc[0]["corner_lot"] == 1)

        if (not pd.isna(df.iloc[0]["sqftfinbasement"])):
            value_basement = html.Div(["You have a sizable finished basement that could be converted to an AADU."], id="basement", className='white-box green-box')
            if (df.iloc[0]["daylightbasement"]):
                value_basement.children.append("A daylight basement in particular can be quite attractive to renters.")
            # unfinished
            # add finished
            # add daylight
            # garage + grade

        if (not pd.isna(df.iloc[0]["miles_nearest_bus"]) == 1):
            value_bus = html.Div([dcc.Markdown("Your home is near a **frequent transit stop**, making it attractive \
                to renters of AADUs and DADUs.")], className='white-box green-box')

        #Negative stuff
        if (df.iloc[0]["yrbuilt"] < 1959):
            value_age = html.Div(["Because your home may be relatively old, if you wish to build an AADU, you may need to find an inspector to ensure no additional changes need to be made to your property."], className='white-box red-box')

        if (df.iloc[0]["treecanopy_prct"] > 30):
            value_tree = html.Div([
                dcc.Markdown("Based upon the amount of **tree canopy** in your rear yard the location and size of a detached \
                accessory dwelling unit may be limited.  You should consult with a design professional or a land use coach \
                at the applicant services center (link).  Information regarding the city’s tree protection ordinance can be found here (link).")], className='white-box red-box') ## soft red?

        if (df.iloc[0]["parcel_steepslope"] == 1):
            value_eca += "Steep slopes; "
        if (df.iloc[0]["parcel_flood"] == 1):
            value_eca += "Flood prone areas; "
        if (df.iloc[0]["parcel_poteslide"] == 1):
            value_eca += "Potential slide area; "
        if (df.iloc[0]["parcel_landf"] == 1):
            value_eca += "On or close to a landfill; "
        if (df.iloc[0]["parcel_peat"] == 1):
            value_eca += "Peat settlements; "
        if (df.iloc[0]["parcel_riparian"] == 1):
            value_eca += "Riparian corridor; "

        if (df.iloc[0]["side_sewer_conflict"] == 1):
            value_sewer = html.Div([dcc.Markdown("Your home has a **conflicting side sewer** crossing \
                another lot. You may need to reroute or construct a new side sewer \
                for a DADU. Additionally, being a landlocked parcel, you may have \
                to run a new side sewer through another's lot while constructing an ADU. \
                You may need to talk to your neighbor about your options.")], className='white-box red-box')
        else:
            if (df.iloc[0]["intersecting_sewer"] == 1):
                value_sewer = html.Div([dcc.Markdown("Your home has a **side sewer** that crosses another lot. \
                    You may need to reroute or construct a new side sewer for a DADU")], className='white-box')
                #
            if (df.iloc[0]["landlocked_parcel"] == 1):
                value_lock = html.Div([dcc.Markdown("Being a **landlocked parcel**, you may have to \
                    run a new side sewer through another's lot while constructing an ADU. \
                    You may need to talk to your neighbor about your options")], className='white-box')

        if not df.empty:
            output = html.Div([
                html.H5("Other potential considerations for your lot:", style={'textAlign': 'center'}),
                value_age,
                value_alley, value_basement, value_bus, value_corner, value_lock,
                html.Div([html.Div(["Environmentally Critical Areas"], style={'textAlign': 'center'}),
                          html.Div([dcc.Markdown("Your parcel lies on the following **environmentally critical areas** that \
                    may make it more costly to permit and build a DADU: (If list empty, there are none)")]),
                          value_eca], className='white-box red-box'),
                value_sewer,
                value_tree,

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


def neighbor_adu(PIN, df, neighbors):
    return fin.neighbor_adu(PIN, df, neighbors)

def show_new_page(PIN):
    if PIN != None:
        return dcc.Link("Figure out your financial options on the next page", href='/finances')


# Zip code lookup
def update_zipcode(value):  #

    if value == None:
        return "Type your address first"
    else:
        return 'Your zipcode is {}'.format(value)



# Master Callback!
@app.callback(
    [
        Output('map', 'srcDoc'),
        Output('eligibilityDetails', 'children'),
        Output('addDetails', 'children'),
        Output('adu_around', 'children'),
        Output('next_page', 'children'),
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
        update_criteria_details(df),
        update_details(df),
        neighbor_adu(value, df, neighbors),
        show_new_page(value),
    ]

# try dynamically change dataset


# global SQFTLOT
SQFTLOT = 1000

# FIXME this is the wrong callbacks


# @app.callback(
#     Output('demo_output', 'children'),
#     [Input('demo', 'value')])
# def demo_activation(value):
#     SQFTLOT = float(np.array([value]).astype(int))*1000 + \
#         (1-float(np.array([value]).astype(int)))*5000
#     return SQFTLOT

# print the zipcode currently in the system


@app.callback(
    Output('ZipcodeOutput', 'children'),
    [Input('zipcode', 'value')])
def print_zipcode(value):
    return 'Calculating gains for zipcode: "{}" '.format(value)
