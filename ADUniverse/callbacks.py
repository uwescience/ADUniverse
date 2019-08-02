import financials as fin
import update_map as updt
import adusql as ads

from adu_app import app
from constant import SEATTLE, INIT_ZOOM
from dash.dependencies import Input, Output
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


@app.callback(
    [Output('rental', 'children'),
     Output('sales', 'children')],
    [Input('BuildSizeInput', 'value'),
     Input('zipcode', 'value')])
def returns(buildSize, zipcode):
    return fin.returns(buildSize, zipcode)

# dynamically updates the map based on the address selected


@app.callback(
    Output('map', 'srcDoc'),
    [Input('addressDropdown', 'value')]
)
def update_map(value, coords=SEATTLE, zoom=INIT_ZOOM):
    return updt.update_map(value, coords=coords, zoom=zoom)

# space holder for some features
# @app.callback(
#    Output('intermediate-value', 'children'),
#    [Input('addressDropdown', 'value')]
# )
# def get_features(value):
    # if value != None:
    # output = data.loc[data['ADDRESS'] == value].reset_index()['YRBUILT'][0]
    # output = addresses.loc[addresses.address == value].reset_index()['YRBUILT'][0]
#    output = 0
#    return output

# calculating loans


@app.callback(
    [Output(component_id='LoanAmount', component_property='children'),
     Output(component_id='MonthlyPayment', component_property='children')],
    [Input(component_id='LoanInput', component_property='value')]
    #Input(component_id='intermediate-value', component_property='children')
)
def loan_calculator(loan):
    return fin.loan_calculator(loan)

# if neighbor has an adu


@app.callback(
    Output('adu_around', 'children'),
    [Input('addressDropdown', 'value')])
def update_purpose(value):
    if value != None:
        adunit = ads.Connection("adunits.db")
        ngb_data = adunit.getNeighbor(value)
        if ngb_data.empty == True:
            return "We didn't find an ADU around you. Be the FIRST!"
        else:
            address = ngb_data.loc[0, 'address']
        return 'Your Neighbor has an ADU! Check it out @ {}'.format(address)
    else:
        return 'Please enter your address first'

# print out


@app.callback(
    Output('output_purpose', 'children'),
    [Input('aduPurposeDropdown', 'value')])
def update_purpose(value):
    return 'You are builing this ADU for "{}"'.format(value)


@app.callback(
    Output('zipcode', 'children'),
    [Input('addressDropdown', 'value')])
def update_zipcode(value):
    if value != None:
        adunit = ads.Connection("adunits.db")
        zp_data = adunit.getZipcode(value)
        if zp_data.empty == True:
            return "We can't find it"
        else:
            zp = zp_data.loc[0, 'zipcode']
        return 'Your zipcode is {}'.format(zp)
    else:
        return "Type your address first"
