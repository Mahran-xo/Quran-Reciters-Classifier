import os
import pandas as pd
from tqdm import tqdm

def create_dataframe(main_directory):
    # Initialize empty lists to store data
    file_paths = []
    class_names = []
    class_ids = {}

    # Assign unique class ids to each class
    class_id_counter = 0

    # Traverse through the main directory and its subdirectories
    for root, dirs, files in tqdm(os.walk(main_directory)):
        for file in files:
            # Get the filename with path
            file_path = os.path.join(root, file)
            file_paths.append(file_path)

            # Get the class name from the subdirectory of the main one
            relative_path = os.path.relpath(file_path, main_directory)
            class_name = os.path.split(os.path.dirname(relative_path))[1]
            class_names.append(class_name)

            # Assign a unique class id to each class
            if class_name not in class_ids:
                class_ids[class_name] = class_id_counter
                class_id_counter += 1

    # Map class_names to class_ids
    class_ids_list = [class_ids[class_name] for class_name in class_names]

    # Create a DataFrame
    data = {'filename': file_paths, 'class_name': class_names, 'class_id': class_ids_list}
    df = pd.DataFrame(data)

    # Replace forward slashes with backslashes in the filename column
    df['filename_'] = df['filename'].str.replace('/', '\\')

    # Save the DataFrame to a CSV file
    df.to_csv('data.csv', index=False)

    # Display the DataFrame
    print(df)

if __name__ == "__main__":
    # Set the main directory path
    main_directory = 'data'

    # Call the main function
    create_dataframe(main_directory)

