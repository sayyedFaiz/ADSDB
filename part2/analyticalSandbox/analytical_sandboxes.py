import duckdb
import pandas as pd
import sys
sys.path.append('./')
from db_utils import (connect_to_database, close_database_connection, fetch_data_from_table)

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



# def create_new_table_from_df(con, df, table_name):
#     con.register('temp_table', df)
#     query = f"CREATE TABLE {table_name} AS SELECT * FROM temp_table;"
#     con.execute(query)
#     con.unregister('temp_table')

def create_new_table_from_df(con, df, table_name, unique_columns):
    # Register the DataFrame as a virtual table in DuckDB
    con.register('temp_table', df)

    # Check if the table already exists
    if not con.execute(f"SELECT * FROM information_schema.tables WHERE table_name = '{table_name}'").fetchone():
        # If the table doesn't exist, create a new table from the virtual table
        con.execute(f"CREATE TABLE {table_name} AS SELECT * FROM temp_table")
        print(f"Table {table_name} created.")
    else:
        # If the table exists, append the data into the existing table
        con.execute(f"INSERT INTO {table_name} SELECT * FROM temp_table")
        print(f"Data appended to table {table_name}.")
        # Now remove duplicates
        # Assuming 'unique_columns' is a list of column names that uniquely identify a row
        unique_cols = ', '.join(unique_columns)
        deduplicate_query = f"""
        CREATE TEMPORARY TABLE deduped_temp AS
        SELECT DISTINCT ON ({unique_cols}) *
        FROM {table_name}
        ORDER BY {unique_cols};

        DELETE FROM {table_name};

        INSERT INTO {table_name}
        SELECT * FROM deduped_temp;

        DROP TABLE deduped_temp;
        """
        con.execute(deduplicate_query)
        print(f"Removed duplicates from table {table_name}.")

    # Unregister the virtual table to clean up namespace
    con.unregister('temp_table')


# append to the tables if it exist or else create

def retrieve_schema_and_profile(con, table_name):
    schema_query = f"SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'"
    schema_result = con.execute(schema_query).fetchall()
    schema_df = pd.DataFrame(schema_result, columns=['Column_Name', 'Data_Type'])

    profile_query = f"SELECT * FROM {table_name} LIMIT 5"
    profile_data = con.execute(profile_query).fetchall()
    profile_df = pd.DataFrame(profile_data, columns=schema_df['Column_Name'].tolist())

    return schema_df, profile_df

def main():
    con = connect_to_database('analyticalSandbox/exploitationdb24-11.db')

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
    close_database_connection(con)

    unique_columns = ['district', 'neighbourhood', 'year']
    con = connect_to_database('analyticalSandbox/analytical_sandboxes.db')
    create_new_table_from_df(con, df_analysis, 'sandbox', unique_columns)
    schema_df, profile_df = retrieve_schema_and_profile(con, 'sandbox')
    close_database_connection(con)

    # print("Schema:", schema_df)
    # print("\nProfile (first 5 rows):", profile_df)


if __name__ == "__main__":
    main()
