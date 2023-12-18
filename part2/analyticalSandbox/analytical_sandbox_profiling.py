import duckdb
import pandas as pd
import sys

sys.path.append("../")

from db_utils import connect_to_database, close_database_connection


def connect_to_database(db_path):
    try:
        con = duckdb.connect(database=db_path)
        return con
    except Exception as e:
        print(f"Error connecting to database: {e}")
        raise


def execute_query(con, query):
    try:
        result = con.execute(query)
        return result
    except Exception as e:
        print(f"Error executing query: {e}")
        raise


def get_table_schema(con, table_name):
    schema_query = f"SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table_name}'"
    schema_data = execute_query(con, schema_query).fetchall()
    schema_df = pd.DataFrame(schema_data, columns=["Column_Name", "Data_Type"])
    print("Schema:")
    print(schema_df)
    return schema_df


def profile_data(con, table_name, schema_df):
    profile_query = f"SELECT * FROM {table_name} LIMIT 5"
    profile_data = execute_query(con, profile_query).fetchall()
    profile_df = pd.DataFrame(profile_data, columns=schema_df["Column_Name"].tolist())
    print("\nProfile (first 5 rows):")
    print(profile_df)


def summarize_data(con, table_name):
    summary_query = f"SUMMARIZE SELECT * FROM '{table_name}'"
    summary_data = execute_query(con, summary_query).fetchall()
    print("Summary:")
    print(
        "column_name, column_type, min, max, approx_unique, avg, std, q25, q50, q75, count, null_percentage"
    )
    for sd in summary_data:
        print(sd)


def main():
    db_path = "analytical_sandboxes.db"
    table_name = "sandbox"

    con = connect_to_database(db_path)

    # Alter table queries
    alter_queries = [
        f"ALTER TABLE {table_name} ALTER COLUMN Income SET NOT NULL;",
        f"ALTER TABLE {table_name} ALTER COLUMN district SET NOT NULL;",
        f"ALTER TABLE {table_name} ALTER COLUMN neighbourhood SET NOT NULL;",
        f"ALTER TABLE {table_name} ALTER COLUMN year SET NOT NULL;",
    ]

    for query in alter_queries:
        execute_query(con, query)

    # Describing the schema
    schema_query = f"DESCRIBE SELECT * FROM '{table_name}'"
    schema_data = execute_query(con, schema_query).fetchall()
    print("Describe:")
    print("column_name, column_type, null, key, default, extra")
    for sd in schema_data:
        print(sd)

    # Get and print the table schema
    schema_df = get_table_schema(con, table_name)

    # Profile the data
    profile_data(con, table_name, schema_df)

    # Summarize the data
    summarize_data(con, table_name)

    close_database_connection(con)


if __name__ == "__main__":
    main()
