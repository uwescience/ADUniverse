# Structural Parameter Assumptions

APR = 0.069  # anual interest rate
MATURITY = 15  # loan MATURITY years

#CHANGED: added keyword parameters and documentation for function
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
        /((1+(APR/12))**(MATURITY*12)-1)
    return loan, payment


#FIXME: add function level comment
#FIXME: Use python constants instead of numbers (e.g., 125000)
def cost_breakdown(size):
    #CHANGED: Use PEP8 convention for variable names
    construction = 125000+125*float(size)
    design = float(construction)*0.06
    total = construction + design+11268+4000
    return construction, design, total


def decide_finance(benifit, cost):
    yell = "We need a little bit more information of you."
    if benifit != None and cost != None:
        if float(benifit) > 1.2*float(cost):
            yell = "Great financial decision!"
        elif float(benifit) < 0.8*float(cost):
            yell = "Very risky financial decision!"
        else:
            yell = "Probably not a bad idea."
    return yell
