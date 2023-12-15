import pandas as pd
from sklearn.decomposition import PCA
import os
import logging
from sklearn.model_selection import train_test_split

def splitting(X, y):
    ts = 0.30
    rs = 42
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=ts, random_state=rs)
    return [ts,rs,X_train,X_test,y_train,y_test]

def load_data(x_path, y_path):
    try:
        X = pd.read_csv(x_path)
        y = pd.read_csv(y_path)
        return X, y
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        raise

def perform_pca(X, n_components=2):
    pca = PCA(n_components=n_components)
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
    features_file_path = 'C:/Users/sayye/OneDrive/Desktop/college/PG/UPC/ADSDB/part2/featureGeneration/dataLabelling/df_ml_Xset.csv'
    labels_file_path = 'C:/Users/sayye/OneDrive/Desktop/college/PG/UPC/ADSDB/part2/featureGeneration/dataLabelling/df_ml_yset.csv'

    X, y = load_data(features_file_path, labels_file_path)

    ts, rs, X_train, X_test, y_train, y_test = splitting(X, y)

    X_train_pca, _ = perform_pca(X_train)
    X_test_pca, _ = perform_pca(X_test)

    save_transformed_data(X_train_pca, y_train, 'C:/Users/sayye/OneDrive/Desktop/college/PG/UPC/ADSDB/part2/advanceTopic/featureSelection/X_trainPCA.csv', 'C:/Users/sayye/OneDrive/Desktop/college/PG/UPC/ADSDB/part2/advanceTopic/featureSelection/y_train.csv')
    save_transformed_data(X_test_pca, y_test, 'C:/Users/sayye/OneDrive/Desktop/college/PG/UPC/ADSDB/part2/advanceTopic/featureSelection/X_testPCA.csv', 'C:/Users/sayye/OneDrive/Desktop/college/PG/UPC/ADSDB/part2/advanceTopic/featureSelection/y_test.csv')

if __name__ == "__main__":
    main()
