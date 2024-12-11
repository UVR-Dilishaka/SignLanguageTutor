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
    """Generate a list of angles from landmarks."""
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


def getRightHandLandmarks(folder_path, output_csv_path, label):
    # Initialize MediaPipe Hand model
    mp_hands = mp.solutions.hands

    # Create or overwrite the CSV file and write the header
    with open(output_csv_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        # Write header
        header = ["Image"]
        header.extend([f"Angle_{i}" for i in range(16)])  # 16 angles
        header.append("Label")  # Add the label column
        csv_writer.writerow(header)

        with mp_hands.Hands(
                static_image_mode=True,
                max_num_hands=1,  # Only one hand (right hand)
                min_detection_confidence=0.5
        ) as hands:
            for filename in os.listdir(folder_path):
                if filename.lower().endswith(('.jpg', '.jpeg', '.png')):  # Process image files
                    image_path = os.path.join(folder_path, filename)
                    image = cv2.imread(image_path)

                    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    result = hands.process(rgb_image)

                    right_hand_data = np.zeros((21, 3))  # Placeholder for right hand landmarks

                    if result.multi_hand_landmarks and result.multi_handedness:
                        for hand_landmarks, handedness in zip(result.multi_hand_landmarks, result.multi_handedness):
                            hand_label = handedness.classification[0].label
                            if hand_label == "Right":  # Process only the right hand
                                wrist = hand_landmarks.landmark[0]
                                wrist_x, wrist_y, wrist_z = wrist.x, wrist.y, wrist.z

                                for i, landmark in enumerate(hand_landmarks.landmark):
                                    norm_x = landmark.x - wrist_x
                                    norm_y = landmark.y - wrist_y
                                    norm_z = landmark.z - wrist_z
                                    right_hand_data[i] = [norm_x, norm_y, norm_z]

                    # Generate angles
                    right_joint_angles = listing_angles(right_hand_data)

                    # Write data to CSV
                    row_data = [filename]
                    row_data.extend(right_joint_angles.flatten())
                    row_data.append(label)  # Append label
                    csv_writer.writerow(row_data)


# Usage
folder_path = r".\\dataset\\Twelve"
output_csv_path = "right_hand_angles_12.csv"
label = "Letter 12"
getRightHandLandmarks(folder_path, output_csv_path, label)
