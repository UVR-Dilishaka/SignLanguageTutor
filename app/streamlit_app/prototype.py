import streamlit as st
import cv2
import mediapipe as mp
import pandas as pd
import numpy as np
from PIL import Image

# List of landmark names
landmark_names = [
    "WRIST",
    "THUMB_CMC", "THUMB_MCP", "THUMB_IP", "THUMB_TIP",
    "INDEX_FINGER_MCP", "INDEX_FINGER_PIP", "INDEX_FINGER_DIP", "INDEX_FINGER_TIP",
    "MIDDLE_FINGER_MCP", "MIDDLE_FINGER_PIP", "MIDDLE_FINGER_DIP", "MIDDLE_FINGER_TIP",
    "RING_FINGER_MCP", "RING_FINGER_PIP", "RING_FINGER_DIP", "RING_FINGER_TIP",
    "PINKY_MCP", "PINKY_PIP", "PINKY_DIP", "PINKY_TIP"
]

# Mediapipe utilities
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Define the triplets of points for which angles are needed
point_indices = [
    (1, 2, 3), (0, 5, 6), (0, 9, 10), (0, 13, 14), (0, 17, 18),
    (5, 6, 7), (9, 10, 11), (13, 14, 15), (17, 18, 19),
    (6, 7, 8), (10, 11, 12), (14, 15, 16), (18, 19, 20),
    (0, 1, 2), (2, 3, 4), (2, 1, 5)
]

def calculate_angle_bulk(landmarks, point_indices):
    p1 = landmarks[[i[0] for i in point_indices]]
    p2 = landmarks[[i[1] for i in point_indices]]
    p3 = landmarks[[i[2] for i in point_indices]]

    # Compute vectors
    ba = p1 - p2  # Vector from p2 to p1
    bc = p3 - p2  # Vector from p2 to p3

    # Compute dot products and magnitudes
    dot_products = np.sum(ba * bc, axis=1)  # Dot product for each triplet
    magnitudes_ba = np.linalg.norm(ba, axis=1)
    magnitudes_bc = np.linalg.norm(bc, axis=1)

    # Calculate angles (clip to handle floating-point errors)
    cosine_angles = dot_products / (magnitudes_ba * magnitudes_bc)
    cosine_angles = np.clip(cosine_angles, -1.0, 1.0)
    angles_rad = np.arccos(cosine_angles)

    # Convert to degrees
    angles_deg = np.rad2deg(angles_rad)
    return angles_deg

st.title("Sign Language Tutor")

st.header("Webcam Live Feed")
run = st.checkbox("Run Webcam")

show_landmarks_legend = False

if run:
    cap = cv2.VideoCapture(0)
    frame_window = st.image([])
    landmarks_table = st.empty()  # Placeholder for the table
    angles_table = st.empty()  # Placeholder for the angles table

    with mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
        while run:
            ret, frame = cap.read()
            if not ret:
                st.error("Failed to capture image")
                break

            # Flip the frame for a mirror view
            frame = cv2.flip(frame, 1)

            # Convert the image to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(frame_rgb)

            landmarks_data = []
            angle_data = []  # To store angle information

            

            # If hand landmarks are detected
            if result.multi_hand_landmarks and result.multi_handedness:
                for hand_idx, (hand_landmarks, handedness) in enumerate(
                        zip(result.multi_hand_landmarks, result.multi_handedness)):

                    # Identify the hand as "Left" or "Right"
                    hand_label = handedness.classification[0].label

                    # Draw landmarks on the frame
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    # Get wrist coordinates for normalization
                    wrist = hand_landmarks.landmark[0]
                    wrist_x, wrist_y, wrist_z = wrist.x, wrist.y, wrist.z

                    # Prepare a list to store landmarks as an array
                    landmarks_array = np.zeros((21, 3))

                    # Extract landmark coordinates and associate them with the corresponding name
                    for i, landmark in enumerate(hand_landmarks.landmark):
                        # Normalize the coordinates by subtracting the wrist position
                        norm_x = landmark.x - wrist_x
                        norm_y = landmark.y - wrist_y
                        norm_z = landmark.z - wrist_z

                        # Append both normalized and original coordinates to the data
                        landmarks_data.append({
                            'Hand': hand_label,  # Left or Right hand
                            'Landmark': landmark_names[i],
                            'Normalized_X': norm_x,
                            'Normalized_Y': norm_y,
                            'Normalized_Z': norm_z
                        })

                        # Store landmark coordinates into the array for angle calculation
                        landmarks_array[i] = [landmark.x, landmark.y, landmark.z]

                    # Calculate angles using the landmark array
                    angles = calculate_angle_bulk(landmarks_array, point_indices)

                    # Prepare angle data for display, including point indices
                    for idx, angle in enumerate(angles):
                        point_indices_str = f"({point_indices[idx][0]}, {point_indices[idx][1]}, {point_indices[idx][2]})"
                        angle_data.append({
                            'Hand': hand_label,
                            'Angle_Index': f"Angle_{idx + 1}",
                            'Angle_Degrees': angle,
                            'Point_Indices': point_indices_str
                        })
                    

            # Update the frame in Streamlit
            frame_window.image(frame)



            # If there are landmarks, display them in a table
            if landmarks_data:
                df_landmarks = pd.DataFrame(landmarks_data)
                landmarks_table.table(df_landmarks)

            if show_landmarks_legend == False:
                        legend_image = Image.open('app/hand-landmarks.png')  # Replace with the path to your image
                        st.image(legend_image, caption="Hand Landmark Legend", use_container_width=True)

                        show_landmarks_legend = True

            # If there are angles, display them in a table
            if angle_data:
                df_angles = pd.DataFrame(angle_data)
                angles_table.table(df_angles)

    
            
    cap.release()


    
