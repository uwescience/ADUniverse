# Structural Parameter Assumptions

apr = 0.069  # anual interest rate
maturity = 15  # loan maturity years


def loan_calculator(loan, feature):
    loan = float(loan)
    payment = 0*feature + loan*(apr/12)*(1+(apr/12))**(maturity*12)/((1+(apr/12))**(maturity*12)-1)
    return loan, payment


def cost_breakdown(size):
    ConstructCost = 125000+125*float(size)
    DesignCost = float(ConstructCost)*0.06
    TotalCost = ConstructCost+DesignCost+11268+4000
    return ConstructCost, DesignCost, TotalCost


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
