import pandas as pd
import duckdb
import os
import sys
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style='whitegrid')
def getTables():
    trustedDatabasePath = 'C:/Users/sayye/OneDrive/Desktop/college/PG/UPC/ADSDB/trusted/trusted.db'
    connection = duckdb.connect(database=trustedDatabasePath)
    result = connection.execute('SHOW TABLES')
    tables = [table[0] for table in result.fetchall()]

    return connection, tables


def checkDuplicate():
    connection, tables = getTables()
    for table in tables:
        # print(table_name)
        check_duplicates_query = f'''
            SELECT *
            FROM {table}
            GROUP BY {', '.join([f'"{col}"' for col in connection.table(table).columns])}
            HAVING COUNT(*) > 1;
        '''
        # Execute the query to find duplicate rows
        result = connection.execute(check_duplicates_query)

        # Fetch the duplicate rows
        duplicate_rows = result.fetchall()

        # Print the duplicate rows
        if duplicate_rows:
            print("Duplicate Rows:")
            for row in duplicate_rows:
                print(row)
        else:
            print("No duplicate rows found.")
    connection.close()

# checkDuplicate()

# In our case both the tables didnt have an unique Identifier so here we are adding an ID column to both the tables. (Optional)
def addIDColumn():
    connection, tables = getTables()
    for table in tables:
        # Check if the 'id' column already exists in the table
        check_column_query = f'SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME=\'{table}\' AND COLUMN_NAME=\'id\''
        existing_columns = connection.execute(check_column_query).fetchall()
        # If 'id' column does not exist, add it
        if not existing_columns:
        # Add a new column 'id' with INTEGER data type
            alter_query = f'ALTER TABLE {table} ADD id INTEGER;'
            connection.execute(alter_query)
            # # Update the 'id' column with unique values for each row
            update_query = f'UPDATE {table}  SET id = rowid +1;'
            connection.execute(update_query)
            # # Commit changes
            connection.commit()
        # print the column names
        query_columns = f"PRAGMA table_info('{table}');"
        result_columns = connection.execute(query_columns)
        column_names = [row[1] for row in result_columns.fetchall()]
        print("Column Names:",column_names)
    # Close the connection
    connection.close()

# addIDColumn()

def dataStatistics():
    connection, tables = getTables()
    # print(tables)
    for table in tables:
        query = f'SELECT * FROM {table};'
        df = pd.read_sql_query(query, connection)
        print("TABLE NAME",table)
        print(df.head())
        # Number of Unique Values in Each Column
        unique_counts = df.nunique()
        for column_name, count in unique_counts.items():
            print(f"Column '{column_name}': {count} unique values")
            unique_values = df[column_name].unique()
            print("Unique Values:", unique_values)
            print()
        # Missing Values (Null Values) Count in Each Column
        missing_values = df.isnull().sum()
        print("MISSING VALUES:\n",missing_values)
# dataStatistics()



# This is very project specific however by just changing few variables one get similar results
def dataVisualization():
    connection, tables = getTables()
    income , rents = tables[0], tables[1]
    query = f'SELECT * FROM {income};'
    df_income = pd.read_sql_query(query, connection)
    query = f'SELECT * FROM {rents};'
    df_rents = pd.read_sql_query(query, connection)
    df_income['Nom_Districte'] = df_income['Nom_Districte'].str.replace("L'Eixample", 'Eixample')

    # FOR INCOME TABLE
    plt.figure(figsize=(8, 6))
    sns.barplot(x='Nom_Districte', y='Import_Renda_Bruta_', data=df_income, errorbar=None)
    plt.title('Income  by District')
    plt.xlabel('Codi_Districte')
    plt.ylabel('Income per District')
    plt.xticks(rotation=90)
    plt.show()

    plt.figure(figsize=(8, 6))
    sns.barplot(x='Any', y='Import_Renda_Bruta_', data=df_income, errorbar=None)
    plt.title('Income per year')
    plt.xlabel('Year')
    plt.ylabel(' Income per year')
    plt.show()

    plt.figure(figsize=(20, 6))
    sns.barplot(x='Nom_Barri', y='Import_Renda_Bruta_', data=df_income, errorbar=None)
    plt.title(' Income per neighborhood')
    plt.xlabel('Neighborhood')
    plt.ylabel('Income')
    plt.xticks(rotation=90)
    plt.show()

    # FOR RENTS TABLE
    plt.figure(figsize=(8, 6))
    sns.barplot(x='District', y='Price', data=df_rents, errorbar=None)
    plt.title('Average Rent per person by District')
    plt.xlabel('District')
    plt.ylabel('Average Rent per District')
    plt.xticks(rotation=90)
    plt.show()

    plt.figure(figsize=(8, 6))
    sns.barplot(x='Year', y='Price', data=df_rents, errorbar=None)
    plt.title('Average rent per person per person per year')
    plt.xlabel('Year')
    plt.ylabel('Average rent')
    plt.show()

    plt.figure(figsize=(20, 6))
    sns.barplot(x='Neighbourhood', y='Price', data=df_rents, errorbar=None)
    plt.title('Average rent per person per neighborhood')
    plt.xlabel('Neighbourhood')
    plt.ylabel('Average rent')
    plt.xticks(rotation=90)
    plt.show()
dataVisualization()