import financials

# Structural Parameter Assumptions
APR = 0.069  # anual interest rate
MATURITY = 15  # loan MATURITY years


def test_loan_calculator():
    loan = 150000
    feature = 3
    output1, output2 = financials.loan_calculator(loan, feature)
    assert (output1 != 0)
    assert (output2 != 0)


def test_cost_breakdown():
    construction, sewer, design, total = financials.cost_breakdown(True, 500)
    assert(isinstance(construction, float))
    assert(isinstance(sewer, float))
    assert(isinstance(design, float))
    assert(isinstance(total, float))
