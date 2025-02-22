import json
from flask import Flask, request,send_from_directory
from flask_socketio import SocketIO, emit
import numpy as np
import os

def json_to_numpy(data):
    if "hands" in data and isinstance(data["hands"], list) and len(data["hands"]) > 0:
        hands_array = np.array(data["hands"], dtype=np.float32)
        if hands_array.shape[0] > 0 and hands_array.shape[1:] == (21, 3):  # Ensure valid shape
            return hands_array
    return None 


def normalize_landmarks(landmarks):
    """Normalize landmarks by shifting and scaling."""
    normalized_landmarks = landmarks - landmarks[0]  # Shifting 
    hand_size = np.linalg.norm(landmarks[9] - landmarks[0])  # Palm size
    if hand_size > 0:
        normalized_landmarks /= hand_size 
    return normalized_landmarks

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


def angle_listing(landmarks):
    # Define the triplets of points for which angles are needed
    point_indices = [
        (1, 2, 3), (0, 5, 6), (0, 9, 10), (0, 13, 14), (0, 17, 18),
        (5, 6, 7), (9, 10, 11), (13, 14, 15), (17, 18, 19),
        (6, 7, 8), (10, 11, 12), (14, 15, 16), (18, 19, 20),
        (0, 1, 2), (2, 3, 4), (2, 1, 5)
    ]

    # Calculate angles in bulk
    angle_list = calculate_angle_bulk(landmarks, point_indices)
    return angle_list


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Serving the HTML file
@app.route('/')
def index():
    return send_from_directory(os.getcwd(), 'frontend.html')

# Serving the main.js file (as static)
@app.route('/main.js')
def serve_js():
    return send_from_directory(os.getcwd(), 'main.js')

# Handle receiving landmarks from the client
@socketio.on('hand_landmarks')
def handle_landmarks(data):
    print("Received landmarks:", data)  # Log the received landmarks

    landmarks_array = json_to_numpy(data)
    if landmarks_array is None or landmarks_array.shape[0] == 0:
        emit('hand_landmarks', {"error": "No hand detected"}, room=request.sid)
        return  # Exit function if no valid data

    # Process first detected hand
    normalized_landmarks = normalize_landmarks(landmarks_array[0])
    angles = angle_listing(landmarks_array[0])

    response_data = {
        "original_landmarks": landmarks_array[0].tolist(),
        "normalized_landmarks": normalized_landmarks.tolist(),
        "angles": angles.tolist()
    }

    emit('hand_landmarks', response_data, room=request.sid)

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)


