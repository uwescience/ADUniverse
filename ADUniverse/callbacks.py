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
        value1 = "Your home is not eligible."
    else:
        value1 = "Your home is eligible."

    if (df.iloc[0]["ls_indic"] == 0):
        value2 = "Your lot is {} and therefore is not eligible for a DADU.".format(df.iloc[0]["sqftlot"])
    else:
        value2 = "Your lot is {} square feet and therefore is eligible for a DADU".format(df.iloc[0]["sqftlot"])

    if (df.iloc[0]["lot_dim_indic"] == "no"):
        value5 = "Your lot's width is {} and depth is {} and therefore does not qualify.".format(df.iloc[0]["lot_width"], df.iloc[0]["lot_depth"])
    else:
        value5 = "Your lot's width is {} and depth is {} and therefore qualifies!".format(df.iloc[0]["lot_width"], df.iloc[0]["lot_depth"])

    if (df.iloc[0]["sqftlot"] >= 5000):
        if (df.iloc[0]["lotcoverage"] <= 0.35):
            value3 = "Your {}-square-foot lot has an estimated lot coverage of {:0.2f}%. Therefore it is eligible for a DADU.".format(
                df.iloc[0]["sqftlot"], 100*df.iloc[0]["lotcoverage"])
        else:
            value3 = "Your {}-square-foot lot has an estimated lot coverage of {:0.2f}%. Therefore it is not eligible for a DADU.".format(
                df.iloc[0]["sqftlot"], 100*df.iloc[0]["lotcoverage"])
    else:
        if (df.iloc[0]["lotcoverage"] <= df.iloc[0]["sm_lotcov"]):
            value3 = "Your {}-square-foot lot has an estimated lot coverage of {:0.2f}%, less than the threshold of {} \
                and therefore is eligible for a DADU".format(df.iloc[0]["sqftlot"], 100*df.iloc[0]["lotcoverage"], df.iloc[0]["sm_lotcov"])
        else:
            value3 = "Your {}-square-foot lot has an estimated lot coverage of {:0.2f}%, greater than the threshold of {} \
             and therefore is eligible for a DADU.".format(df.iloc[0]["sqftlot"], 100*df.iloc[0]["lotcoverage"], df.iloc[0]["sm_lotcov"])

    if (df.iloc[0]["shoreline_ind"] == 1):
        value4 = "Your lot is located within 200 feet of a designated shoreline (i.e., in the Shoreline District). DADUs are not allowed on lots in the Shoreline District."
    else:
        value4 = "Your lot is not located in the Shoreline District, an area where DADUs are not allowed. Therefore your lot is eligible."

    if (not pd.isna(df.iloc[0]["ADU"])):
        value_adu = "At least one ADU already exists on this \
        property. A lot may have up to two ADUs, so you may add at least one more."
    else:
        value_adu = "No ADUs currently exist on this property."

    if not df.empty:
        output = html.Div([
            html.H4("Core Eligibility Details", style={'textAlign': 'center'}),
            html.Div([html.Div(["Zoning"], style={'textAlign': 'center'}),
                      html.Div(["Your lot must be in a single-family zone to build an AADU or DADU"]),
                      html.Div(value1), ], className='white-box'),
            html.Div([html.Div(["Lot Size"], style={'textAlign': 'center'}),
                      html.Div(["Your lot must be at least 3,200 square feet in area to have a DADU"]),
                      html.Div(value2)], className='white-box'),
            html.Div([html.Div(["Lot Dimensions"], style={'textAlign': 'center'}),
                      html.Div(["Your lot must be at least 25 feet wide and 70 feet deep for a DADU"]),
                      html.Div(value5)], className='white-box'),
            html.Div([html.Div(["Lot Coverage"], style={'textAlign': 'center'}),
                      html.Div(["If lot is larger than 5000 feet, no more than 35% \
                should be covered. If lot is smaller, no more than 1000 plus 15% should be covered."], style={}),
                      html.Div(value3)], className='white-box'),
            html.Div([html.Div(["Shoreline"], style={'textAlign': 'center'}),
                      html.Div(["Your home must not be located within the Shoreline District to be eligible for a DADU"]),
                      html.Div(value4)], className='white-box'),
            html.Div([html.Div(["Existing ADUs"], style={'textAlign': 'center'}),
                      html.Div(["A lot may have up two ADUs"]),
                      html.Div(value_adu)], className='white-box'),

            html.Div("Want even more information? Please see the Transparency \
                section for more details on these terms", style={
                'textAlign': 'center'}),
            dcc.Link("Explore the financial implications of creating an ADU on the next page", href='/finances')
        ])

    return output


def update_details(df):
    if (df.iloc[0]["zone_ind"] == 1):
        value_alley = value_basement = value_garage = value_bus = value_corner = None
        value_tree = value_sewer = value_lock = value_age = None
        value_eca = ""

        if (df.iloc[0]["alley_lot"] == 1):
            value_alley = html.Div([dcc.Markdown("Your home in on a lot **neighboring an alley**. Renters, being able to enter through \
            a separate entrance, would consider this advantageous.")], className='white-box green-box')

        if (df.iloc[0]["basement_total_sqft"] > 0.0):
            value_basement = html.Div(
                ["You have a sizable basement that could be converted to an AADU."], className='white-box green-box')
            if (df.iloc[0]["sqftfinbasement"] > 0.0):
                value_basement.children.append(
                    "An already finished basement will not be as expensive to retrofit for an AADU.")
            if (df.iloc[0]["daylightbasement"] == "Y"):
                value_basement.children.append(
                    "A daylight basement in particular can be quite attractive to renters.")
        if (df.iloc[0]["garage_basement_sqft"] > 0.0 and not pd.isna(df.iloc[0]["garage_basement_sqft"])):
            value_garage = html.Div(
                ["You have a sizable garage that could be converted to an AADU."], className='white-box green-box')

        if (not pd.isna(df.iloc[0]["miles_nearest_bus"]) == 1):
            value_bus = html.Div([dcc.Markdown("Your home is near a **frequent transit stop**, making it attractive \
                to renters of AADUs and DADUs.")], className='white-box green-box')

        # Negative stuff
        if (df.iloc[0]["yrbuilt"] < 1959):
            value_age = html.Div(
                ["Given the age of your home, converting existing space to an AADU might require substantial changes or upgrades to meet current building code requirements."], className='white-box red-box')

        if (df.iloc[0]["treecanopy_prct"] > 30):
            value_tree = html.Div([
                dcc.Markdown("The amount of tree canopy in your rear yard could constrain the location and size of a DADU. \
                	Consult with a design professional or a land use coach at the \
                	[applicant services center](https://www.seattle.gov/sdci/about-us/who-we-are/applicant-services-center). \
                	Information regarding the City’s tree protection ordinance can be found [here](http://www.seattle.gov/sdci/codes/codes-we-enforce-(a-z)/tree-protection-code).")], className='white-box red-box')  # soft red?

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
            value_sewer = html.Div([dcc.Markdown("Your home appears to have a **conflicting side sewer** crossing \
                another lot. You may need to reroute or construct a new side sewer \
                for a DADU. Additionally, your lot appears to be landlocked, meaning it \
                lacks direct access to the right-of-way. As a result, you may need to run \
                a new side sewer through a neighboring lot in order to construct an ADU.")], className='white-box red-box')
        else:
            if (df.iloc[0]["intersecting_sewer"] == 1):
                value_sewer = html.Div([dcc.Markdown("Your home has a **side sewer** that crosses a neighboring lot. \
                    You may need to reroute or construct a new side sewer for a DADU")], className='white-box')
                #
            if (df.iloc[0]["landlocked_parcel"] == 1):
                value_lock = html.Div([dcc.Markdown("Your lot appears to be **landlocked**, \
                meaning it lacks direct access to the right-of-way. As a result, you may have to \
                    run a new side sewer through a neighboring lot in order to construct an ADU.")], className='white-box')

        if not df.empty:
            output = html.Div([
                html.H5("Other potential considerations for your lot:",
                        style={'textAlign': 'center'}),
                value_age,
                value_alley, value_basement, value_garage, value_bus, value_corner, value_lock,
                html.Div([html.Div(["Environmentally Critical Areas"], style={'textAlign': 'center'}),
                          html.Div([dcc.Markdown("Your lot has the following **environmentally critical areas (ECAs)** that \
                    may make it more costly to permit and build a DADU: (If list is empty, no ECAs are present)")]),
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
    output = html.Div([html.H4("Let's find an ADU around you!", style={'textAlign': 'center'}),
                       fin.neighbor_adu(PIN, df, neighbors)], )

    return output


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
        # Output('zip_code', 'children'),
        Output('eligibilityDetails', 'children'),
        Output('addDetails', 'children'),
        Output('neighborinfo', 'children')
        # Output('zipcode', 'label')
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
        neighbors = adunit.getNeighbors(df)
        zipc = df.iloc[0]["zipcode"]
    return [
        update_map(df, neighbors, coords=SEATTLE, zoom=INIT_ZOOM),
        update_criteria_details(df),
        update_details(df),
        neighbor_adu(value, df, neighbors),
    ]

# print the zipcode currently in the system


@app.callback(
    Output('ZipcodeOutput', 'children'),
    [Input('zipcode', 'value')])
def print_zipcode(value):
    if (value is None):
        try:
            format(zipc)
        except NameError:
            return 'Calculating gains for zipcode: "{}" '.format('98105')
        else:
            return 'Calculating gains for zipcode: "{}" '.format(zipc)
    else:
        return 'Calculating gains for zipcode: "{}" '.format(value)
