# Structural Parameter Assumptions

apr = 0.069  # anual interest rate
maturity = 15  # loan maturity years


def loan_calculator(loan, feature):
    loan = float(loan)
    payment = 0*feature + loan*(apr/12)*(1+(apr/12))**(maturity*12)/((1+(apr/12))**(maturity*12)-1)
    return loan, payment
