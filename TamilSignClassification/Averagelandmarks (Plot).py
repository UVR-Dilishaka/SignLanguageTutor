import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load landmarks data from CSV
landmarks_df = pd.read_csv("./Land Marks from each sign/landmarks_1.csv")
print(landmarks_df.head())  # Check data structure



# Compute average x, y, z for each landmark across all images
mean_landmarks = landmarks_df.iloc[:, 1:].mean().values.reshape(21, 3)
x_mean, y_mean = mean_landmarks[:, 0], mean_landmarks[:, 1]

x_max = 1.0  # Set this to your desired maximum for the x-axis
y_max = 1.0

# Plot average hand landmarks
plt.figure(figsize=(6, 6))
plt.scatter(x_mean, y_mean, color='red')
plt.title("Average Hand Landmarks Across All Images of vowel 12 ")
plt.xlabel("X")
plt.ylabel("Y")
plt.gca().invert_yaxis()  # Match image coordinates
plt.grid(True)
plt.show()
