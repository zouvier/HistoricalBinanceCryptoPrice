import os
import pandas as pd

def convert_parquet_to_csv(root_folder):
    # Walk through all folders and subfolders in the root_folder
    for folder_path, _, filenames in os.walk(root_folder):
        for filename in filenames:
            # Check if the file has a .parquet extension
            if filename.endswith('.parquet'):
                # Construct the full path of the file
                parquet_path = os.path.join(folder_path, filename)
                
                try:
                    # Check if the size of the .parquet file is 0
                    if os.path.getsize(parquet_path) == 0:
                        os.remove(parquet_path)
                        print(f"Deleted empty {parquet_path}")
                        continue
                    
                    # Construct the path for the .csv file
                    csv_path = os.path.join(folder_path, filename.replace('.parquet', '.csv'))
                    
                    # Check if the .csv file already exists
                    if os.path.exists(csv_path):
                        print(f"{csv_path} already exists. Deleting {parquet_path}.")
                        os.remove(parquet_path)
                        continue
                    
                    # Read the .parquet file using pandas
                    df = pd.read_parquet(parquet_path)
                    
                    # Save the dataframe to .csv format
                    df.to_csv(csv_path, index=False)
                    print(f"Converted {parquet_path} to {csv_path}")
                    
                    # Delete the .parquet file after conversion
                    os.remove(parquet_path)
                    print(f"Deleted {parquet_path}")
                
                except Exception as e:
                    print(f"Error processing {parquet_path}: {e}")

if __name__ == "__main__":
    root_folder = "/Users/zouvier/Downloads/crypto-currency-data"
    convert_parquet_to_csv(root_folder)
