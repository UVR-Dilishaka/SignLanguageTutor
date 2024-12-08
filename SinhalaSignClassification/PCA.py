import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Load the combined dataset
file_path = 'SinhalaSignClassification/SSL - Cleaned CSV'  # Path to the combined CSV file
data = pd.read_csv(file_path)

# Separate features and labels
features = data.drop(columns=['image'])  # Drop non-numeric or irrelevant columns

# Standardize the features
scaler = StandardScaler()
standardized_features = scaler.fit_transform(features)

# Perform PCA
n_components = 2  # Number of components
pca = PCA(n_components=n_components)
principal_components = pca.fit_transform(standardized_features)

# Create a DataFrame for principal components
pca_df = pd.DataFrame(principal_components, columns=[f'PC{i+1}' for i in range(n_components)])

# Visualize the PCA results
plt.figure(figsize=(8, 6))
plt.scatter(pca_df['PC1'], pca_df['PC2'], alpha=0.7)
plt.title('PCA Visualization')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.show()

# Print explained variance ratio
explained_variance = pca.explained_variance_ratio_
print("Explained Variance Ratio:", explained_variance)
