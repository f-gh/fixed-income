from fetch_treasury import cleanup_yields
import pandas as pd
import pytest 

input_df = pd.DataFrame({
    "Id": [1],
    "NEW_DATE": ["2026-10-01"],
    "BC_1MONTH": [4.04],
    "BC_1YEAR": [3.50],
    "BC_30YEARDISPLAY": [3.75],
})

df = cleanup_yields(input_df)

def test_date_column_name_is_correct():
    assert df.columns[0] == 'date'

def test_month_column_name_is_correct():
    assert df.columns[1] == '1MONTH'

def test_yield_is_stored_as_decimal():
    assert df["1MONTH"][0] == 0.0404

def test_30YEARDISPLAY_is_dropped():
    assert "30YEARDISPLAY" not in df.columns



