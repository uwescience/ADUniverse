import constant as C
import numpy as np

# CHANGED: added keyword parameters and documentation for function


def loan_calculator(loan, feature, apr=C.MONTHLY_APR, maturity=C.ANNUAL_MATURITY):
    """
    Calculates the monthly payments for a loan over
    the maturity period.
    :param number load: amount to borrow
    #FIXME: put in the correct information for feature
    :param ?? feature:
    :param float apr: annual interest rate of the loan
    :param int maturity: maturity for the loan
    :
    """
    loan = float(loan)

    payment = 0*feature + loan*(apr)*(1+apr)**(maturity)  \
        / ((1+apr)**(maturity)-1)
    return '{0:6,.0f}'.format(loan), '{0:6,.0f}'.format(payment)


# FIXME: add function level comment
def cost_breakdown(build_dadu, size):
    # CHANGED: Use PEP8 convention for variable names
    """
    Calculates various cost for ADU construction
    :param boolean build_dadu: if building a DADU
    :param float size: the square footage of potential adu
    """
    construction = float(np.array([build_dadu]).astype(int))*C.DADU_FIXED + \
        C.ADU_VAR*float(size)

    sewer = float(np.array([build_dadu]).astype(int))*C.DADU_SEWER +  \
        (1-float(np.array([build_dadu]).astype(int)))*C.AADU_SEWER

    design = float(construction)*C.DESIGN_PERCENTAGE
    total = construction + sewer + design + C.PERMIT
    return '{0:6,.0f}'.format(construction), '{0:6,.0f}'.format(sewer), \
        '{0:6,.0f}'.format(design), '{0:6,.0f}'.format(total)
