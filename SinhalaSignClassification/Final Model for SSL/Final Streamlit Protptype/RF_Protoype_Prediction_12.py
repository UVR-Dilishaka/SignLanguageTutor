import streamlit as st
import cv2
import mediapipe as mp
import pandas as pd
import numpy as np
import pickle  # For loading the trained model
from PIL import Image
import os
import time  # To avoid freezing issues

import tensorflow as tf
tf.compat.v1.reset_default_graph()


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

# Load the trained model
@st.cache_resource
def load_model():
    model_path = "./best_rf_model_with_12.pkl"  # Update this path as needed
    if not os.path.exists(model_path):
        st.error(f"Model file not found at {model_path}. Please ensure the file exists.")
        return None
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    return model

model = load_model()

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
frame_window = st.image([])  # For live webcam
prediction_placeholder = st.empty()  # To display prediction

# Webcam processing loop
if run:
    cap = cv2.VideoCapture(0)
    with mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
        while cap.isOpened():
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

                    for i, landmark in enumerate(hand_landmarks.landmark):
                        # Normalize the coordinates by subtracting the wrist position
                        norm_x = landmark.x - wrist_x
                        norm_y = landmark.y - wrist_y
                        norm_z = landmark.z - wrist_z

                        # Append to landmarks array
                        landmarks_array[i] = [landmark.x, landmark.y, landmark.z]

                    # Calculate angles using the landmark array
                    angles = calculate_angle_bulk(landmarks_array, point_indices)

                    # Perform prediction using the loaded model
                    if model:
                        angle_payload = np.array(angles[:16]).reshape(1, -1)  # Adjust number of angles if needed
                        predicted_sign = model.predict(angle_payload)[0]
                        prediction_placeholder.write(f"Predicted Sign: {predicted_sign}")

            # Update the frame in Streamlit
            frame_window.image(frame)

            # Limit frame rate to prevent Streamlit crash
            time.sleep(0.05)

    cap.release()
    cv2.destroyAllWindows()
