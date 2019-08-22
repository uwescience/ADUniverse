import adusql as ads
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import constant as C

from constant import SEATTLE, INIT_ZOOM
from dash_daq import ToggleSwitch  # requires dash_daq version 0.1.0
from folium import Map

import dash_table

import base64
import dash_dangerously_set_inner_html as dish

SEATTLE_LOGO = "assets/seattle-logo.png"

# Navigation Bar
NavigationBar = dbc.NavbarSimple(
    children=[
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=SEATTLE_LOGO, height="50px")),
                    dbc.Col(dbc.NavbarBrand("ADUniverse", className="ml-2")),
                ],
                align="center",
                no_gutters=True,
            ),
            href="/",
        ),
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Map", href="/map")),
        dbc.NavItem(dbc.NavLink("Cost Estimator", href="/finances")),
        dbc.NavItem(dbc.NavLink("FAQ", href="/faq")),
        dbc.NavItem(dbc.NavLink("Transparency", href="/transparency")),
        dbc.NavItem(dbc.NavLink("Testimonials", href="/testimonials")),
        dbc.NavItem(dbc.NavLink("Analysis", href="/analysis")),
        dbc.NavItem(dbc.NavLink("Neighborhood View", href="/neighborhood")),

    ],
    # brand="ADUniverse",
    brand_href="/",
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
addresses = adunit.getAddresses(sqftlot=C.SQFTLOT)
AddressDropdown = dcc.Dropdown(
    id='addressDropdown',
    options=[
        {'label': i, 'value': j} for i, j in zip(addresses.address, addresses.PIN)
    ],
    placeholder='Type your house address here...',
    style={'width': '100%', 'display': 'inline-block', 'vertical-align': 'top'}
)

# create empty map zoomed in on Seattle
Map(location=SEATTLE, zoom_start=INIT_ZOOM, control_scale=True).save("map.html")

MapBlock = html.Iframe(id='map', srcDoc=open("map.html", "r").read(),
                       width="100%", height="75%", style={'display': 'inline-block'})  # height="550"


prices = pd.read_csv("prices_byzipcode.csv")
# Financial Feasibility section


def zipPlaceholder():
    from common_data import app_data
    if app_data.zipcode != 0:
        return str(app_data.zipcode)
    elif app_data.zipcode == 0:
        return 'Find your zipcode here...'


FinFeasibility = html.Div([
    html.Div([
        html.H3('What ADU will you build?', style={'textAlign': 'center'}),
        ToggleSwitch(
            id='build_dadu',
            label=['Attached ADU', 'Detached ADU'],
            style={'width': '350px', 'margin': 'auto'},
            value=False),
        dcc.Markdown('''&nbsp; '''),
        dcc.Slider(
            id='BuildSizeInput',
            min=200,
            max=1000,
            step=10,
            marks={
                300: '300 SF (Studio)',
                500: '500 SF (1 Bed)',
                800: '800 SF (2 Bed)',
            },
            value=500,),
        dcc.Markdown('''&nbsp; '''),
        html.Div(id='BuildSizeOutput', style={'textAlign': 'center'}),
        html.H4('Cost Breakdown:', style={'textAlign': 'center'}),
        html.Table([
            html.Tr([html.Td(['Construction Cost']), html.Td(id='ConstructCost')]),
            html.Tr([html.Td(['+ Sales Tax (10.1%) ']), html.Td(id='Tax')]),
            html.Tr([html.Td(['+ Sewer Capacity Charge ']), html.Td(id='SewerCharge')]),
            html.Tr([html.Td(['+  Permit Fee']), html.Td(id='PermitFee')]),
            html.Tr([html.Td(['+  Architecture Fee']), html.Td(id='DesignCost')]),
            html.Tr([html.Td(['=  Estimated Cost']), html.Td(id='TotalCost')])]),
        html.P('*Actual cost may vary. The estimate is for reference only.'),
        html.A("Be part of the SOLUTION! (@Seattle.gov)",
               href='http://www.seattle.gov/rentinginseattle', target="_blank")

    ], className="six columns"),

    html.Div([
        html.H3("Cost Estimator", style={'textAlign': 'center'}),
        html.H5("How much will you borrow?"),
        html.H1("  "),
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
            value=50000,
        ),
        html.H2("  "),
        html.Table([
            html.Tr([html.Td(['Total Loan']), html.Td(id='LoanAmount')]),
            html.Tr([html.Td(['Monthly Payment']), html.Td(id='MonthlyPayment')]),
            html.Tr([html.Td(['Monthly Increase In Property Tax']), html.Td(id='PropertyTax')])
        ]),
        html.H2("  "),
        html.P('Assumptions: APR 6.9% for a 15-year fixed-rate home equity loan.'),
        html.P('Reminder: Your home equity loan interest might be tax deductible!'),
        html.H3("Financial Benefits", style={'textAlign': 'center'}),
        dcc.Dropdown(
            id='zipcode',
            options=[
                {'label': i, 'value': i} for i in sorted(prices.ZipCode)
            ],
            placeholder='Modify your zipcode here...',
            # value='98105'
        ),
        html.H4("  "),
        html.Div(id='ZipcodeOutput', style={'textAlign': 'center'}),
        html.Table([
            html.Tr([html.Td(['Estimated Monthly Rental']),
                     html.Td(id='rental')]),
            html.Tr([html.Td(['Estimated Value-Added to Property']),
                     html.Td(id='sales')])
        ]),
        html.P('*Based on Zillow home value and rental index.'),
    ], className="six columns",),

], className="row", style={'margin-left': '25px', 'margin-right': '25px', })

NeighborInfo = html.Div([], id='neighborinfo',
                        style={'margin-left': '15px', 'margin-right': '15px', })

OutputDetails = html.Div([], id='eligibilityDetails',
                         style={'margin-left': '15px', 'margin-right': '15px', 'height': '420px'})

AdditionalDetails = html.Div([], id='addDetails',
                             style={'margin-left': '10px', 'margin-right': '10px', })

# FAQ Section
FAQ = dcc.Markdown('''
## Can you give me some more financial information?
Here is the home equity loan information
## I guess I have to talk to an architect?
Here is a contact for the architects' association in Seattle
## What do I do to start the permitting process?
Here are some contacts to get you started and for questions.
## So I have to become a landlord..
Here are some resources about being a landlord!
## What's the deal with these side sewers?
## What are my neighborhood covenants?
You may be living within the jurisdiction of a homeowner's association that may have its own rules in place regarding ADUs.
The best way to begin, if you have not looked into their rules, is to Google your neighborhood name followed by "homeowners association"
## Other links
If you may not have the funds to build an ADU on your property at the moment, but wish to affect the housing crisis, consider the
[Block Project](http://the-block-project.org/). Volunteers with this nonprofit design and build a small ADU in your backyard and
house a member of the homeless community, while you pay only their water bill.

'''
                   )

Transparency = html.Div([

    html.A("Here in this PDF is a glossary of terms!",
           href='https://www.rhawa.org/', target="_blank"),

    dcc.Markdown('''
## ADUniverse
Accessory Dwelling Units (ADU) such as backyard cottages and in-house mother-in-law apartments provide a way for the
City of Seattle to address the housing affordability crisis. This project is about aiding owners of single family homes
to assess the eligibility and desirability of building an ADU. We illustrate our vision via a prototype software tool for homeowners.


## Here's all the stuff that goes into making a decision to be eligible for an ADU
The current legislation states that:
You can build up to 2 ADUs
The owner does not have to occupy any of the units
There is no parking requirement
You must be in a single family lot to build any sort of ADU
Your lot size must be at least 3200 square feet
Your lot width (the side of your home neighboring the street) must be at least 25 feet
Your lot depth (the adjoining line) must be at least 70 feet
Property must have sufficient available lot area for a new accessory structure (or project is conversion of an existing structure).
Maximum lot coverage:
35 percent of lot area for lots >= 5,000 sq. ft.
1,000 sq. ft. + 15 percent of lot area for lots < 5,000 sq. ft
You may build a maximum of x sized ADU on your lot
Property must have sufficient available area of the rear yard for a new accessory structure
(or project is conversion of an existing structure)
Maximum rear yard coverage:
60 percent of designated rear yard (25 feet or 20 percent of lot depth, whichever is less, and 10 feet minimum)
You can not build any ADU if your home lies along the shoreline.

Other variables such as your parcel being on environmentally critical areas, sharing side sewers with other parcels, trees and tree roots in your anticipated build site might (or might not!) all affect the cost to permit and build an ADU.
Some variables such as your home's proximity to well-served transit stops, presence on corner lots or by an alley, a large basement or garage, and others might advantage a built ADU(???) increase market value of your ADU???

Everything has a degree of uncertainty. Many of these variables were calculated. Existence of unpermitted accessory structures could be barriers to building that would be difficult for this tool to assess. Your lot width and depth, and presence on corner lots, for instance, are merely estimates.

## Here's how we came up with our estimates
We identified each parcel’s placement on neighborhood, zip code, environmental variables (steep slope, riparian corridors,
peat settlements, etc), city zones, and on high tree cover yards. We were then able to measure these parcels’ proximity to other
zones, to nearest and frequent transit stops, to alleys and to the shoreline. Using ArcGIS tools, we created corner lot,
alley lot, and lot coverage indicators by overlaying relevant shapefiles and manipulating intersecting features.
Their potential median home value based on their location in a Zillow neighborhood was also calculated.

Our data was collected from a combination of City of Seattle OpenGIS Portal, King County Assessors, the US Census Bureau and Zillow.
There may be mistakes in this data we are not responsible for.

## Assumptions Made
Our rental number comes from zillow and is condos, MF and all
For the cost estimation, we understand that each parcel has its own physical characters that may add up or lower
the cost of construction. Our estimate is based on appendix 1 of the Environmental Statement Impact (EIS) report on ADUs
from the City of Seattle (2018).
For the mortgage calculation, we assumed the homeowner will use home equity loans (HELOC). This assumption is based on
the experience of Oregon where most ADU constructors use either cash/savings or home equity loans. The 6.9% APR is the
prevailing market rate accessed from Wells Fargo website for a 15-year fixed-rate loan. Both interest rates and rental income
are subjected to future market fluctuations, our analysis doesn’t take this into consideration.



## Stuff We Haven't Gotten To:
Rear yard coverage


## Stuff In The Works Through the City
Pre approved ADU plans
Low income Homeowner assistance
Direct connection to Voucher 8 holder
Once these are created, these can be integrated into the app to suggest, based on the user’s inputs, city-supported loan
options and low-income renter voucher options to you.


## Why Do You Post My Neighbors' Addresses?
So you'll talk to the darn humans around you.
(Discussions about the issues surrounding this)


*Disclaimer: We help to gather useful informtion to facilitate your decisions *
''')

])

image_filename = 'assets/my-image.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())
image_filename2 = 'assets/webflow.png'
webflow_image = base64.b64encode(open(image_filename2, 'rb').read())


Home = html.Div([
    html.Div([
        html.Div([dish.DangerouslySetInnerHTML('''
        <map id="map-map" name="image-map">
            <area target="" alt="" title="" href="/map" coords="1,30,100,100" shape="rect" cursor="pointer">
            <area target="" alt="" title="" href="/faq" coords="130,30,255,100" shape="rect">
            <area target="" alt="" title="" href="/finances" coords="60,195,175,269" shape="rect">
        </map>
        ''')], id="image-map", style={'display': 'none', 'cursor': 'pointer'}),
        dcc.Markdown(['''
        **What is an ADU?**
        Accessory dwelling units (ADUs) are small, secondary homes located within, attached to, or in the rear yard of a single-family lot. A detached accessory dwelling unit (DADU), often called a backyard cottage or carriage house, is a secondary unit located in a separate structure from the main house. An attached accessory dwelling unit (AADU), often called a basement apartment or secondary suite, is located within or connected to the main house.
        '''], style={'font': '2px'}),
        html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), alt="Types of Accessory Dwelling Units",
                 style={'align': 'center', 'width': '100%', 'height': '25%'}),
        dcc.Markdown('''
            ---
            **What is the ADUniverse?**
            Creating an accessory dwelling unit can raise several questions. What’s possible on my property? Where do I start? The ADUniverse is your gateway to answers. Our [map tool](/map) assesses the physical feasibility of an ADU on your lot. Our [cost estimator](/finances) helps you evaluate the financial costs and benefits of an ADU. Ready to proceed? You can explore pre-approved plans, get a loan from the City, and begin the permitting process. Are you a policymaker or ADU advocate? Explore our [citywide and neighborhood-level analysis](/analysis) of how ADUs can support affordability and equity goals.

            **Navigate Through this Site**
        '''),
        html.Img(src='data:image/png;base64,{}'.format(webflow_image.decode()), alt="Navigation for ADUniverse page",
                     style={'align': 'center', 'width': '530px', 'height': '298px'}, useMap="#image-map")
    ], className="seven columns"),


    html.Div([
        html.H4('NEWS', style={'textAlign': 'center'}),
        html.Iframe(src=f'https://www.youtube.com/embed/V9B_Nw9X4AI',
                    style={'width': '560px', 'height': '315px', 'frameborder': '0'}),
        dcc.Markdown(['''

            > (City) will develop a one-stop ADU website that provides a comprehensive inventory of
            > ADU information, guidance, resources ... by prototyping an ADU feasibility tool through the City’s
            > participation in the UW Data Science for Social Good program.
            - From Mayor Durkan's Executive Order'''], style={'font-style': 'italic'}),
        dcc.Markdown('''
        © ADUniverse, DSSG 2019, eScience Institute, University of Washington
        Project Leads: Rick Mohler, Nick Welch, Joseph Hellerstein
        Fellows: Emily Finchum-Mason, Yuanhao Niu, Adrian Tullock, Anagha Uppal
        '''),
    ], className="five columns"),
], className="row", style={'margin-left': '20px', 'margin-right': '20px', })

Analysis = html.Iframe(id='anal', srcDoc=open("analysis.html", "r").read(),
                       style={'display': 'inline-block', 'width': '100%', 'height': '800px'})

ADU_Counts = html.Iframe(id='adc', srcDoc=open("adu_counts.html", "r").read(),
                         style={'display': 'inline-block', 'width': '100%', 'height': '800px'})
