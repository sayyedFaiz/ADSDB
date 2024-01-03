import pandas as pd
import duckdb
import os
import sys

formattedDatabasePath = 'C:/Users/sayye/OneDrive/Desktop/college/PG/UPC/ADSDB/formatted/formatted.db'

def mergeFormattedTable(path):
    connection = duckdb.connect(database=path)
    result = connection.execute('SHOW TABLES')
    tables = result.fetchall()

    table_words = []
    for table in tables:
        table_words.append(table[0].split('_')[0])
    tbl_words = list(set(table_words))
    # print(tbl_words)
    table_groups = {}

    # Group tables based on common prefixes
    for table in tables:
        table_name = table[0]
        prefix = table_name.split('_')[0]
        if prefix not in table_groups:
            table_groups[prefix] = []
        table_groups[prefix].append(table_name)
    # print(table_groups)

    # Create a dictionary to store the merged data
    merged_data = {}

    # Merge the tables in each group using UNION ALL
    for prefix, tables in table_groups.items():
        query = " UNION ALL ".join([f"SELECT * FROM {table}" for table in tables])
        result = connection.execute(query)
        # Retrieve column names for the first table
        column_names = result.description
        # Store the merged data and column names in the dictionary
        merged_data[prefix] = {
            'data': result.fetchall(),
            'columns': column_names
        }
    return merged_data

trustedDatabasePath = 'C:/Users/sayye/OneDrive/Desktop/college/PG/UPC/ADSDB/trusted/trusted.db'

merged_data = mergeFormattedTable(formattedDatabasePath)

def createTrustedDB(path, mergeData):
    connection = duckdb.connect(database=path)
    for table_name, data_with_columns in mergeData.items():
        # Check if the table already exists
        check_table_query = f'SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE table_name=\'{table_name}\''
        existing_tables = connection.execute(check_table_query).fetchall()
        # If the table does not exist, create it
        if not existing_tables:
            if data_with_columns:
                data = data_with_columns['data']
                column_names = [f'"{col[0].strip()}"'.replace(' ', '_').replace('€', '') for col in data_with_columns['columns']]
                # print(column_names)
                lst = merged_data[table_name]['columns']
                dtypes = [lis[1] for lis in lst]
            for d,y in zip(dtypes,data[0]):
                if d=='NUMBER':
                    ind = dtypes.index(d)
                    if isinstance(y, int):
                        dtypes[ind]='INT'
                    else:
                        dtypes[ind]='NUMERIC'
                    # Create the table with the properly formatted column names
            column_definitions = ", ".join([f'{col} {dtype}' for col,dtype in zip(column_names, dtypes)])
            create_table_query = f'CREATE TABLE {table_name} ({column_definitions})'
            createTable = connection.execute(create_table_query)

                # Insert data into the new table using parameterized queries
            for row in data:
                insert_query = f'INSERT INTO {table_name} VALUES ({", ".join(["?"] * len(row))})'
                connection.execute(insert_query, row)

    result = connection.execute('SHOW TABLES')
    tables = [table[0] for table in result.fetchall()]
    print("Created Tables:",tables)

    # Close the database connection
    connection.close()

createTrustedDB(trustedDatabasePath, merged_data)

