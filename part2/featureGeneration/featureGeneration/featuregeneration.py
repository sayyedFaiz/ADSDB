import duckdb
import pandas as pd
import sys
import warnings


sys.path.append("./")
from db_utils import (
    connect_to_database,
    close_database_connection,
    fetch_data_from_table,
    append_new_data_to_csv
)

warnings.filterwarnings('ignore')


def calculate_avg_rent(df):
    # Group by 'neighbourhood' and 'year', calculate the mean of 'avg_rent' for each group
    neighborhood_avg_rent = (
        df.groupby(["neighbourhood", "year"])["avg_rent"].mean().reset_index()
    )

    # Fill NaN values in 'avg_rent' based on the average rent of the same neighborhood in different years
    df["avg_rent"] = df.apply(
        lambda row: neighborhood_avg_rent.loc[
            (neighborhood_avg_rent["neighbourhood"] == row["neighbourhood"])
            & (neighborhood_avg_rent["year"] != row["year"])
        ]["avg_rent"].mean()
        if pd.isna(row["avg_rent"])
        else row["avg_rent"],
        axis=1,
    )

    df = df.dropna(subset=["avg_rent"])
    return df


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


def main():
    if len(sys.argv) >= 2:
        income = [float(sys.argv[1])]
        district = [sys.argv[2]]
        neighbourhood = [sys.argv[3]]
        year = [int(sys.argv[4])]
        test = int(sys.argv[5])
        row = {"Income": income, "district": district, "neighbourhood": neighbourhood, "year": year}
        if test == 1:
            df_analysis = pd.DataFrame(row)
            df_analysis = calculate_district_income_variability(df_analysis)
            df_analysis = categorize_income_group(df_analysis)
            df_hist = pd.read_csv("featureGeneration/featureGeneration/df_feature_generation.csv")
            t = df_hist.query(f"district=={district} | neighbourhood=={neighbourhood}")["District_Income_Variability"]
            df_analysis['District_Income_Variability'] = t.iloc[0]
            df_analysis.to_csv('featureGeneration/featureGeneration/test_row.csv', index=False)
    else:
        con = connect_to_database("analyticalSandbox/analytical_sandboxes.db")
        df_analysis = fetch_data_from_table(con, "sandbox")
        # df_analysis = calculate_avg_rent(df_analysis)
        # df_analysis = calculate_income_rent_ratio(df_analysis)
        # df_analysis = calculate_district_average_rent(df_analysis)
        df_analysis = calculate_district_income_variability(df_analysis)
        df_analysis = categorize_income_group(df_analysis)

        unique_columns = ['district', 'neighbourhood', 'year']

        append_new_data_to_csv(df_analysis, "featureGeneration/featureGeneration/df_feature_generation.csv",unique_columns)

        close_database_connection(con)


if __name__ == "__main__":
    main()
