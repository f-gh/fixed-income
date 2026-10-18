import requests
import pandas as pd
from io import StringIO
from datetime import datetime
from pathlib import Path

# Clean up the dataframe and save it as csv
def cleanup_yields(df: pd.DataFrame) -> pd.DateFrame:
    df = df.drop(columns=["Id", "BC_30YEARDISPLAY"], errors="ignore")

    df["NEW_DATE"] = pd.to_datetime(df["NEW_DATE"])

    yield_columns = [
        column for column in df.columns
        if column.startswith("BC_")
    ]

    df[yield_columns] = (df[yield_columns] / 100).round(4)

    df = df.rename(columns={
        "NEW_DATE": "date"
    })

    df = df.rename(
        columns=lambda col: col.removeprefix("BC_")
    )

    return df


def main():
    # Request data for the current month in YYYYMM format
    MONTH = datetime.now().strftime("%Y%m")

    URL = "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/pages/xmlview"

    params = {
        "data": "daily_treasury_yield_curve",
        "field_tdr_date_value_month": MONTH,
    }

    response = requests.get(URL, params=params, timeout=30)
    response.raise_for_status()

    # Parse the XML response into a dataframe
    namespaces = {
        "m": "http://schemas.microsoft.com/ado/2007/08/dataservices/metadata",
        "d": "http://schemas.microsoft.com/ado/2007/08/dataservices",
    }

    df = pd.read_xml(
        StringIO(response.text),
        xpath=".//m:properties",
        namespaces=namespaces,
        parser="etree",
    )


    df = cleanup_yields(df)

    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
    OUTPUT_DIR = PROJECT_ROOT / "data" / "raw"

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_file = OUTPUT_DIR / f"treasury_yields_{MONTH}.csv"
    df.to_csv(output_file, index=False)
    print(f"Saved {len(df)} rows to {output_file}")


if __name__ == "__main__":
    main()