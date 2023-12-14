import pandas as pd
import numpy as np
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR

from sklearn.model_selection import train_test_split

def splitting(X, y):
    ts = 0.30
    rs = 42
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=ts, random_state=rs)
    return [ts,rs,X_train,X_test,y_train,y_test]


def load_data(features_file_path, labels_file_path):
    X = pd.read_csv(features_file_path)
    y = pd.read_csv(labels_file_path)
    return X, y

def train_and_evaluate(ts, rs, models, X_train, y_train, X_test, y_test):
    results = []
    for model in models:
        model.fit(X_train, y_train.values.ravel())
        pred = model.predict(X_test)
        mape = mean_absolute_percentage_error(y_test, pred)
        results.append({
            'test_size':ts,
            'random_state_of_splitting':rs,
            'model': str(model),
            'hyperparameters': str(model.get_params()),
            'scoring_function':"mean_absolute_percentage_error",
            'error': str('{:.3f}'.format(mape))
        })
    return results

def remove_duplicates(models_info):
    unique_models = {model['model']: model for model in models_info}.values()
    return list(unique_models)

def store_results(results, file_path):
    try:
        with open(file_path, 'rb') as file:
            existing_results = pickle.load(file)
    except FileNotFoundError:
        existing_results = []

    existing_results.extend(results)
    unique_results = remove_duplicates(existing_results)
    with open(file_path, 'wb') as file:
        pickle.dump(unique_results, file)

def main():
    # Replace these paths with the paths where your input data is stored
    features_file_path = 'C:/Users/sayye/OneDrive/Desktop/college/PG/UPC/ADSDB/part2/featureGeneration/dataLabelling/df_ml_Xset.csv'
    labels_file_path = 'C:/Users/sayye/OneDrive/Desktop/college/PG/UPC/ADSDB/part2/featureGeneration/dataLabelling/df_ml_yset.csv'

    # Assuming the splitting function is already defined and accessible
    X, y = load_data(features_file_path, labels_file_path)
    ts, rs, X_train, X_test, y_train, y_test = splitting(X, y)
    # Define the models you want to train
    models = [
        DecisionTreeRegressor(random_state=42, max_depth=5, max_leaf_nodes=20),
        DecisionTreeRegressor(random_state=42, max_depth=10),
        KNeighborsRegressor(p=1, n_neighbors=5),
        KNeighborsRegressor(p=2, n_neighbors=5),
        KNeighborsRegressor(n_neighbors=7),
        LinearRegression(n_jobs=-1),
        SVR(kernel='poly', degree=1),
        SVR(kernel='poly', degree=2)
    ]

    # Train and evaluate models
    results = train_and_evaluate(ts, rs, models, X_train, y_train, X_test, y_test)

    # Store results
    store_results(results, 'C:/Users/sayye/OneDrive/Desktop/college/PG/UPC/ADSDB/part2/trainingAndValidation/trainingAndTesting/model_storing2.pkl')

if __name__ == "__main__":
    main()

