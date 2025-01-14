import cv2
import mediapipe as mp
import os
import csv
import numpy as np

def palm_orientation(finger_MCP_coordinates):
    """Calculate the palm orientation angles."""
    wrist = np.array([0, 0, 0])
    mean_finger_base = np.mean(finger_MCP_coordinates, axis=0)

    vector_a = mean_finger_base - wrist
    vector_b = finger_MCP_coordinates[3] - finger_MCP_coordinates[0]

    pitch = np.arctan2(vector_a[2], np.sqrt(vector_a[0] ** 2 + vector_a[1] ** 2))
    yaw = np.arctan2(vector_a[0], vector_a[2])
    roll = np.arctan2(vector_b[1], vector_b[0])

    return np.rad2deg(np.array([pitch, yaw, roll]))

def getPalmOerientationFromFolder(folder_path, output_csv_path):


    # Initialize MediaPipe Hand model
    mp_hands = mp.solutions.hands

    # Create or overwrite the CSV file and write the header
    with open(output_csv_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        # Write header with columns for each landmark's coordinates for both hands
        header = ["Image"]

        header.extend(["Left_Palm_orientation_pitch",
                       "Left_Palm_orientation_yaw",
                       "Left_Palm_orientation_roll"])

        header.extend(["Right_Palm_orientation_pitch",
                       "Right_Palm_orientation_yaw",
                       "Right_Palm_orientation_roll"])


        csv_writer.writerow(header)

        # Initialize the Hand model
        with mp_hands.Hands(
                static_image_mode=True,  # Set to static mode for images
                max_num_hands=2,  # Detect up to 2 hands
                min_detection_confidence=0.5  # Detection threshold
        ) as hands:
            # Loop through all files in the folder
            for filename in os.listdir(folder_path):
                # Check if file is an image (e.g., .jpg, .jpeg, .png)
                if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                    image_path = os.path.join(folder_path, filename)
                    image = cv2.imread(image_path)

                    # Convert the image to RGB for MediaPipe processing
                    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                    # Process the image and detect hands
                    result = hands.process(rgb_image)

                    # Initialize placeholders for left and right hand landmarks
                    left_hand_data = np.zeros((21, 3))  # 21 landmarks, 3 coordinates
                    right_hand_data = np.zeros((21, 3))

                    if result.multi_hand_landmarks and result.multi_handedness:
                        for hand_idx, (hand_landmarks, handedness) in enumerate(
                                zip(result.multi_hand_landmarks, result.multi_handedness)):
                            # Identify the hand as "Left" or "Right"
                            hand_label = handedness.classification[0].label

                            # Get wrist coordinates for normalization
                            wrist = hand_landmarks.landmark[0]
                            wrist_x, wrist_y, wrist_z = wrist.x, wrist.y, wrist.z

                            # Add normalized landmark data for each landmark
                            for i, landmark in enumerate(hand_landmarks.landmark):
                                norm_x = landmark.x - wrist_x
                                norm_y = landmark.y - wrist_y
                                norm_z = landmark.z - wrist_z
                                if hand_label == "Left":
                                    left_hand_data[i] = [norm_x, norm_y, norm_z]
                                elif hand_label == "Right":
                                    right_hand_data[i] = [norm_x, norm_y, norm_z]


                    # Adding palm orientation
                    left_palm_orientation = palm_orientation(left_hand_data)
                    right_palm_orientation = palm_orientation(right_hand_data)


                    # Write data for this image to the CSV file
                    row_data = [filename]
                    row_data.extend(left_palm_orientation)
                    row_data.extend(right_palm_orientation)

                    csv_writer.writerow(row_data)




    print(f"Palm orientation data saved to {output_csv_path}")


# Usage
folder_path = r"D:\Yr2\DSGP\Virtual Environment\DSGP\TamilDataset\TamilDataset\letter1"
output_csv_path = "palm_orientation.csv"
getPalmOerientationFromFolder(folder_path, output_csv_path)
