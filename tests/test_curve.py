from fixed_income.curve import discount_factor
import pytest 

def test_discount_factor_one_year():
    assert discount_factor(0.05, 1) == 1 / 1.05

def test_discount_factor_zero_maturity():
    assert discount_factor(0.05, 0) == 1

def test_discount_factor_negative_maturity():
    # negative maturity is financially impossible
    with pytest.raises(ValueError):
        discount_factor(1, -1)


    