# Structural Parameter Assumptions

import functions
APR = 0.069  # anual interest rate
MATURITY = 15  # loan MATURITY years


def test_loan_calculator(loan, feature):
    (output1, output2) = = functions.loan_calculator(loan, feature)
    assert (output1 != 0)
    assert (output2 != 0)
