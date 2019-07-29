import adusql as ads
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_daq as daq # requires dash_daq version 0.1.0

# Navigation Bar
NavigationBar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Map", href="/map")),
        dbc.NavItem(dbc.NavLink("Financial Feasibility", href="/finances")),
        dbc.NavItem(dbc.NavLink("Additional Information", href="/more-info")),
        dbc.NavItem(dbc.NavLink("Transparency", href="/transparency")),
        dbc.NavItem(dbc.NavLink("Test Page", href="/test")),
    ],
    brand="Seattle ADU Feasibility",
    brand_href="http://www.seattle.gov/services-and-information/city-planning-and-development",
    brand_external_link=True,
    color="primary",
    dark=True,
    fluid=True,
    id="navbar",
    style={
    }
)


# Address addressDropdown
adunit = ads.Connection("adunits.db")
addresses = adunit.getAddresses()
AddressDropdown = dcc.Dropdown(
    id='addressDropdown',
    options=[
        {'label': i, 'value': j} for i, j in zip(addresses.address, addresses.PIN)
    ],
    placeholder='Type your house address here...',
    style={'width': '48%', 'display': 'inline-block', 'vertical-align': 'top'}
)


PurposeDropdown = dcc.Dropdown(
    id='aduPurposeDropdown',
    options=[
        {'label': 'Build one more unit for rental income', 'value': 'income'},
        {'label': 'A Relative needs some housing', 'value': 'support'},
    ],
    value='purposes'
)


# Financial Feasibility section
FinFeasibility = html.Div([
    html.Div([
        html.H3('Cost Breakdown', style={'textAlign': 'center'}),
        daq.ToggleSwitch(
            id='build_dadu',
            label=['Attached ADU', 'Detached ADU'],
            style={'width': '350px', 'margin': 'auto'},
            value=False),
        html.H4('What ADU will you build?', style={'textAlign': 'center'}),
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
            html.Tr([html.Td(['+ Sales Tax (10.1%) ']), html.Td(id='Tax')]),
            html.Tr([html.Td(['+ Sewer Capacity Charge ']), html.Td(id='SewerCharge')]),
            html.Tr([html.Td(['+  Permit Fee']), html.Td(id='PermitFee')]),
            html.Tr([html.Td(['+  Architecture Fee']), html.Td(id='DesignCost')]),
            html.Tr([html.Td(['=  Estimated Cost']), html.Td(id='TotalCost')]),
            html.Tr([html.Td(['Estimated Increase In Property Tax']), html.Td(id='PropertyTax')]),
            html.Tr([html.Td(['*Actual cost may vary. Estimation is for reference only.'])])])
    ], className="six columns"),

    html.Div([
        html.H3("How much will you borrow?", style={'textAlign': 'center'}),
        dcc.Slider(
            id='LoanInput',
            min=10000,
            max=400000,
            step=1000,
            marks={
                100000: '100 K',
                200000: '200 K',
                300000: '300 K',
            },
            value=150000,
        ),
        html.Table([
            html.Tr([html.Td(['Total Loan']), html.Td(id='LoanAmount')]),
            html.Tr([html.Td(['Monthly Payment']), html.Td(id='MonthlyPayment')])
        ]),

        dcc.Markdown('''Assumptions:
                    APR 6.9% for a 15-year fixed-rate home equity loan.
                    Bank typical requires debt-to-income ratio < 40%.'''),

        html.H3("Where do you live?", style={'textAlign': 'center'}),
        dcc.Dropdown(
            id='neighbor_dropdown',
            options=[  # data from zillow 2019/may rent per square foot
                {'label': 'Ballard', 'value': '3.277945619'},
                {'label': 'Capitol Hill', 'value': '3.22537112'},
                {'label': 'Downtown', 'value': '3.861445783'},
                {'label': 'Fremont', 'value': '3'}, ],
            value='3'),
        html.Table(
            [html.Tr([html.Td(['Expected Monthly Rental (Zillow Estimate)']),
                      html.Td(id='rental')])], style={'textAlign': 'center'}),
        html.H2("  "),
        dcc.Markdown('''
        Be part of the SOLUTION! check out [Seattle Housing Authority]
        (https://www.seattlehousing.org/housing/housing-choice-vouchers/landlords)
        '''),
    ], className="six columns",),

], className="row", style={'margin-left': '25px', 'margin-right': '25px', })
