from fixed_income.linear_cmt_curve import create_interpolation_df
from fixed_income.linear_cmt_curve import interpolate_cmt

import pandas as pd
import numpy as np
import pytest

df = pd.DataFrame({
    "date": ["2026-10-01"],
    "6MONTH": [3.04],
    "1YEAR": [3.50],
    "2YEAR": [3.91],
    "3YEAR": [4.50],
    "5YEAR": [4.80],
    "7YEAR": [4.91],
    "10YEAR": [5.50],
    "20YEAR": [5.70],
    "30YEAR": [5.90],
})

def test_dataframe_length():
    df_test = create_interpolation_df(df)
    assert len(df_test.columns) == 61

def test_interpolate_cmt():
    df_test = create_interpolation_df(df)
    df_test = interpolate_cmt(df_test)
    assert df_test['2.5'].iloc[0] == pytest.approx(4.205)
    assert df_test['29.5'].iloc[0] == pytest.approx(5.89)
    assert df_test['30.0'].iloc[0] == pytest.approx(5.9)



