import pandas as pd
import sys
sys.path.append("./")

from sklearn.model_selection import train_test_split

from db_utils import load_data

from machine_learning_utils import splitting


def print_dataset_info(X_train, X_test, y_train, y_test):
    print("Training Dataset Schema:")
    print(X_train.dtypes)  # Features
    print('\n')
    print('Target variable:')
    print(y_train.dtypes)  # Target variable

    print("\nTraining Dataset Profile:")
    print('\n')
    print('Target variable:')
    print(X_train.describe())  # Descriptive statistics for features
    print(y_train.describe())  # Descriptive statistics for target variable

    print("Validation Dataset Schema:")
    print(X_test.dtypes)  # Features
    print('\n')
    print('Target variable:')
    print(y_test.dtypes)  # Target variable

    # Profile of Validation Dataset
    print("\nValidation Dataset Profile:")
    print(X_test.describe())  # Descriptive statistics for features
    print('\n')
    print('Target variable:')
    print(y_test.describe())  # Descriptive statistics for target variable

def main():
    # Replace these paths with the paths where your input data is stored
    features_file_path = 'featureGeneration/dataLabelling/df_ml_Xset.csv'
    labels_file_path = 'featureGeneration/dataLabelling/df_ml_yset.csv'
    X = load_data(features_file_path)
    y = load_data(labels_file_path)
    ts, rs, X_train, X_test, y_train, y_test = splitting(X, y)

    print_dataset_info(X_train, X_test, y_train, y_test)

if __name__ == "__main__":
    main()


