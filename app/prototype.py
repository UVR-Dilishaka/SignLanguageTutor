import streamlit as st
import cv2
import mediapipe as mp
import pandas as pd

# List of landmark names
landmark_names = [
    "WRIST",
    "THUMB_CMC", "THUMB_MCP", "THUMB_IP", "THUMB_TIP",
    "INDEX_FINGER_MCP", "INDEX_FINGER_PIP", "INDEX_FINGER_DIP", "INDEX_FINGER_TIP",
    "MIDDLE_FINGER_MCP", "MIDDLE_FINGER_PIP", "MIDDLE_FINGER_DIP", "MIDDLE_FINGER_TIP",
    "RING_FINGER_MCP", "RING_FINGER_PIP", "RING_FINGER_DIP", "RING_FINGER_TIP",
    "PINKY_MCP", "PINKY_PIP", "PINKY_DIP", "PINKY_TIP"
]

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

st.title("Sign Language Tutor")

st.header("Webcam Live Feed")
run = st.checkbox("Run Webcam")

if run:
    cap = cv2.VideoCapture(0)
    frame_window = st.image([])
    landmarks_table = st.empty()  # Placeholder for the table

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

            # Update the frame in Streamlit
            frame_window.image(frame)

            # If there are landmarks, display them in a table
            if landmarks_data:
                df = pd.DataFrame(landmarks_data)
                landmarks_table.table(df)

    cap.release()
