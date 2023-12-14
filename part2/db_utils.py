import duckdb
import pandas as pd

def connect_to_database(db_name):
    return duckdb.connect(database=db_name)

def close_database_connection(con):
    con.close()

def fetch_data_from_table(con, table_name):
    query = f'SELECT * FROM {table_name};'
    return pd.read_sql_query(query, con)
