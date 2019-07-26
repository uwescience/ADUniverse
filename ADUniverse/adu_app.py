import app_pages as page
import constant as C
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import financials as fin
import update_map as updt

from dash.dependencies import Input, Output, State

# Dashify
external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash("SeattleADU", external_stylesheets=external_stylesheets)


#app.layout = page.Original_Page
app.layout = html.Div(page.Original_Page, id='page_layout')


@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(path_name):
    return html.Div([
        html.H3('You are on page {}'.format(path_name))
    ])

# Code for changing page. Broken at the moment
#@app.callback(dash.dependencies.Output('page_layout', 'children'),
#              [dash.dependencies.Input('url', 'pathname')])
#def change_page(path_name):
    #if path_name == '/test':
    #    return page.New_Page
    #else:
#        return page.Original_Page

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
    return updt.update_map(value, coords=coords, zoom=zoom)


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


# calculating loans
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
    Output('output_purpose', 'children'),
    [Input('aduPurposeDropdown', 'value')])
def update_purpose(value):
    return 'You are builing this ADU for "{}"'.format(value)


if __name__ == '__main__':
    app.run_server(debug=True)
