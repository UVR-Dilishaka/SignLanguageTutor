import pandas as pd
import numpy as np

# Function to calculate additional features
def extract_features(row):
    features = {}
    features['average_angle'] = row.mean()
    features['angle_range'] = row.max() - row.min()
    return features

# Load dataset
file_path = 'combined_dataset.csv'
data = pd.read_csv(file_path)

# Extract features for each row
angle_columns = [col for col in data.columns if 'angle' in col]
features_df = data[angle_columns].apply(extract_features, axis=1, result_type='expand')

# Save the features
features_df.to_csv('real_time_features.csv', index=False)
print("Real-time features saved as 'real_time_features.csv'.")
