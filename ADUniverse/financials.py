import constant as C
import numpy as np
import pandas as pd
import adusql as ads


def loan_calculator(loan, apr=C.MONTHLY_APR, maturity=C.ANNUAL_MATURITY):
    """
    Calculates the monthly payments for a loan over
    the maturity period.
    :param number load: amount to borrow
    :param float apr: annual interest rate of the loan
    :param int maturity: maturity for the loan
    :
    """
    loan = float(loan)

    payment = loan*(apr)*(1+apr)**(maturity) / ((1+apr)**(maturity)-1)
    return '${0:6,.0f}'.format(loan), '${0:5,.0f}'.format(payment)


def cost_breakdown(build_dadu, size):
    """
    Calculates various cost for ADU construction
    :param boolean build_dadu: if building a DADU
    :param float size: the square footage of potential adu
    """
    construction = float(np.array([build_dadu]).astype(int))*C.DADU_FIXED + \
        C.ADU_VAR*float(size)

    construction_min = construction*(1-C.MULTIPLIER)

    construction_max = construction*(1+C.MULTIPLIER)

    tax_min = construction_min*C.SALES_TAX

    tax_max = construction_max*C.SALES_TAX

    sewer = float(np.array([build_dadu]).astype(int))*C.DADU_SEWER +  \
        (1-float(np.array([build_dadu]).astype(int)))*C.AADU_SEWER

    permit = C.PERMIT_FIXED + float(size)*C.PERMIT_VAR

    design_min = float(construction_min)*C.DESIGN_PERCENTAGE
    design_max = float(construction_max)*C.DESIGN_PERCENTAGE

    total_min = construction_min + tax_min + sewer + design_min + permit
    total_max = construction_max + tax_max + sewer + design_max + permit

    property_tax = (total_min+total_max)/2*C.PROPERTY_TAX/12

    if build_dadu == 1:
        return '(${0:6,.0f} -- ${1:6,.0f})'.format(construction_min, construction_max), \
               '(${0:6,.0f} -- ${1:6,.0f})'.format(tax_min, tax_max), \
            '${0:6,.0f}'.format(sewer), '${0:6,.0f}'.format(permit), \
            '(${0:6,.0f} -- ${1:6,.0f})'.format(design_min, design_max), \
            '(${0:6,.0f} -- ${1:6,.0f})'.format(total_min, total_max), \
            '${0:3,.0f}'.format(property_tax)
    else:
        return '(${0:6,.0f} -- ${1:6,.0f})'.format(construction_min, construction_max), \
               '(${0:6,.0f} -- ${1:6,.0f})'.format(tax_min, tax_max), \
            "(Not Applicable)",  '${0:6,.0f}'.format(permit), \
            '(${0:6,.0f} -- ${1:6,.0f})'.format(design_min, design_max), \
            '(${0:6,.0f} -- ${1:6,.0f})'.format(total_min, total_max), \
            '${0:3,.0f}'.format(property_tax)


prices = pd.read_csv("prices_byzipcode.csv")


def returns(build_size, zipcode):
    """
    Calculates the expeted rental and value-added
    :param int build_size: size of ADU to build
    :param string zipcode: zipcode of the ADU
    """

    if int(zipcode) in list(prices['ZipCode']):
        zip_code = zipcode

        rent_per_fq = prices[prices['ZipCode'] == int(zip_code)].rent.values[0]
        rental = float(build_size)*float(rent_per_fq)

        sales_per_fq = prices[prices['ZipCode'] == int(zip_code)].sales.values[0]
        sales = 0.2*float(build_size)*float(sales_per_fq)

        return '${0:6,.0f}'.format(rental), '${0:6,.0f}'.format(sales)
    else:
        return "Can't find your ZipCode", "Can't find your ZipCode"


def neighbor_adu(PIN, df, neighbors):
    """
    Find existing ADU around the entered address
    :param text PIN: PIN number related to the address entered
    """
    if PIN != None:

        if neighbors.empty == True:
            return "We didn't find an ADU around you. Be the FIRST!"
        else:
            neighbors = neighbors.head(1).reset_index()
            address = neighbors.loc[0, 'address']
        return ("At least one of your neighbors has an ADU. Zoom out to see more on the map.\
                The closest one @ {}".format(address))
    else:
        return "Please enter your address first"
