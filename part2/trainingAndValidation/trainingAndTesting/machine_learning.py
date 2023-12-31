import sys
import pickle

sys.path.append("./")
from db_utils import load_data
from machine_learning_utils import (splitting, train_and_evaluate, store_results, train_only_best)


def main():
    if len(sys.argv) < 2:
        # Replace these paths with the paths where your input data is stored
        features_file_path = "featureGeneration/dataLabelling/df_ml_Xset.csv"
        labels_file_path = "featureGeneration/dataLabelling/df_ml_yset.csv"

        # Assuming the splitting function is already defined and accessible
        X = load_data(features_file_path)
        y = load_data(labels_file_path)
        ts, rs, X_train, X_test, y_train, y_test = splitting(X, y)
        # Define the models you want to train

        # # Train and evaluate models
        # results = train_and_evaluate(ts, rs, X_train, y_train, X_test, y_test)
        #
        # # Store results
        # store_results(
        #     results,
        #     "trainingAndValidation/trainingAndTesting/model_storing2.pkl",
        # )

        # Train and evaluate models
        result = train_only_best(ts, rs, X_train, y_train, X_test, y_test)

        # Store results
        store_results(
            result,
            "trainingAndValidation/trainingAndTesting/best_model.pkl",
        )

        with open("trainingAndValidation/trainingAndTesting/best_model.pkl", "rb") as file:
            existing_results = pickle.load(file)
            print('The best model was trained: ')
            print(existing_results)
    else:
        with open("model.pkl", "rb") as file:
            model = pickle.load(file)
        features_file_path = 'featureGeneration/featureGeneration/test_row.csv'
        hist_file_path = "featureGeneration/dataLabelling/df_ml_Xset.csv"
        X = load_data(features_file_path)
        X.drop('avg_rent', axis=1, inplace=True)
        df_hist = load_data(hist_file_path)
        X = X[df_hist.columns]
        pred = model.predict(X)
        print('The average rent is predicted to be:', pred[0])


if __name__ == "__main__":
    main()
