
import pandas as pd
import sys
sys.path.append("./")

from db_utils import (append_new_data_to_csv, load_data)

def separate_features_and_labels(df, label_column_name):
    X = df.drop(label_column_name, axis=1)
    y = df[label_column_name]
    return X, y


def main():
    input_file_path = 'featureGeneration/DataPreparation/df_data_preparation.csv'
    features_file_path = 'featureGeneration/dataLabelling/df_ml_Xset.csv'
    labels_file_path = 'featureGeneration/dataLabelling/df_ml_yset.csv'

    df_analysis = load_data(input_file_path)

    X, y = separate_features_and_labels(df_analysis, 'avg_rent')
    # print(y.name)
    append_new_data_to_csv(X, features_file_path, ['Income', 'year'])
    append_new_data_to_csv(y, labels_file_path, ['avg_rent'])

if __name__ == "__main__":
    main()


