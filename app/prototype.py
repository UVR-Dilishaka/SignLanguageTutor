

import streamlit as st
import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils


st.title("Sign Language Tutor")


st.header("Webcam Live Feed")
run = st.checkbox("Run Webcam")

if run:
    cap = cv2.VideoCapture(0)
    frame_window = st.image([])

    with mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
        while run:
            ret, frame = cap.read()
            if not ret:
                st.error("Failed to capture image")
                break

            # Flip the image horizontally for a selfie-view display.
            frame = cv2.flip(frame, 1)

            # Convert the BGR image to RGB.
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(frame_rgb)

            # Draw hand landmarks if detected
            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Display the image with hand landmarks
            frame_window.image(frame)

    cap.release()
