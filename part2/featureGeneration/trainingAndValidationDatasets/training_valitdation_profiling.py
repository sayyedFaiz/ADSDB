import os
import pandas as pd
import sys
sys.path.append('../../')
from machine_learning_utils import splitting

def main():
    # Replace these paths with the paths where your input data is stored
    features_file_path = '../dataLabelling/df_ml_Xset.csv'
    labels_file_path = '../dataLabelling/df_ml_yset.csv'

    # Load datasets
    X = pd.read_csv(features_file_path)
    y = pd.read_csv(labels_file_path)


    # Splitting the dataset
    ts, rs, X_train, X_test, y_train, y_test = splitting(X, y)

    # Print Training Dataset Schema and Profile
    print("Training Dataset Schema:")
    print(X_train.iloc[:,:10].dtypes)  # Features
    print('\nTarget variable:')
    print(y_train.dtypes)  # Target variable

    print("\nTraining Dataset Profile:")
    print(X_train.iloc[:,:10].describe())  # Descriptive statistics for features
    print('\nTarget variable:')
    print(y_train.describe())  # Descriptive statistics for target variable

    # Print Validation Dataset Schema and Profile
    print("\nValidation Dataset Schema:")
    print(X_test.iloc[:,:10].dtypes)  # Features
    print('\nTarget variable:')
    print(y_test.dtypes)  # Target variable

    print("\nValidation Dataset Profile:")
    print(X_test.iloc[:,:10].describe())  # Descriptive statistics for features
    print('\nTarget variable:')
    print(y_test.describe())  # Descriptive statistics for target variable

if __name__ == "__main__":
    main()
