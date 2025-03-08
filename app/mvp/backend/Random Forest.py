from flask import Flask, request, jsonify
import pickle
import numpy as np

# Load the trained model
with open('RF.pkl', 'rb') as file:
    model = pickle.load(file)

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    # Get the data from the POST request
    data = request.get_json(force=True)
    
    # Extract the features from the JSON data
    # Assuming the JSON data is in the format you provided earlier
    features = np.array([
        data['Right_THUMB_MCP_angle'],
        data['Right_INDEX_MCP_angle'],
        data['Right_MIDDLE_MCP_angle'],
        data['Right_RING_MCP_angle'],
        data['Right_PINKY_MCP_angle'],
        data['Right_INDEX_PIP_angle'],
        data['Right_MIDDLE_PIP_angle'],
        data['Right_RING_PIP_angle'],
        data['Right_PINKY_PIP_angle'],
        data['Right_INDEX_DIP_angle'],
        data['Right_MIDDLE_DIP_angle'],
        data['Right_RING_DIP_angle'],
        data['Right_PINKY_DIP_angle'],
        data['Right_THUMB_TMC_angle'],
        data['Right_THUMB_IP_angle'],
        data['Right_THUMB_INDEX_Abduction_angle']
    ]).reshape(1, -1)
    
    # Make prediction using the loaded model
    prediction = model.predict(features)
    
    # Return the prediction as a JSON response
    return jsonify({'prediction': int(prediction[0])})

if __name__ == '__main__':
    app.run(debug=True)