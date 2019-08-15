import financials as fin


def test_loan_calculator():
    loan = 150000
    output1, output2 = fin.loan_calculator(loan)
    assert(isinstance(output1, str))
    assert(isinstance(output2, str))


def test_cost_breakdown():
    build_dadu = True
    size = 500
    construction, tax, sewer, permit, design, total, p_tax = fin.cost_breakdown(build_dadu, size)
    assert(isinstance(construction, str))
    assert(isinstance(tax, str))
    assert(isinstance(sewer, str))
    assert(isinstance(permit, str))
    assert(isinstance(design, str))
    assert(isinstance(total, str))
    assert(isinstance(p_tax, str))


def test_returns():
    build_size = 500
    zipcode = 98103
    rental, sales = fin.returns(build_size, zipcode)
    assert(isinstance(rental, str))
    assert(isinstance(sales, str))
