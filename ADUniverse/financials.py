import numpy as np

# Structural Parameter Assumptions

APR = 0.069  # anual interest rate
MATURITY = 15  # loan MATURITY years

# CHANGED: added keyword parameters and documentation for function


def loan_calculator(loan, feature, apr=APR, maturity=MATURITY):
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
    payment = 0*feature +   \
        loan*(APR/12)*(1+(APR/12))**(MATURITY*12)  \
        / ((1+(APR/12))**(MATURITY*12)-1)
    return loan, payment


dadu_fixed_cost = 125000
adu_variable_cost = 125
dadu_sewer = 11268
aadu_sewer = 6760
permit_cost = 4000
design_percentage = 0.06


# FIXME: add function level comment
# FIXME: Use python constants instead of numbers (e.g., 125000)
def cost_breakdown(build_dadu, size):
    # CHANGED: Use PEP8 convention for variable names
    """
    Calculates various cost for ADU construction
    :param boolean build_dadu: if building a DADU
    :param float size: the square footage of potential adu
    """
    construction = float(np.array([build_dadu]).astype(int))*dadu_fixed_cost + \
        adu_variable_cost*float(size)
    sewer = float(np.array([build_dadu]).astype(int))*dadu_sewer +  \
        (1-float(np.array([build_dadu]).astype(int)))*aadu_sewer
    design = float(construction)*design_percentage
    total = construction + sewer + design + permit_cost
    return construction, sewer, design, total
