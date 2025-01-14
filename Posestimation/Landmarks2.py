import cv2
import mediapipe as mp
import os
import csv


def getLandmarksFromFolder(folder_path, output_csv_path):
    # Define landmark names
    landmark_names = [
        "WRIST",
        "THUMB_CMC", "THUMB_MCP", "THUMB_IP", "THUMB_TIP",
        "INDEX_FINGER_MCP", "INDEX_FINGER_PIP", "INDEX_FINGER_DIP", "INDEX_FINGER_TIP",
        "MIDDLE_FINGER_MCP", "MIDDLE_FINGER_PIP", "MIDDLE_FINGER_DIP", "MIDDLE_FINGER_TIP",
        "RING_FINGER_MCP", "RING_FINGER_PIP", "RING_FINGER_DIP", "RING_FINGER_TIP",
        "PINKY_MCP", "PINKY_PIP", "PINKY_DIP", "PINKY_TIP"
    ]

    # Initialize MediaPipe Hand model
    mp_hands = mp.solutions.hands

    # Create or overwrite the CSV file and write the header
    with open(output_csv_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        # Write header with columns for each landmark's coordinates for both hands
        header = ["Image"]
        for hand in ["Left", "Right"]:
            for landmark_name in landmark_names:
                header.extend([f"{hand}_{landmark_name}_X", f"{hand}_{landmark_name}_Y", f"{hand}_{landmark_name}_Z"])
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

                    # Initialize row data with the filename
                    row_data = [filename]

                    # Prepare placeholders for left and right hand landmarks
                    left_hand_data = [0.0] * (len(landmark_names) * 3)
                    right_hand_data = [0.0] * (len(landmark_names) * 3)

                    if result.multi_hand_landmarks and result.multi_handedness:
                        for hand_idx, (hand_landmarks, handedness) in enumerate(
                                zip(result.multi_hand_landmarks, result.multi_handedness)):
                            # Identify the hand as "Left" or "Right"
                            hand_label = handedness.classification[0].label

                            # Prepare data list for the detected hand
                            hand_data = []

                            # Get wrist coordinates for normalization
                            wrist = hand_landmarks.landmark[0]
                            wrist_x, wrist_y, wrist_z = wrist.x, wrist.y, wrist.z

                            # Add normalized landmark data for each landmark
                            for landmark in hand_landmarks.landmark:
                                norm_x = landmark.x - wrist_x
                                norm_y = landmark.y - wrist_y
                                norm_z = landmark.z - wrist_z
                                hand_data.extend([norm_x, norm_y, norm_z])

                            # Assign data to left or right hand list based on label
                            if hand_label == "Left":
                                left_hand_data = hand_data
                            elif hand_label == "Right":
                                right_hand_data = hand_data

                    # Append left and right hand data to the row data
                    row_data.extend(left_hand_data)
                    row_data.extend(right_hand_data)

                    # Write data for this image to the CSV file
                    csv_writer.writerow(row_data)

    print(f"Landmark data saved to {output_csv_path}")


# Usage
folder_path = 
output_csv_path = "hand_landmarks.csv"
getLandmarksFromFolder(folder_path, output_csv_path)
