import os
import cv2
import mediapipe as mp
import pandas as pd

# Initialize Mediapipe Hands module
mp_hands = mp.solutions.hands


def extract_landmarks_from_images(folder_path, output_csv):
    # Initialize Mediapipe Hands in static_image_mode
    hands = mp_hands.Hands(
        static_image_mode=True,  # For static images
        max_num_hands=1,  # Only one hand per image
        min_detection_confidence=0.5  # Confidence threshold for detection
    )

    # Initialize DataFrame to store results
    columns = ['image'] + [f"{i}_x" for i in range(21)] + [f"{i}_y" for i in range(21)]
    data = pd.DataFrame(columns=columns)
    rows = []  # List to accumulate rows

    # Process each image in the folder
    for idx, image_name in enumerate(sorted(os.listdir(folder_path))):
        image_path = os.path.join(folder_path, image_name)

        # Load the image
        image = cv2.imread(image_path)
        if image is None:
            print(f"Failed to load image: {image_path}")
            continue

        # Convert to RGB for Mediapipe
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Process the image to detect hands
        results = hands.process(image_rgb)

        # Initialize row data
        row_data = {'image': idx}

        # Extract landmarks if a hand is detected
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]  # Use the first detected hand
            h, w, _ = image.shape  # Image dimensions

            for i, lm in enumerate(hand_landmarks.landmark):
                # Convert normalized coordinates to pixel values
                x = int(lm.x * w)
                y = int(lm.y * h)
                row_data[f"{i}_x"] = x
                row_data[f"{i}_y"] = y
        else:
            # print(f"No hand detected in image: {image_name}")
            # Fill missing landmarks with NaN
            for i in range(21):
                row_data[f"{i}_x"] = None
                row_data[f"{i}_y"] = None

        # Add the row data to the rows list
        rows.append(row_data)

    # Convert rows to DataFrame and save as CSV
    data = pd.DataFrame(rows, columns=columns)
    data.to_csv(output_csv, index=False)
    print(f"Landmarks saved to {output_csv}")
    hands.close()


# Define folder path and output CSV file
folder_path = r"D:\DSGP\benchmarking\dataset\evaluation\rgb"  # Replace with your folder path
output_csv = "mp_landmarks.csv"  # Replace with desired output file name

# Call the function
extract_landmarks_from_images(folder_path, output_csv)
