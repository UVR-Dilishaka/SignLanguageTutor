from flask import Flask, request, jsonify
import pickle
import pandas as pd

# Load the trained model once during initialization
with open("random_forest_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

# Initialize Flask app
app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get JSON data from request
        data = request.get_json()

        # Check if all required fields are present
        required_columns = ['THUMB_MCP_angle', 'INDEX_MCP_angle', 'MIDDLE_MCP_angle', 'RING_MCP_angle',
'PINKY_MCP_angle', 'INDEX_PIP_angle', 'MIDDLE_PIP_angle', 'RING_PIP_angle',
'PINKY_PIP_angle', 'INDEX_DIP_angle', 'MIDDLE_DIP_angle', 'RING_DIP_angle',
'PINKY_DIP_angle', 'THUMB_TMC_angle', 'THUMB_IP_angle', 'THUMB_INDEX_Abduction_angle']
  # replace with actual feature names
        missing_columns = [col for col in required_columns if col not in data]
        if missing_columns:
            return jsonify({"error": f"Missing columns: {', '.join(missing_columns)}"}), 400

        # Convert JSON to DataFrame
        features = pd.DataFrame([data])

        # Make prediction
        prediction = model.predict(features)

        # Return prediction as JSON
        return jsonify({"prediction": int(prediction[0])})
    except KeyError as e:
        return jsonify({"error": f"Missing key: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
