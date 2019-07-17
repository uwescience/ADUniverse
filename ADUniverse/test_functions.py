# Structural Parameter Assumptions

import functions
apr = 0.069  # anual interest rate
maturity = 15  # loan maturity years


def test_loan_calculator(loan, feature):
    (output1, output2) = = functions.loan_calculator(loan, feature)
    assert (output1 != 0)
    assert (output2 != 0)
