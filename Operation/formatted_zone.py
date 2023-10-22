import pandas as pd
import duckdb
import os
import sys
dataframes = {}

# List all CSV files in the folder
csvFolderPath = 'C:/Users/sayye/OneDrive/Desktop/college/PG/UPC/ADSDB/landing/persistent'

def formattedZone(path) :

    csv_files = [file for file in os.listdir(path) if file.endswith('.csv')]
    # Iterate through the CSV files and read them into DataFrames
    for csv_file in csv_files:
        # Generate a DataFrame name based on the file name without the extension
        dataframe_name = os.path.splitext(csv_file)[0]

        # Read the CSV file into a DataFrame and store it in the dictionary
        dataframes[dataframe_name] = pd.read_csv(os.path.join(path, csv_file))

    connection= duckdb.connect(database='C:/Users/sayye/OneDrive/Desktop/college/PG/UPC/ADSDB/formatted/formatted.db')

    # Iterate through the DataFrames and save them to the database
    for dataset_name, dataset_df in dataframes.items():
        # Register the DataFrame as a DuckDB table
        connection.register(dataset_name, dataset_df)
        create_table_query = f'CREATE TABLE {dataset_name} AS SELECT * FROM {dataset_name}'
        connection.execute(create_table_query)

    connection.commit()

    # Define the SQL query to retrieve table names
    query = "SELECT name FROM sqlite_master WHERE type='table';"

    # Execute the query and fetch the results
    result = connection.execute(query)

    # Fetch all table names from the result set
    table_names = [row[0] for row in result.fetchall()]

    for table_name in table_names:
        # Get the column names
        query_columns = f"PRAGMA table_info('{table_name}');"
        # print(table_name)
        result_columns = connection.execute(query_columns)
        column_names = [row[1] for row in result_columns.fetchall()]

        # Get the first 5 rows of the table
        query_data = f"SELECT * FROM {table_name} LIMIT 5;"
        result_data = connection.execute(query_data)
        data = result_data.fetchall()

    result = connection.execute('SHOW TABLES')
    tables = result.fetchall()

    # Loop through and print the names of all tables
    for table in tables:
        table_name = table[0]
        print(f'Table Name: {table_name}')
        query_columns = f"PRAGMA table_info('{table_name}');"
        result_columns = connection.execute(query_columns)
        column_names = [row[1] for row in result_columns.fetchall()]
        print(column_names)
    connection.close()


formattedZone(csvFolderPath)