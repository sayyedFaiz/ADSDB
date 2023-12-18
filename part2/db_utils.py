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

def load_data(file_path):
    try:
       return pd.read_csv(file_path)
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        raise


def append_new_data_to_csv(new_data, file_path, unique_columns):
    # Generate a unique_id only if there is more than one unique column
    print(unique_columns)
    if len(unique_columns) > 1:
        new_data["unique_id"] = new_data[unique_columns].apply(
            lambda row: "_".join(row.values.astype(str)), axis=1
        )
    else:
        unique_data = new_data.to_frame(name="unique_value")
        unique_data["unique_id"] = unique_data["unique_value"].astype(str)
    if Path(file_path).is_file():
        # Read the existing data
        existing_data = pd.read_csv(file_path)
        if len(unique_columns) > 1:
            # Filter out duplicates
            existing_data["unique_id"] = existing_data[unique_columns].apply(
                lambda row: "_".join(row.values.astype(str)), axis=1
            )
            unique_new_data = new_data[
                ~new_data["unique_id"].isin(existing_data["unique_id"])
            ].drop(columns=["unique_id"])
        else:
            existing_data["unique_id"] = existing_data[unique_columns].astype(str)
            unique_new_data = unique_data[
                ~unique_data["unique_id"].isin(existing_data["unique_id"])
            ].drop(columns=["unique_id"])

        if not unique_new_data.empty:
            unique_new_data.to_csv(file_path, mode="a", index=False, header=False)
            print("New unique rows appended.")
        else:
            print("No new unique rows to append.")
    else:
        new_data.drop(columns=["unique_id"]).to_csv(file_path, index=False)
        print("File created and data written.")

    return new_data
