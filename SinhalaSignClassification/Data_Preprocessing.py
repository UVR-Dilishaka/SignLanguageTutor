import os
import pandas as pd

# Specify the directory containing your CSV files
csv_directory = 'SinhalaSignClassification/SSL - Cleaned CSV'  # Replace with the folder containing the 18 CSVs
combined_data = []

# Loop through all CSV files in the directory
for file in os.listdir(csv_directory):
    if file.endswith('.csv'):  # Process only CSV files
        file_path = os.path.join(csv_directory, file)
        print(f"Processing {file_path}...")
        data = pd.read_csv(file_path)

        # Ensure the dataset has the expected columns
        expected_columns = [
            'image', 'THUMB_MCP_angle', 'INDEX_MCP_angle', 'MIDDLE_MCP_angle', 'RING_MCP_angle',
            'PINKY_MCP_angle', 'INDEX_PIP_angle', 'MIDDLE_PIP_angle', 'RING_PIP_angle',
            'PINKY_PIP_angle', 'INDEX_DIP_angle', 'MIDDLE_DIP_angle', 'RING_DIP_angle',
            'PINKY_DIP_angle', 'THUMB_TMC_angle', 'THUMB_IP_angle', 'THUMB_INDEX_Abduction_angle'
        ]
        if not all(col in data.columns for col in expected_columns):
            print(f"File {file} does not have the expected columns. Skipping...")
            continue

        combined_data.append(data)

# Combine all files into a single DataFrame
if combined_data:
    combined_df = pd.concat(combined_data, ignore_index=True)
    print(f"Combined dataset shape: {combined_df.shape}")
else:
    raise ValueError("No valid CSV files found in the directory.")

# Save the combined data to a new CSV file
combined_df.to_csv('combined_dataset.csv', index=False)
print("Combined dataset saved as 'combined_dataset.csv'.")
