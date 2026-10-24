# bootstrap treasury's constant maturity yield curve

# initialize a new dataframe for bootstraping

def create_bootstrap_df(df: pd.DataFrame) -> pd.DataFrame:  
    df_bootstrap = df.rename(columns={
        "6MONTH": "0.5"
    })
    
    df_bootstrap = df_bootstrap.rename(
        columns=lambda col: col.removesuffix("YEAR")
    )

    df_bootstrap = df_bootstrap.rename(columns={
        col: str(float(col))
        for col in df_bootstrap.columns
        if col != "date"
    })
    
    for i in range(3, 60):
        if str(i/2) not in df_bootstrap.columns:
            df_bootstrap[str(i / 2)] = np.nan
    
    maturity_cols = [col for col in df_bootstrap.columns if col != "date"]
    
    maturity_cols = sorted(maturity_cols, key=float)
    
    df_bootstrap = df_bootstrap[["date"] + maturity_cols]

    return df_bootstrap


def main() -> None:
    df_bootstrap = create_bootstrap_df(df)

if __name__ == "__main__":
    main()
    