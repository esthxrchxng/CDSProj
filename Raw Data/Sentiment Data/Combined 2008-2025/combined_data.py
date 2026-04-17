import pandas as pd
import os

# Root directory containing 2008, 2009, etc.
root_dir = './' 
# The specific filenames you want to target
target_files = ['daily.csv', 'daily_sentiment_results.csv', 'predictions.csv', 'test_predictions.csv']

# Dictionary to hold lists of dataframes for each category
data_groups = {name: [] for name in target_files}

# 1. Walk through all folders
for folder_name in sorted(os.listdir(root_dir)):
    folder_path = os.path.join(root_dir, folder_name)
    
    if os.path.isdir(folder_path) and folder_name.isdigit():
        for target in target_files:
            file_path = os.path.join(folder_path, target)
            
            # Check if the specific file exists in this year's folder
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
                
                # Highly recommended: Add the year so you don't lose context
                df['source_year'] = folder_name
                
                data_groups[target].append(df)

# 2. Merge and save each group
for file_name, df_list in data_groups.items():
    if df_list:
        combined_df = pd.concat(df_list, ignore_index=True)
        
        # Create a new filename like "combined_daily.csv"
        output_name = f"combined_{file_name}"
        combined_df.to_csv(output_name, index=False)
        
        print(f"Saved: {output_name} (from {len(df_list)} years of data)")
    else:
        print(f"No files found for: {file_name}")