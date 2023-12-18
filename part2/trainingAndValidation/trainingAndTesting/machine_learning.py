import sys

sys.path.append("./")
from db_utils import load_data
from machine_learning_utils import (splitting, train_and_evaluate, store_results)

def main():
    # Replace these paths with the paths where your input data is stored
    features_file_path = "featureGeneration/dataLabelling/df_ml_Xset.csv"
    labels_file_path = "featureGeneration/dataLabelling/df_ml_yset.csv"

    # Assuming the splitting function is already defined and accessible
    X = load_data(features_file_path)
    y= load_data(labels_file_path)
    ts, rs, X_train, X_test, y_train, y_test = splitting(X, y)
    # Define the models you want to train

    # Train and evaluate models
    results = train_and_evaluate(ts, rs, X_train, y_train, X_test, y_test)

    # Store results
    store_results(
        results,
        "trainingAndValidation/trainingAndTesting/model_storing2.pkl",
    )


if __name__ == "__main__":
    main()
