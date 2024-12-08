import cv2
import mediapipe as mp
from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit
from flask_cors import CORS

# Create an instance of the Flask class
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# MediaPipe Hands setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# OpenCV Video Capture (from webcam)
cap = cv2.VideoCapture(0)

# Function to generate frames for streaming
def generate_frames():
    while True:
        # Read frame from the webcam
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame for correct orientation
        frame = cv2.flip(frame, 1)

        # Convert the frame to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame using MediaPipe
        result = hands.process(rgb_frame)

        # Initialize dictionary to store coordinates
        coordinates = {}

        # Draw landmarks on the frame and extract coordinates
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                # Draw landmarks on the frame
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Extract specific coordinates from the landmarks (wrist, index MCP, middle MCP)
                wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                index_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
                middle_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]

                # Store the coordinates in the dictionary
                coordinates = {
                    'wrist': (wrist.x, wrist.y),
                    'index_mcp': (index_mcp.x, index_mcp.y),
                    'middle_mcp': (middle_mcp.x, middle_mcp.y)
                }


                # Emit coordinates to the frontend
                socketio.emit('hand_coordinates', coordinates)

        # Encode the frame to JPEG and yield it for streaming
        ret, jpeg = cv2.imencode('.jpg', frame)
        if ret:
            frame = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# Route to display the live camera feed (video stream)
@app.route('/hand_detection')
def hand_detectionPage():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Route for homepage
@app.route('/')
def home():
    return render_template('hand_detection.html')

# Start the Flask server when running this script
if __name__ == '__main__':
    socketio.run(app, debug=True)
