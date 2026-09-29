from fixed_income.curve import discount_factor

def test_discount_factor():
    df = discount_factor(0.05, 1)

    assert df == 1 / 1.05

    