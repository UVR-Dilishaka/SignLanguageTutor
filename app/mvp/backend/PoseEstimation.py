from flask import request, jsonify
from flask_restx import Namespace, Resource
import numpy as np
import json
from ext import SLmodel, TLmodel  # Ensure TLmodel and SLmodel are trained

poseEstimation_ns = Namespace('poseEstimation', description='API for pose estimation')

@poseEstimation_ns.route("/hand_landmarks")
class HandLandmarks(Resource):
    def post(self):
        data = request.json
        language = data.get("language")
        print(language)  

        if language not in ["Sinhala", "Tamil"]:
            return {"error": "Invalid or missing language parameter. Use 'sinhala' or 'tamil'."}, 400

        landmarks_array = json_to_numpy(data)
        if landmarks_array is None:
            return {"error": "Invalid hand landmark data"}, 400
        
        # Compute angles
        angles = angle_listing(landmarks_array[0])
        
        # Prepare feature array for prediction
        features = np.array(angles).reshape(1, -1)
        print("Extracted Features: ", features)
        
        # Select the appropriate model based on language
        model = TLmodel if language == "Tamil" else SLmodel
        
        # Make prediction
        prediction = model.predict(features)
        print("Prediction: ", prediction)

        return jsonify({'prediction': int(prediction[0])})

# Utility function to convert JSON to NumPy
def json_to_numpy(data):
    if "hands" in data and isinstance(data["hands"], list) and len(data["hands"]) > 0:
        hands_array = np.array(data["hands"], dtype=np.float32)
        if hands_array.shape[0] > 0 and hands_array.shape[1:] == (21, 3):
            return hands_array
    return None 

# Function to compute angles in bulk
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

# Extract relevant angles
def angle_listing(landmarks):
    point_indices = [
        (1, 2, 3), (0, 5, 6), (0, 9, 10), (0, 13, 14), (0, 17, 18),
        (5, 6, 7), (9, 10, 11), (13, 14, 15), (17, 18, 19),
        (6, 7, 8), (10, 11, 12), (14, 15, 16), (18, 19, 20),
        (0, 1, 2), (2, 3, 4), (2, 1, 5)
    ]
    return calculate_angle_bulk(landmarks, point_indices)
