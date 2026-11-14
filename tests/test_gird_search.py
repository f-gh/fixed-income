import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal

from fixed_income.grid_search import ns_linesearch, nss_gridsearch

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


linesearch_data = {
    "Criterion": ["RMSE", "MAE", "Max error"],
    "Lambda": [0.5, 0.5, 0.5],
    "Mu": [np.nan, np.nan, np.nan],
    "Criterion Value": [0.0007, 0.0006, 0.0012],
    "Beta0": [0.0569, 0.0569, 0.0569],
    "Beta1": [-0.0160, -0.0160, -0.0160],
    "Beta2": [-0.0005, -0.0005, -0.0005],
}

linesearch_df = pd.DataFrame(linesearch_data).set_index("Criterion")


gridseach_data = {
    "Criterion": ["RMSE", "MAE", "Max error"],
    "Lambda": [0.3, 0.3, 0.3],
    "Mu": [0.05, 0.05, 0.05],
    "Criterion Value": [0.0003, 0.0002, 0.0005],
    "Beta0": [-0.0751, -0.0751, -0.0751],
    "Beta1": [0.1155, 0.1155, 0.1155],
    "Beta2": [0.0910, 0.0910, 0.0910],
    "Beta3": [0.368, 0.368, 0.368],
}

gridsearch_df = pd.DataFrame(gridseach_data).set_index("Criterion")


def test_ns_linesearch():
    test_result_ns = ns_linesearch(maturities, rates, lambda_values=None)
    assert_frame_equal(
        test_result_ns,
        linesearch_df,
        check_exact=False,
        atol=1e-8,
        rtol=1e-5,
    )


def test_nss_gridsearch():
    test_result_nss = nss_gridsearch(
        maturities, rates, lambda_values=None, mu_values=None
    )
    assert_frame_equal(
        test_result_nss,
        gridsearch_df,
        check_exact=False,
        atol=1e-8,
        rtol=1e-5,
    )
