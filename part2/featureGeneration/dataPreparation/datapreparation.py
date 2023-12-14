import pandas as pd


def load_data(file_path):
    return pd.read_csv(file_path)

def one_hot_encode(df, column_name):
    one_hot = pd.get_dummies(df[column_name])
    df = df.drop(column_name, axis=1)
    df = df.join(one_hot)
    return df

def save_data(df, file_path):
    df.to_csv(file_path, index=False)

def main():
    # Set your local file paths here
    input_file_path = 'C:/Users/sayye/OneDrive/Desktop/college/PG/UPC/ADSDB/part2/featureGeneration/featureGeneration/df_feature_generation.csv'
    output_file_path = 'C:/Users/sayye/OneDrive/Desktop/college/PG/UPC/ADSDB/part2/featureGeneration/dataPreparation/df_data_preparation.csv'

    df_analysis = load_data(input_file_path)

    # One-hot encode 'Income_Group' with a prefix for the column names
    df_analysis = one_hot_encode(df_analysis, 'Income_Group')
    df_analysis.rename(columns={'Low':'Income_group_Low','Medium-Low':'Income_group_Medium-Low','Medium':'Income_group_Medium','Medium-High':'Income_group_Medium-High','High':'Income_group_High'}, inplace=True)

    # One-hot encode 'district' with a prefix for the column names
    df_analysis = one_hot_encode(df_analysis, 'district')
    df_analysis.rename(columns={'les corts':'les corts_district','sant andreu': 'sant andreu_district'}, inplace=True)

    # One-hot encode 'neighbourhood' with no prefix (since the neighbourhood names are unique)
    df_analysis = one_hot_encode(df_analysis, 'neighbourhood')
    df_analysis.head()
    save_data(df_analysis, output_file_path)

if __name__ == "__main__":
    main()
