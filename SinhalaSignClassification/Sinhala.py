import cv2
import mediapipe as mp
import os
import csv
import numpy as np


def calculate_angle(p1, p2, p3):
    """Calculate the angle between three points."""
    a = np.array(p1)
    b = np.array(p2)
    c = np.array(p3)

    ba = a - b
    bc = c - b

    dot_product = np.dot(ba, bc)
    magnitude_ba = np.linalg.norm(ba)
    magnitude_bc = np.linalg.norm(bc)

    angle_rad = np.arccos(dot_product / (magnitude_ba * magnitude_bc))
    angle_deg = np.rad2deg(angle_rad)
    return angle_deg


def listing_angles(landmarks):
    """Calculate joint angles from landmarks."""
    angle_list = np.array([
        calculate_angle(landmarks[1], landmarks[2], landmarks[3]),
        calculate_angle(landmarks[0], landmarks[5], landmarks[6]),
        calculate_angle(landmarks[0], landmarks[9], landmarks[10]),
        calculate_angle(landmarks[0], landmarks[13], landmarks[14]),
        calculate_angle(landmarks[0], landmarks[17], landmarks[18]),
        calculate_angle(landmarks[5], landmarks[6], landmarks[7]),
        calculate_angle(landmarks[9], landmarks[10], landmarks[11]),
        calculate_angle(landmarks[13], landmarks[14], landmarks[15]),
        calculate_angle(landmarks[17], landmarks[18], landmarks[19]),
        calculate_angle(landmarks[6], landmarks[7], landmarks[8]),
        calculate_angle(landmarks[10], landmarks[11], landmarks[12]),
        calculate_angle(landmarks[14], landmarks[15], landmarks[16]),
        calculate_angle(landmarks[18], landmarks[19], landmarks[20]),
        calculate_angle(landmarks[0], landmarks[1], landmarks[2]),
        calculate_angle(landmarks[2], landmarks[3], landmarks[4]),
        calculate_angle(landmarks[2], landmarks[1], landmarks[5]),
    ])
    return angle_list


def process_hand_images(folder_path, output_csv_path):
    """Process images from a folder and extract joint angles for a single hand."""
    # Initialize MediaPipe Hand model
    mp_hands = mp.solutions.hands

    # Create or overwrite the CSV file and write the header
    with open(output_csv_path, mode="w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)

        # Write header with columns for joint angles
        header = ["Image"]
        header.extend([
            "THUMB_MCP_angle", "INDEX_MCP_angle", "MIDDLE_MCP_angle", "RING_MCP_angle", "PINKY_MCP_angle",
            "INDEX_PIP_angle", "MIDDLE_PIP_angle", "RING_PIP_angle", "PINKY_PIP_angle",
            "INDEX_DIP_angle", "MIDDLE_DIP_angle", "RING_DIP_angle", "PINKY_DIP_angle",
            "THUMB_TMC_angle", "THUMB_IP_angle", "THUMB_INDEX_Abduction_angle"
        ])
        csv_writer.writerow(header)

        # Initialize the Hand model
        with mp_hands.Hands(
            static_image_mode=True,  # Set to static mode for images
            max_num_hands=1,  # Detect only one hand
            min_detection_confidence=0.5,  # Detection threshold
        ) as hands:
            # Loop through all files in the folder
            for filename in os.listdir(folder_path):
                # Check if file is an image (e.g., .jpg, .jpeg, .png)
                if filename.lower().endswith((".jpg", ".jpeg", ".png")):
                    image_path = os.path.join(folder_path, filename)
                    image = cv2.imread(image_path)

                    # Convert the image to RGB for MediaPipe processing
                    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                    # Process the image and detect hands
                    result = hands.process(rgb_image)

                    # If landmarks are detected, extract features
                    if result.multi_hand_landmarks:
                        for hand_landmarks in result.multi_hand_landmarks:
                            # Extract normalized landmarks
                            joint_coordinates = np.array([
                                [lm.x, lm.y, lm.z]
                                for lm in hand_landmarks.landmark
                            ])

                            # Calculate joint angles
                            joint_angles = listing_angles(joint_coordinates)

                            # Write data for this image to the CSV file
                            row_data = [filename]
                            row_data.extend(joint_angles.flatten())
                            csv_writer.writerow(row_data)

                    else:
                        print(f"No hand detected in {filename}. Skipping...")

    print(f"Hand landmark data saved to {output_csv_path}")


# Usage Example
folder_path = r".\\dataset\\Twelve"  # Replace with the path to your dataset folder
output_csv_path = "hand_angles_12.csv"  # Replace with the desired output CSV file path
process_hand_images(folder_path, output_csv_path)
