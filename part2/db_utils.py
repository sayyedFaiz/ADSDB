import duckdb
import pandas as pd
from pathlib import Path


def connect_to_database(db_name):
    return duckdb.connect(database=db_name)


def close_database_connection(con):
    con.close()


def fetch_data_from_table(con, table_name):
    query = f"SELECT * FROM {table_name};"
    return pd.read_sql_query(query, con)


def append_new_data_to_csv(new_data, file_path):
    # Check if the file exists
    if Path(file_path).is_file():
        existing_data = pd.read_csv(file_path)
        combined_data = pd.concat([existing_data, new_data], ignore_index=True)
        combined_data_unique = combined_data.astype('str').drop_duplicates(subset=None, keep="first", inplace=False)
        # Overwrite the file with the unique data
        combined_data_unique.to_csv(file_path, index=False, header=True)
        print("File updated with unique rows.")
    else:
        # If the file does not exist, create it and write the new data
        new_data.to_csv(file_path, index=False, header=True)
        print("File created and data written.")

    return new_data
