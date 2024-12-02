import pandas as pd

# Load the combined dataset
file_path = 'combined_dataset.csv'
data = pd.read_csv(file_path)

# Compute mean, max, and min for each angle
angle_columns = [col for col in data.columns if 'angle' in col]
angle_stats = data[angle_columns].agg(['mean', 'max', 'min'])

# Save the extracted features
angle_stats.to_csv('extracted_features.csv')
print("Extracted features saved as 'extracted_features.csv'.")
