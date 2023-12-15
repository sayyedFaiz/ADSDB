import duckdb
import pandas as pd
import sys
sys.path.append('C:/Users/sayye/OneDrive/Desktop/college/PG/UPC/ADSDB/part2/')
from db_utils import connect_to_database, close_database_connection, fetch_data_from_table

def merge_tables(df1, df2, left_on, right_on):
    return pd.merge(df1, df2, left_on=left_on, right_on=right_on, how="inner")


def compute_average_rent(df):
    df_grouped = (
        df.groupby(["year", "district", "neighbourhood"])["avg_rent"]
        .mean()
        .reset_index()
    )
    return df_grouped


def prepare_final_dataset(income_df, rent_df):
    df_analysis = pd.merge(
        income_df, rent_df, on=["year", "district", "neighbourhood"], how="left"
    )
    neighborhood_avg_rent = df_analysis.groupby(['neighbourhood', 'year'])['avg_rent'].mean().reset_index()

    # Fill NaN values in 'avg_rent' based on the average rent of the same neighborhood in different years
    df_analysis['avg_rent'] = df_analysis.apply(
        lambda row: neighborhood_avg_rent.loc[
            (neighborhood_avg_rent['neighbourhood'] == row['neighbourhood']) &
            (neighborhood_avg_rent['year'] != row['year'])
        ]['avg_rent'].mean() if pd.isna(row['avg_rent']) else row['avg_rent'],
    axis=1
)
    return df_analysis.dropna(subset=["avg_rent"])

def create_new_table_from_df(con, df, table_name):
    query = f"CREATE TABLE {table_name} AS SELECT * FROM df_analysis;"
    con.execute(query)

def retrieve_schema_and_profile(con, table_name):
    schema_query = f"SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'"
    schema_result = con.execute(schema_query).fetchall()
    schema_df = pd.DataFrame(schema_result, columns=['Column_Name', 'Data_Type'])

    profile_query = f"SELECT * FROM {table_name} LIMIT 5"
    profile_data = con.execute(profile_query).fetchall()
    profile_df = pd.DataFrame(profile_data, columns=schema_df['Column_Name'].tolist())

    return schema_df, profile_df

def main():
    con = connect_to_database('exploitationdb24-11.db')

    df_income = fetch_data_from_table(con, 'income')
    df_rents = fetch_data_from_table(con, 'rent')
    df_area = fetch_data_from_table(con, 'area')
    df_trim = fetch_data_from_table(con, 'trimester')
    df_year = fetch_data_from_table(con, 'year')

    result_df = merge_tables(df_rents, df_area, 'AreaID', 'id')
    result_df = merge_tables(result_df, df_trim, 'TrimesterID', 'id')
    rents_sandbox = compute_average_rent(result_df)

    result_df = merge_tables(df_income, df_area, 'AreaID', 'id')
    result_df = merge_tables(result_df, df_year, 'YearID', 'id')
    income_sandbox = result_df[['Income', 'district', 'neighbourhood', 'year']]

    df_analysis = prepare_final_dataset(income_sandbox, rents_sandbox)

    create_new_table_from_df(connect_to_database('analytical_sandboxes.db'), df_analysis, 'sandbox')

    schema_df, profile_df = retrieve_schema_and_profile(connect_to_database('analytical_sandboxes.db'), 'sandbox')
    print("Schema:", schema_df)
    print("\nProfile (first 5 rows):", profile_df)

    close_database_connection(con)

if __name__ == "__main__":
    main()
