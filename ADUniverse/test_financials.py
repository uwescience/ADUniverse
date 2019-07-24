import financials

# Structural Parameter Assumptions
APR = 0.069  # anual interest rate
MATURITY = 15  # loan MATURITY years


def test_loan_calculator():
    loan = 150000
    feature = 3
    output1, output2 = financials.loan_calculator(loan, feature)
    assert (float(output1) != 0)
    assert (float(output2) != 0)


def test_cost_breakdown():
    construction, sewer, design, total = financials.cost_breakdown(True, 500)
    assert(isinstance(float(construction), float))
    assert(isinstance(float(sewer), float))
    assert(isinstance(float(design), float))
    assert(isinstance(float(total), float))
