import sys

sys.path.append("C:/Users/sayye/OneDrive/Desktop/college/PG/UPC/ADSDB/part2/")
import machine_learning_utils as ml


def main():
    # Replace these paths with the paths where your input data is stored
    features_file_path = "C:/Users/sayye/OneDrive/Desktop/college/PG/UPC/ADSDB/part2/featureGeneration/dataLabelling/df_ml_Xset.csv"
    labels_file_path = "C:/Users/sayye/OneDrive/Desktop/college/PG/UPC/ADSDB/part2/featureGeneration/dataLabelling/df_ml_yset.csv"

    # Assuming the splitting function is already defined and accessible
    X, y = ml.load_data(features_file_path, labels_file_path)
    ts, rs, X_train, X_test, y_train, y_test = ml.splitting(X, y)
    # Define the models you want to train

    # Train and evaluate models
    results = ml.train_and_evaluate(ts, rs, X_train, y_train, X_test, y_test)

    # Store results
    ml.store_results(
        results,
        "C:/Users/sayye/OneDrive/Desktop/college/PG/UPC/ADSDB/part2/trainingAndValidation/trainingAndTesting/model_storing2.pkl",
    )


if __name__ == "__main__":
    main()
