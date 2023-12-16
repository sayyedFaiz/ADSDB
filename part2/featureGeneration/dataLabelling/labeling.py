
import pandas as pd
import sys
sys.path.append("./")

def load_data(file_path):
    return pd.read_csv(file_path)

def separate_features_and_labels(df, label_column_name):
    X = df.drop(label_column_name, axis=1)
    y = df[label_column_name]
    return X, y

def save_data(df, file_path):
    df.to_csv(file_path, index=False)

def main():
    input_file_path = '../DataPreparation/df_data_preparation.csv'
    features_file_path = './df_ml_Xset.csv'
    labels_file_path = './df_ml_yset.csv'

    df_analysis = load_data(input_file_path)

    X, y = separate_features_and_labels(df_analysis, 'avg_rent')

    save_data(X, features_file_path)
    save_data(y, labels_file_path)

if __name__ == "__main__":
    main()


