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

    angle_rad = np.arccos(dot_product / (magnitude_ba * magnitude_bc ))
    angle_deg = np.rad2deg(angle_rad)
    return angle_deg


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


def remove_rotation(joint_coordinates, wrist, finger_MCP_coordinates):
    """Remove rotation from the joint coordinates."""
    mean_finger_base = np.mean(finger_MCP_coordinates, axis=0)

    reference_vector1 = mean_finger_base - wrist
    reference_vector2 = finger_MCP_coordinates[3] - finger_MCP_coordinates[0]

    v1_norm = reference_vector1 / np.linalg.norm(reference_vector1)
    v2_norm = reference_vector2 / np.linalg.norm(reference_vector2)

    v3_norm = np.cross(v1_norm, v2_norm)  # z-axis
    v1_norm = v1_norm  # y-axis
    v2_norm = np.cross(v3_norm, v1_norm)  # x-axis

    rotation_matrix = np.array([v2_norm, v1_norm, v3_norm]).T

    transformed_joints = joint_coordinates @ rotation_matrix

    return transformed_joints


def calculate_rotational_angles(original_coordinates, transformed_coordinates):
    # Difference in position after rotation removal
    rotation_diff = transformed_coordinates - original_coordinates

    pitch = np.arctan2(rotation_diff[:, 1], rotation_diff[:, 2])  # Rotation around X-axis
    yaw = np.arctan2(rotation_diff[:, 0], rotation_diff[:, 2])  # Rotation around Y-axis
    roll = np.arctan2(rotation_diff[:, 1], rotation_diff[:, 0])  # Rotation around Z-axis

    return np.vstack([pitch, yaw, roll]).T


def listing_angles(landmarks):
    angle_list = np.array([calculate_angle(landmarks[1], landmarks[2], landmarks[3]),
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
                           calculate_angle(landmarks[2], landmarks[1], landmarks[5])])
    return angle_list


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

        header.extend(["Left_THUMB_MCP_angle", "Left_INDEX_MCP_angle", "Left_MIDDLE_MCP_angle", "Left_RING_MCP_angle", "Left_PINKY_MCP_angle"])
        header.extend(["Left_INDEX_PIP_angle", "Left_MIDDLE_PIP_angle", "Left_RING_PIP_angle", "Left_PINKY_PIP_angle"])
        header.extend(["Left_INDEX_DIP_angle", "Left_MIDDLE_DIP_angle", "Left_RING_DIP_angle", "Left_PINKY_DIP_angle"])

        header.extend(["Left_THUMB_TMC_angle",
                        "Left_THUMB_IP_angle",
                        "Left_THUMB_INDEX_Abduction_angle"])

        header.extend(["Right_THUMB_MCP_angle", "Right_INDEX_MCP_angle", "Right_MIDDLE_MCP_angle", "Right_RING_MCP_angle",
                       "Right_PINKY_MCP_angle"])
        header.extend(["Right_INDEX_PIP_angle", "Right_MIDDLE_PIP_angle", "Right_RING_PIP_angle", "Right_PINKY_PIP_angle"])
        header.extend(["Right_INDEX_DIP_angle", "Right_MIDDLE_DIP_angle", "Right_RING_DIP_angle", "Right_PINKY_DIP_angle"])

        header.extend(["Right_THUMB_TMC_angle",
                       "Right_THUMB_IP_angle",
                       "Right_THUMB_INDEX_Abduction_angle"])


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


                    # Adding joint angles
                    left_joint_angles = listing_angles(left_hand_data)
                    right_joint_angles = listing_angles(right_hand_data)

                    # Adding palm orientation
                    left_palm_orientation = palm_orientation(left_hand_data)
                    right_palm_orientation = palm_orientation(right_hand_data)

                    # Adding Transformed coordinates
                    wrist = np.array([0,0,0])
                    left_finger_bases = np.array([left_hand_data[5],
                                             left_hand_data[9],
                                             left_hand_data[13],
                                             left_hand_data[17]])
                    transformed_left_hand_coord = remove_rotation(left_hand_data, wrist, left_finger_bases)

                    right_finger_bases = np.array([right_hand_data[5],
                                                 right_hand_data[9],
                                                 right_hand_data[13],
                                                 right_hand_data[17]])
                    transformed_right_hand_coord = remove_rotation(right_hand_data, wrist, right_finger_bases)

                    # Adding rotation details
                    left_rotational_data = calculate_rotational_angles(left_hand_data, transformed_left_hand_coord)
                    right_rotational_data = calculate_rotational_angles(right_hand_data, transformed_right_hand_coord)

                    # Write data for this image to the CSV file
                    row_data = [filename]
                    row_data.extend(left_joint_angles.flatten())
                    row_data.extend(right_joint_angles.flatten())


                    csv_writer.writerow(row_data)




    print(f"Landmark data saved to {output_csv_path}")


# Usage
#folder_path = r"D:\Yr2\DSGP\Virtual Environment\DSGP\TamilDataset\TamilDataset\letter 2"
#output_csv_path = "hand_angles1.csv"
#getLandmarksFromFolder(folder_path, output_csv_path)

getLandmarksFromFolder("D:\Yr2\DSGP\Virtual Environment\DSGP\Sinhala dataset\Sinhala Images\S_Letter1", "S_angles1.csv")
getLandmarksFromFolder("D:\Yr2\DSGP\Virtual Environment\DSGP\Sinhala dataset\Sinhala Images\S_Letter2", "S_angles2.csv")
getLandmarksFromFolder("D:\Yr2\DSGP\Virtual Environment\DSGP\Sinhala dataset\Sinhala Images\S_Letter3", "S_angles3.csv")
getLandmarksFromFolder("D:\Yr2\DSGP\Virtual Environment\DSGP\Sinhala dataset\Sinhala Images\S_Letter4", "S_angles4.csv")
getLandmarksFromFolder("D:\Yr2\DSGP\Virtual Environment\DSGP\Sinhala dataset\Sinhala Images\S_Letter5", "S_angles5.csv")
getLandmarksFromFolder("D:\Yr2\DSGP\Virtual Environment\DSGP\Sinhala dataset\Sinhala Images\S_Letter6", "S_angles6.csv")
getLandmarksFromFolder("D:\Yr2\DSGP\Virtual Environment\DSGP\Sinhala dataset\Sinhala Images\S_Letter7", "S_angles7.csv")
getLandmarksFromFolder("D:\Yr2\DSGP\Virtual Environment\DSGP\Sinhala dataset\Sinhala Images\S_Letter8", "S_angles8.csv")
getLandmarksFromFolder("D:\Yr2\DSGP\Virtual Environment\DSGP\Sinhala dataset\Sinhala Images\S_Letter9", "S_angles9.csv")
getLandmarksFromFolder("D:\Yr2\DSGP\Virtual Environment\DSGP\Sinhala dataset\Sinhala Images\S_Letter10", "S_angles10.csv")
getLandmarksFromFolder("D:\Yr2\DSGP\Virtual Environment\DSGP\Sinhala dataset\Sinhala Images\S_Letter11", "S_angles11.csv")
getLandmarksFromFolder("D:\Yr2\DSGP\Virtual Environment\DSGP\Sinhala dataset\Sinhala Images\S_Letter12", "S_angles12.csv")
getLandmarksFromFolder("D:\Yr2\DSGP\Virtual Environment\DSGP\Sinhala dataset\Sinhala Images\S_Letter13", "S_angles13.csv")
getLandmarksFromFolder("D:\Yr2\DSGP\Virtual Environment\DSGP\Sinhala dataset\Sinhala Images\S_Letter14", "S_angles14.csv")
getLandmarksFromFolder("D:\Yr2\DSGP\Virtual Environment\DSGP\Sinhala dataset\Sinhala Images\S_Letter15", "S_angles15.csv")
getLandmarksFromFolder("D:\Yr2\DSGP\Virtual Environment\DSGP\Sinhala dataset\Sinhala Images\S_Letter16", "S_angles16.csv")
getLandmarksFromFolder("D:\Yr2\DSGP\Virtual Environment\DSGP\Sinhala dataset\Sinhala Images\S_Letter17", "S_angles17.csv")
getLandmarksFromFolder("D:\Yr2\DSGP\Virtual Environment\DSGP\Sinhala dataset\Sinhala Images\S_Letter18", "S_angles18.csv")
