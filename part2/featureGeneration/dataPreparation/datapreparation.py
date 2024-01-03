import pandas as pd
import sys
sys.path.append("./")
from db_utils import (append_new_data_to_csv, load_data)


def one_hot_encode(df, column_name):
    one_hot = pd.get_dummies(df[column_name])
    df = df.drop(column_name, axis=1)
    df = df.join(one_hot)
    return df


def main():
    if len(sys.argv) < 2:
        input_file_path = 'featureGeneration/featureGeneration/df_feature_generation.csv'
        output_file_path = 'featureGeneration/dataPreparation/df_data_preparation.csv'
        flag = 0
    else:
        input_file_path = 'featureGeneration/featureGeneration/test_row.csv'
        flag = 1

    df_analysis = load_data(input_file_path)
    # One-hot encode 'Income_Group' with a prefix for the column names
    df_analysis = one_hot_encode(df_analysis, 'Income_Group')
    df_analysis.rename(columns={'Low': 'Income_group_Low', 'Medium-Low': 'Income_group_Medium-Low',
                                'Medium': 'Income_group_Medium','Medium-High': 'Income_group_Medium-High',
                                'High': 'Income_group_High'}, inplace=True)

    # One-hot encode 'district' with a prefix for the column names
    df_analysis = one_hot_encode(df_analysis, 'district')
    df_analysis.rename(columns={'les corts': 'les corts_district', 'sant andreu': 'sant andreu_district'}, inplace=True)

    # One-hot encode 'neighbourhood' with no prefix (since the neighbourhood names are unique)
    df_analysis = one_hot_encode(df_analysis, 'neighbourhood')
    if flag == 1:
        input_hist_path = 'featureGeneration/dataPreparation/df_data_preparation.csv'
        df_hist = load_data(input_hist_path)
        cols_dif = df_hist.columns.difference(df_analysis.columns)
        for col in cols_dif:
            df_analysis[col] = 0
    df_analysis.to_csv('featureGeneration/featureGeneration/test_row.csv', index=False)
    if len(sys.argv) < 2:
        unique_columns = ['year', 'Income', 'avg_rent']
        append_new_data_to_csv(df_analysis, output_file_path, unique_columns)


if __name__ == "__main__":
    main()
