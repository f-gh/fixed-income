def discount_factor(rate, maturity):
    if maturity < 0:
        raise ValueError("Maturity cannot be negative")
        
    return 1/(1 + rate)**maturity

