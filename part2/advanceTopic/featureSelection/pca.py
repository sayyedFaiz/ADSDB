import pandas as pd
from sklearn.decomposition import PCA
import os
import logging
import sys
sys.path.append('./')
from machine_learning_utils import (splitting)
from db_utils import load_data


def perform_pca(X, n_components=2):
    pca = PCA(n_components=n_components, random_state=42)
    X_pca = pca.fit_transform(X)
    explained_variance = pca.explained_variance_ratio_
    return X_pca, explained_variance


def save_transformed_data(X, y, x_path, y_path):
    try:
        pd.DataFrame(X).to_csv(x_path, index=False)
        pd.DataFrame(y).to_csv(y_path, index=False)
    except Exception as e:
        logging.error(f"Error saving data: {e}")
        raise


def main():
    features_file_path = 'featureGeneration/dataLabelling/df_ml_Xset.csv'
    labels_file_path = 'featureGeneration/dataLabelling/df_ml_yset.csv'

    X = load_data(features_file_path)
    y = load_data(labels_file_path)

    ts, rs, X_train, X_test, y_train, y_test = splitting(X, y)
    X_train_pca, _ = perform_pca(X_train)
    X_test_pca, _ = perform_pca(X_test)

    save_transformed_data(X_train_pca, y_train, 'advanceTopic/featureSelection/X_trainPCA.csv', 'advanceTopic/featureSelection/y_train.csv')
    save_transformed_data(X_test_pca, y_test, 'advanceTopic/featureSelection/X_testPCA.csv', 'advanceTopic/featureSelection/y_test.csv')


if __name__ == "__main__":
    main()
