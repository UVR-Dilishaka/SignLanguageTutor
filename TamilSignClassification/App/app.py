
from flask import Flask, request, jsonify
import pickle
import numpy as np

# Load the trained model
with open('random_forest_model.pkl', 'rb') as file:
    model = pickle.load(file)

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    # Get the data from the POST request
    data = request.get_json(force=True)
    
    # Convert the data into a numpy array
    features = np.array(data['features']).reshape(1, -1)
    
    # Make prediction using the loaded model
    prediction = model.predict(features)
    
    # Return the prediction as a JSON response
    return jsonify({'prediction': int(prediction[0])})

if __name__ == '__main__':
    app.run(debug=True)