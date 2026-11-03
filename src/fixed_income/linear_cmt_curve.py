import numpy as np
import pandas as pd

# Linear interpolation of the yield curve


# initialize a new dataframe for interpolation
def create_interpolation_df(df: pd.DataFrame) -> pd.DataFrame:
    df_interpolation = df.rename(columns={"6MONTH": "0.5"})

    df_interpolation = df_interpolation.rename(
        columns=lambda col: col.removesuffix("YEAR")
    )

    df_interpolation = df_interpolation.rename(
        columns={
            col: str(float(col)) for col in df_interpolation.columns if col != "date"
        }
    )

    for i in range(3, 60):
        if str(i / 2) not in df_interpolation.columns:
            df_interpolation[str(i / 2)] = np.nan

    maturity_cols = [col for col in df_interpolation.columns if col != "date"]

    maturity_cols = sorted(maturity_cols, key=float)

    df_interpolation = df_interpolation[["date"] + maturity_cols]

    return df_interpolation


# Linear interpolation of constant maturity yields for missing maturities
def interpolate_cmt(df_interpolation: pd.DataFrame) -> pd.DataFrame:
    df_interpolation["1.5"] = df_interpolation["1.0"] + (1.5 - 1) / (2 - 1) * (
        df_interpolation["2.0"] - df_interpolation["1.0"]
    )
    df_interpolation["2.5"] = df_interpolation["2.0"] + (2.5 - 2) / (3 - 2) * (
        df_interpolation["3.0"] - df_interpolation["2.0"]
    )

    for i in [3.5, 4.0, 4.5]:
        df_interpolation[str(i)] = df_interpolation["3.0"] + (i - 3) / (5 - 3) * (
            df_interpolation["5.0"] - df_interpolation["3.0"]
        )

    for i in [5.5, 6.0, 6.5]:
        df_interpolation[str(i)] = df_interpolation["5.0"] + (i - 5) / (7 - 5) * (
            df_interpolation["7.0"] - df_interpolation["5.0"]
        )

    for i in [7.5, 8.0, 8.5, 9.0, 9.5]:
        df_interpolation[str(i)] = df_interpolation["7.0"] + (i - 7) / (10 - 7) * (
            df_interpolation["10.0"] - df_interpolation["7.0"]
        )

    numbers = [x / 2 for x in range(21, 40)]
    for i in numbers:
        df_interpolation[str(i)] = df_interpolation["10.0"] + (i - 10) / (20 - 10) * (
            df_interpolation["20.0"] - df_interpolation["10.0"]
        )

    numbers = [x / 2 for x in range(41, 60)]
    for i in numbers:
        df_interpolation[str(i)] = df_interpolation["20.0"] + (i - 20) / (30 - 20) * (
            df_interpolation["30.0"] - df_interpolation["20.0"]
        )

    return df_interpolation
