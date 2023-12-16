import duckdb
import pandas as pd
import sys

sys.path.append("../../")
from db_utils import (
    connect_to_database,
    close_database_connection,
    fetch_data_from_table,
)


def calculate_income_rent_ratio(df):
    df["Income_Rent_Ratio"] = df["Income"] / df["avg_rent"]
    return df


def calculate_district_average_rent(df):
    df["District_Avg_Rent"] = df.groupby(["district", "year"])["avg_rent"].transform(
        "mean"
    )
    return df


def calculate_district_income_variability(df):
    df["District_Income_Variability"] = df.groupby("district")["Income"].transform(
        "std"
    )
    return df


def categorize_income_group(df):
    bins = [0, 10000, 20000, 30000, 40000, float("inf")]
    labels = ["Low", "Medium-Low", "Medium", "Medium-High", "High"]
    df["Income_Group"] = pd.cut(df["Income"], bins=bins, labels=labels)
    return df


def save_data(df, file_name):
    df.to_csv(file_name, index=False)


def main():
    con = connect_to_database("../../analyticalSandbox/analytical_sandboxes.db")
    df_analysis = fetch_data_from_table(con, "sandbox")

    df_analysis = calculate_income_rent_ratio(df_analysis)
    df_analysis = calculate_district_average_rent(df_analysis)
    df_analysis = calculate_district_income_variability(df_analysis)
    df_analysis = categorize_income_group(df_analysis)

    save_data(df_analysis, "df_feature_generation.csv")

    close_database_connection(con)


if __name__ == "__main__":
    main()
