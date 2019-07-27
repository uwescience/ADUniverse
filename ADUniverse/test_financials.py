import financials as fin

# Structural Parameter Assumptions
APR = 0.069  # anual interest rate
MATURITY = 15  # loan MATURITY years


def test_loan_calculator():
    loan = 150000
    feature = 3
    output1, output2 = fin.loan_calculator(loan, feature)
    assert(isinstance(output1, str))
    assert(isinstance(output2, str))


def test_cost_breakdown():
    construction, tax, sewer, permit, design, total, p_tax = fin.cost_breakdown(True, 500)
    assert(isinstance(construction, str))
    assert(isinstance(tax, str))
    assert(isinstance(sewer, str))
    assert(isinstance(permit, str))
    assert(isinstance(design, str))
    assert(isinstance(total, str))
    assert(isinstance(p_tax, str))
