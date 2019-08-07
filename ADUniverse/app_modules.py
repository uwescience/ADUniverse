import adusql as ads
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
from callbacks import CommonData


from constant import SEATTLE, INIT_ZOOM
from dash_daq import ToggleSwitch  # requires dash_daq version 0.1.0
from folium import Map

import base64

common_data = CommonData()

# Navigation Bar
NavigationBar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Map", href="/map")),
        dbc.NavItem(dbc.NavLink("Financial Feasibility", href="/finances")),
        dbc.NavItem(dbc.NavLink("FAQ", href="/faq")),
        dbc.NavItem(dbc.NavLink("Transparency", href="/transparency")),
        dbc.NavItem(dbc.NavLink("Testimonials", href="/testimonials")),

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
adunit = ads.Connection()
addresses = adunit.getAddresses()
AddressDropdown = dcc.Dropdown(
    id='addressDropdown',
    options=[
        {'label': i, 'value': j} for i, j in zip(addresses.address, addresses.PIN)
    ],
    placeholder='Type your house address here...',
    style={'width': '48%', 'display': 'inline-block', 'vertical-align': 'top'}
)

# create empty map zoomed in on Seattle
Map(location=SEATTLE, zoom_start=INIT_ZOOM, control_scale=True).save("map.html")

MapBlock = html.Iframe(id='map', srcDoc=open("map.html", "r").read(),
                       width="50%", height="550", style={'display': 'inline-block'})


PurposeDropdown = dcc.Dropdown(
    id='aduPurposeDropdown',
    options=[
        {'label': 'Build one more unit for rental income', 'value': 'income'},
        {'label': 'A Relative needs some housing', 'value': 'support'},
    ],
    value='purposes'
)

prices = pd.read_csv("prices_byzipcode.csv")
# Financial Feasibility section
FinFeasibility = html.Div([
    html.Div([
        html.H3('Cost Breakdown', style={'textAlign': 'center'}),
        ToggleSwitch(
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
            html.Tr([html.Td(['*Actual cost may vary. Estimation is for reference only.'])])])
    ], className="six columns"),

    html.Div([
        html.H3("Financial Cost", style={'textAlign': 'center'}),
        html.H5("How much will you borrow?"),
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
        html.H2("  "),
        html.Table([
            html.Tr([html.Td(['Total Loan']), html.Td(id='LoanAmount')]),
            html.Tr([html.Td(['Monthly Payment']), html.Td(id='MonthlyPayment')]),
            html.Tr([html.Td(['Monthly Increase In Property Tax']), html.Td(id='PropertyTax')])
        ]),
        html.H2("  "),
        dcc.Markdown('''Assumptions:
                    APR 6.9% for a 15-year fixed-rate home equity loan.'''),

        html.H3("Financial Benefits", style={'textAlign': 'center'}),
        html.H5("Where do you live?"),
        dcc.Dropdown(
            id='zipcode',
            options=[
                {'label': i, 'value': i} for i in prices.ZipCode
            ],
            value=str(common_data.zipcode)),
        html.Table([
            html.Tr([html.Td(['Estimated Monthly Rental (Zillow)']),
                     html.Td(id='rental')]),
            html.Tr([html.Td(['Estimated Value-Added to Property (Zillow)']),
                     html.Td(id='sales')])
        ]),
        html.H2("  "),
        dcc.Markdown('''
        Be part of the SOLUTION! check out [Seattle Housing Authority]
        (https://www.seattlehousing.org/housing/housing-choice-vouchers/landlords)
        '''),
    ], className="six columns",),

], className="row", style={'margin-left': '25px', 'margin-right': '25px', })

# FAQ Section
FAQ = dcc.Markdown('''
## How to be a good landlord?
Here is some useful information.
[Rental Housing Association of Washington](https://www.rhawa.org/)
## More financial information?
Here is the home equity loan information
*Disclaimer: We help to gather useful informtion to facilitate your decisions *
'''
                   )

Transparency = dcc.Markdown('''
Here in this PDF is a glossary of terms!
[Glossary of Terms](https://www.rhawa.org/)
## Here's all the stuff that goes into making a decision to be eligible for an ADU
The current legislation states that:
You can build up to 2 ADUs
The owner does not have to occupy any of the units
There is no parking requirements
You must be in a single family lot to build any sort of ADU
Your lot size must be at least y
Your lot width (the side of your home neighboring the street) must be at least xx
Your lot depth (the adjoining line) must be at least xxx
You may build a maximum of x sized ADU on your lot
Your lot coverage including ADUs may be no more than yy
You can not build any ADU if your home lies along the shoreline.

Other variables such as your parcel being on environmentally critical areas, sharing side sewers with other parcels, trees and tree roots in your anticipated build site might (or might not!) all affect the cost to permit and build an ADU.
Some variables such as your home's proximity to well-served transit stops, presence on corner lots or by an alley, ___, __, and others might advantage a built ADU(???) increase market value of your ADU???

Everything has a degree of uncertainty. Many of these variables were calculated. Existence of unpermitted accessory structures could be barriers to building that would be difficult for this tool to assess. Your lot width and depth, and presence on corner lots, for instance, are merely estimates.

Our data was collected from a combination of City of Seattle OpenGIS Portal, King County Assessors, the US Census Bureau and Zillow.
There may be mistakes in this data we are not responsible for.

## Assumptions Made


## Stuff We Haven't Calculated
Rear coverage

Side sewer

## Stuff In The Works Through the City
Pre approved plans

low income Homeowner assistance, direct connection to 8 Voucher holder

## Why Do You Post My Neighbors' Addresses?
So you'll talk to the darn humans around you.
(Discussions about the issues surrounding this)


*Disclaimer: We help to gather useful informtion to facilitate your decisions *
'''
                            )

image_filename = 'my-image.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())


Home = html.Div(html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), alt="Types of Accessory Dwelling Units",
                         style={'align': 'center', 'width': '50%', 'height': '50%'})
                )
