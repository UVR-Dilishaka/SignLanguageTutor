import cv2
import os
import csv
import mediapipe as mp

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.3)

data_base_path = '.\\dataset\\Twelve'


# Get all image paths in the dataset folder
your_dataset_paths = [os.path.join(data_base_path, file) for file in os.listdir(data_base_path) if file.endswith(('.png', '.jpg', '.jpeg'))]

# Print all image paths for debugging
#print("Image Paths:", your_dataset_paths)

# Open a CSV file to save the landmarks
with open("landmarks_12.csv", "w", newline="") as file:
    writer = csv.writer(file)

    # Define the header
    header = ["Image Path"]
    # Append "x", "y", "z" for each of the 21 landmarks
    for i in range(21):  # MediaPipe Hands has 21 landmarks
        header.extend([f"x_{i+1}", f"y_{i+1}", f"z_{i+1}"])
    writer.writerow(header)

    # Process each image and write landmarks to the CSV
    for image_path in your_dataset_paths:
        image = cv2.imread(image_path)

        # Check if the image is read correctly
        if image is None:
            print(f"Failed to read image: {image_path}")
            continue  # Skip this image if it couldn't be read

        print(f"Processing image: {image_path}, shape: {image.shape}")
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        result = hands.process(image_rgb)

        # Start with the image path
        landmarks = [image_path]

        if result.multi_hand_landmarks:
            hand_landmarks = result.multi_hand_landmarks[0]
            # Collect (x, y, z) for each landmark
            for lm in hand_landmarks.landmark:
                landmarks.extend([lm.x, lm.y, lm.z])
            print(f"Processed: {image_path}, Landmarks detected")
        else:
            # If no landmarks detected, fill with None
            landmarks.extend([None] * (3 * 21))  # 21 landmarks with (x, y, z)
            print(f"Processed: {image_path}, No landmarks detected")

        # Write the complete landmarks list for the current image to the CSV
        writer.writerow(landmarks)

print("Landmarks have been saved to landmarks.csv")
