
def construct_curve(df):
    r_1 = df.loc[df["maturity"] == 1, "par_yield"].iloc[0]
    r_2 = df.loc[df["maturity"] == 2, "par_yield"].iloc[0]
    r_3 = df.loc[df["maturity"] == 3, "par_yield"].iloc[0]

    df_1 = 1 / (1 + r_1)
    df_2 = (1 - r_2 * df_1) / (1 + r_2)
    df_3 = (1 - r_3 * df_1 - r_3 * df_2) / (1 + r_3)

    return df_1, df_2, df_3


def discount_factor(rate, maturity):
    if maturity < 0:
        raise ValueError("Maturity cannot be negative")
        
    return 1/(1 + rate)**maturity

