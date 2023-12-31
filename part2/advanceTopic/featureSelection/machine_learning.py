import pandas as pd
import sys
import pickle
sys.path.append("./")
from machine_learning_utils import (splitting, train_and_evaluate, store_results, train_only_best)


def main():
    ts = 0.30
    rs = 42
    X_train = pd.read_csv('advanceTopic/featureSelection/X_trainPCA.csv')
    X_test = pd.read_csv('advanceTopic/featureSelection/X_testPCA.csv')

    y_train = pd.read_csv('advanceTopic/featureSelection/y_train.csv')
    y_test = pd.read_csv('advanceTopic/featureSelection/y_test.csv')

    # # Train and evaluate models
    # results = train_and_evaluate(ts, rs, X_train, y_train, X_test, y_test)
    #
    # # Store results
    # store_results(
    #     results,
    #     "trainingAndValidation/trainingAndTesting/model_storing_pca2.pkl",
    # )

    # Train and evaluate models
    result = train_only_best(ts, rs, X_train, y_train, X_test, y_test)

    # Store results
    store_results(
        result,
        "trainingAndValidation/trainingAndTesting/best_model_pca.pkl",
    )

    with open("trainingAndValidation/trainingAndTesting/best_model_pca.pkl", "rb") as file:
        existing_results = pickle.load(file)
        print('The best model was trained: ')
        print(existing_results)


if __name__ == "__main__":
    main()


