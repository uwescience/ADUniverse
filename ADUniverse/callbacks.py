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

# calculating loans


@app.callback(
    [Output(component_id='LoanAmount', component_property='children'),
     Output(component_id='MonthlyPayment', component_property='children')],
    [Input(component_id='LoanInput', component_property='value')]
    #Input(component_id='intermediate-value', component_property='children')
)
def loan_calculator(loan):
    return fin.loan_calculator(loan)

# find out if neighbor has an adu and where


@app.callback(
    Output('adu_around', 'children'),
    [Input('addressDropdown', 'value')])
def neighbor_adu(PIN):
    return fin.neighbor_adu(PIN)


# print out the purposes

@app.callback(
    Output('output_purpose', 'children'),
    [Input('aduPurposeDropdown', 'value')])
def update_purpose(value):
    return 'You are builing this ADU for "{}"'.format(value)


# return zipcode of address

@app.callback(
    Output('zipcode', 'children'),
    [Input('addressDropdown', 'value')])
def update_zipcode(value):
    if value != None:
        adunit = ads.Connection("adunits.db")
        zp_data = adunit.getZipcode(value)
        if zp_data.empty == True:
            return "Sorry, we can't find your zipcode"
        else:
            zp = zp_data.loc[0, 'zipcode']
        return 'Your zipcode is {}'.format(zp)
    else:
        return "Type your address first"
