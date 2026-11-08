import numpy as np
import pytest

from fixed_income.nss_curve import fit_ns, fit_nss

maturities = np.array(
    [
        0.0833,
        0.125,
        0.1666,
        0.25,
        0.3333,
        0.5,
        1,
        2,
        3,
        5,
        7,
        10,
        20,
        30,
    ]
)
rates = np.array(
    [
        0.0406,
        0.041,
        0.0413,
        0.0417,
        0.0426,
        0.0427,
        0.0444,
        0.0478,
        0.0491,
        0.0501,
        0.0512,
        0.0524,
        0.0564,
        0.0561,
    ]
)

expected_ns_betas = np.array([0.05625777, -0.01496435, 0.01353017])
expected_nss_betas = np.array([0.06978144, -0.02872874, 0.03008224, -0.049403])


def test_fit_ns():
    test_result_ns = fit_ns(maturities, rates).x
    assert test_result_ns == pytest.approx(expected_ns_betas)


def test_fit_nss():
    test_result_nss = fit_nss(maturities, rates).x
    assert test_result_nss == pytest.approx(expected_nss_betas)
