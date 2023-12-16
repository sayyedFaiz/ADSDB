
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import sys
sys.path.append("./")

def load_model_results(results_file_path):
    with open(results_file_path, 'rb') as file:
        loaded_models = pickle.load(file)
    return pd.DataFrame(loaded_models)

def visualize_model_comparison(df, error_column, model_column, plot_title):
    df.sort_values(error_column, inplace=True)
    print(df)
    df[error_column] = pd.to_numeric(df[error_column])
    df.plot(x=model_column, y=error_column, kind='bar', title=plot_title, ylabel='MAPE', xlabel='MODEL')
    plt.show()

def main():
    results_file_path = '../trainingAndTesting/model_storing2.pkl'

    df_models = load_model_results(results_file_path)

    # Call the visualization function
    visualize_model_comparison(df_models, 'error', 'model', 'Comparison of models')

if __name__ == "__main__":
    main()
