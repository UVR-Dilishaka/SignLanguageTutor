import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import pickle
import pandas as pd
import time
from datetime import datetime

# Mediapipe utilities
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Define point indices for angle calculation
point_indices = [
    (1, 2, 3), (0, 5, 6), (0, 9, 10), (0, 13, 14), (0, 17, 18),
    (5, 6, 7), (9, 10, 11), (13, 14, 15), (17, 18, 19),
    (6, 7, 8), (10, 11, 12), (14, 15, 16), (18, 19, 20),
    (0, 1, 2), (2, 3, 4), (2, 1, 5)
]

# Tamil sign mappings
tamil_letters = {
    1: "அ", 2: "ஆ", 3: "இ", 4: "ஈ", 5: "உ",
    6: "ஊ", 7: "எ", 8: "ஏ", 9: "ஐ", 10: "ஒ",
    11: "ஓ", 12: "ஔ"
}

# Sinhala sign mappings
sinhala_letters = {
    1: "අ", 2: "ආ", 3: "ඇ", 4: "ඉ", 5: "උ", 
    6: "එ", 7: "ග", 8: "ව", 9: "ඩ", 10: "ද", 
    11: "ය", 12: "හ"
}

# Load the trained models
@st.cache_resource
def load_models():
    with open("./Model/RF.pkl", "rb") as f_tamil, open("./Model/RF_SL.pkl", "rb") as f_sinhala:
        model_tamil = pickle.load(f_tamil)
        model_sinhala = pickle.load(f_sinhala)
    return model_tamil, model_sinhala

model_tamil, model_sinhala = load_models()

# CSV file for recording data
data_file = "sign_language_data.csv"
students_file = "students.txt"

# Load students
if "students" not in st.session_state:
    try:
        with open(students_file, "r") as f:
            st.session_state.students = [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        st.session_state.students = []

# UI Elements
st.title("Sign Language Data Collection Tool")

# Student Management
st.sidebar.header("Student Management")
student_name = st.sidebar.text_input("Enter Student Name")
if st.sidebar.button("Add Student"):
    if student_name and student_name not in st.session_state.students:
        st.session_state.students.append(student_name)
        with open(students_file, "a") as f:
            f.write(student_name + "\n")
        st.sidebar.success(f"Added student: {student_name}")

# Language selection
st.sidebar.header("Select Language")
language = st.sidebar.radio("Choose a language", ["Tamil", "Sinhala"])

# Dropdown for student selection
selected_student = st.sidebar.selectbox("Select Student", st.session_state.get("students", []))
st.sidebar.write(f"Current Student: {selected_student}")

# Select sign based on language
if language == "Tamil":
    selected_sign = st.sidebar.selectbox("Choose a Tamil Sign", list(tamil_letters.values()))
    model = model_tamil
    sign_dict = tamil_letters
else:
    selected_sign = st.sidebar.selectbox("Choose a Sinhala Sign", list(sinhala_letters.values()))
    model = model_sinhala
    sign_dict = sinhala_letters

if st.sidebar.button("Start Recognition"):
    st.session_state.start_time = time.time()
    st.session_state.sign_in_progress = True

# Webcam Feed
st.header("Webcam Live Feed")
frame_window = st.image([])
prediction_placeholder = st.empty()

def calculate_angle_bulk(landmarks, point_indices):
    p1 = landmarks[[i[0] for i in point_indices]]
    p2 = landmarks[[i[1] for i in point_indices]]
    p3 = landmarks[[i[2] for i in point_indices]]
    
    ba = p1 - p2
    bc = p3 - p2
    
    dot_products = np.sum(ba * bc, axis=1)
    magnitudes_ba = np.linalg.norm(ba, axis=1)
    magnitudes_bc = np.linalg.norm(bc, axis=1)
    
    cosine_angles = dot_products / (magnitudes_ba * magnitudes_bc)
    cosine_angles = np.clip(cosine_angles, -1.0, 1.0)
    angles_rad = np.arccos(cosine_angles)
    angles_deg = np.rad2deg(angles_rad)
    return angles_deg

def record_result(student, skill_id, correctness):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data = pd.DataFrame([[student, skill_id, 1, correctness, timestamp]],
                        columns=["Student ID", "Skill ID", "Opportunity Count", "Correctness", "Timestamp"])
    data.to_csv(data_file, mode='a', header=not pd.io.common.file_exists(data_file), index=False)
    st.sidebar.success(f"Recorded: {student}, {skill_id}, {correctness}")

if "sign_in_progress" not in st.session_state:
    st.session_state.sign_in_progress = False

if st.session_state.sign_in_progress:
    cap = cv2.VideoCapture(0)
    correct_sign_start = None
    correct_sign_detected = False
    
    with mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
        while time.time() - st.session_state.start_time < 5:
            ret, frame = cap.read()
            if not ret:
                st.error("Failed to capture image")
                break

            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(frame_rgb)

            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    landmarks_array = np.array([[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark])
                    angles = calculate_angle_bulk(landmarks_array, point_indices)

                    predicted_sign = model.predict([angles[:16]])[0]
                    prediction_text = sign_dict.get(predicted_sign, "Unknown")
                    prediction_placeholder.write(f"Predicted Sign: {prediction_text}")
                    
                    if prediction_text == selected_sign:
                        if correct_sign_start is None:
                            correct_sign_start = time.time()
                        elif time.time() - correct_sign_start >= 1:
                            correct_sign_detected = True
                            break
                    else:
                        correct_sign_start = None
            
            frame_window.image(frame)
        
        correctness = int(correct_sign_detected)
        record_result(selected_student, selected_sign, correctness)

    
    cap.release()
    st.session_state.sign_in_progress = False
