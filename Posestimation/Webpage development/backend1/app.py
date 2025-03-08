from flask import Flask, jsonify, request, render_template
from flask_cors import CORS 
from flask_socketio import SocketIO, emit
from threading import Thread
import time


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

# Listen for 'landmark_data' event from React frontend
@socketio.on('landmark_data')
def handle_landmark_data(data):
    print("Received Landmark Data:", data)
    # You can process the data here, e.g., store in a database or perform other actions
    # For now, we're just printing it to the console


if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0")

