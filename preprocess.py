import os
import pandas as pd

def shuffle_csv(pth, train_ratio, valid_ratio):
    # Read the CSV file
    df = pd.read_csv(pth)

    # Shuffle the DataFrame
    df = df.sample(frac=1).reset_index(drop=True)

    # Split into training and validation sets
    train_df = df[:int(len(df) * train_ratio)]
    valid_df = df[-int(len(df) * valid_ratio):]

    return train_df, valid_df

if __name__ == "__main__":
    # Specify the path to your CSV file and data directory
    csv_path = 'data.csv'

    # Call the function with the specified arguments
    train_set, valid_set = shuffle_csv(csv_path, 0.80, 0.20)

    # Print or use the resulting DataFrames as needed
    print("Training Set:")
    print(train_set.head())
    train_set.to_csv('train.csv', index=False)

    print("\nValidation Set:")
    print(valid_set.head())
    valid_set.to_csv('test.csv', index=False)
