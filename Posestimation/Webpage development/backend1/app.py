from flask import Flask, jsonify, request, render_template
from flask_cors import CORS 
from flask_socketio import SocketIO, emit
from threading import Thread
import time
import numpy as np
import pickle


app = Flask(__name__)
CORS(app)  # Allow requests from React
socketio = SocketIO(app, cors_allowed_origins="*")

# Variables
username  = "User11"
current_level = 1
level_data = {
    1: ['A','B','C','D','E'],
    2: ["F","G","H","I",'J'],
    3: ['K','L','M','N','O']
}
all_letters = ['A','B','C','D','E',"F","G","H","I",'J','K','L','M','N','O']
completed_letters = []
hint_usage = [True,False,True,False,False,
              False,False,False,False,False,
              False,False,False,False,False]
score = 0
selected_letter = ""
allowed_time = 20
match_detected = False

model_path = "D:/Yr2/DSGP/Virtual Environment/DSGP/web_testing/backend1/RF.pkl"
with open(model_path, 'rb') as f:
    model = pickle.load(f)


# Testing if flask is connected
@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello from Flask!"})

# Response for username request
@app.route('/api/username', methods=['GET'])
def get_username():
    return jsonify({"username": username})

@app.route("/api/get_current_level")
def get_current_level():
    return jsonify({
        "level": current_level,
        "assigned_letters": level_data.get(current_level, [])
    })

# Function to change level in Flask and notify React
def change_level(new_level):
    global current_level
    if new_level in level_data:
        current_level = new_level
        assigned_letters = level_data[new_level]
        socketio.emit("level_updated", {"level": new_level, "assigned_letters": assigned_letters})

# Sending initial score at the start
@app.route("/api/get_score")
def get_score():
    return jsonify({"score": score})

# Updating score in real time in react
@app.route("/api/update_score", methods=["POST"])
def update_score():
    global score
    new_score = request.json.get('score')  # Get the score from the request body
    score = new_score
    socketio.emit("score_updated", {"score": score})  # Emit the new score to all clients
    return jsonify({"message": "Score updated", "score": score})

# Updating selected_letter in real time
@socketio.on("update_selected_letter")
def update_selected_letter(data):
    global selected_letter
    selected_letter = data["letter"]
    print(f"Updated selected letter: {selected_letter}")



# Function that updates the score externally
def update_score_external(new_score):
    global score
    score = new_score
    socketio.emit("score_updated", {"score": score})  # Emit the updated score
    print(f"Score updated to {score}")

update_score_external(325)


# Sending hint usage to frontend initialy
@app.route("/api/get_hint_usage", methods=["GET"])
def get_hint_usage():
    return jsonify({"hint_usage": hint_usage})

# Updating backend hint_usage variable after hint button click
@app.route("/api/update_hint_usage", methods=["POST"])
def update_hint_usage():
    global hint_usage
    # Get the updated hint_usage array from the request
    hint_usage = request.json.get('hint_usage')  # This will be an array
    print(hint_usage)
    return jsonify({"message": "Hint usage updated", "hint_usage": hint_usage})

# Function to predict using ML model
def predict_letter(angles):
    input_data = np.array([angles])
    predicted_letter = model.predict(input_data)[0]
    print("predicted letter :", predicted_letter)

    if predicted_letter == all_letters.index(selected_letter)+1:
        match_detected = True
        print(f"Match detected: {predicted_letter}")
        socketio.emit("match_status", match_detected)
        # Do score changing and other stuff here

# Function to receive detected time
@socketio.on('match_detected')
def handle_match_detected(data):
    time_left = data.get('timeLeft')
    print(f"Match detected at {time_left / 1000}s")
    # Use the time for calculating time remaining and other things
    # Then reset time_left


# Handle receiving landmarks from the client
@socketio.on('hand_landmarks')
def handle_landmarks(data):
    landmarks_array = json_to_numpy(data)
    angles = angle_listing(landmarks_array[0])
    print(angles)
    predict_letter(angles)

def json_to_numpy(data):
    if "hands" in data and isinstance(data["hands"], list) and len(data["hands"]) > 0:
        hands_array = np.array(data["hands"], dtype=np.float32)
        if hands_array.shape[0] > 0 and hands_array.shape[1:] == (21, 3):  # Ensure valid shape
            return hands_array
    return None 



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

# Sending the match_detected value using websockets


if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0")

