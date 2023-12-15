import pandas as pd
import sys
sys.path.append("C:/Users/sayye/OneDrive/Desktop/college/PG/UPC/ADSDB/part2/")
import machine_learning_utils as ml

def main():
    ts = 0.30
    rs = 42
    X_train = pd.read_csv('C:/Users/sayye/OneDrive/Desktop/college/PG/UPC/ADSDB/part2/advanceTopic/featureSelection/X_trainPCA.csv')
    X_test = pd.read_csv('C:/Users/sayye/OneDrive/Desktop/college/PG/UPC/ADSDB/part2/advanceTopic/featureSelection/X_testPCA.csv')

    y_train = pd.read_csv('C:/Users/sayye/OneDrive/Desktop/college/PG/UPC/ADSDB/part2/advanceTopic/featureSelection/y_train.csv')
    y_test = pd.read_csv('C:/Users/sayye/OneDrive/Desktop/college/PG/UPC/ADSDB/part2/advanceTopic/featureSelection/y_test.csv')

    # Train and evaluate models
    results = ml.train_and_evaluate(ts, rs, X_train, y_train, X_test, y_test)

    # Store results
    ml.store_results(
        results,
        "C:/Users/sayye/OneDrive/Desktop/college/PG/UPC/ADSDB/part2/trainingAndValidation/trainingAndTesting/model_storing_pca.pkl",
    )
if __name__ == "__main__":
    main()

