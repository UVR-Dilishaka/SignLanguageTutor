from flask import Flask, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

# Load the trained model
with open("best_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        # Convert JSON data to NumPy array
        features = np.array(data["features"]).reshape(1, -1)

        # Check the input shape
        expected_features = model.n_features_in_
        if features.shape[1] != expected_features:
            return jsonify({"error": f"Model expects {expected_features} features, but received {features.shape[1]}."}), 400

        # Make a prediction
        prediction = model.predict(features)

        return jsonify({"prediction": int(prediction[0])})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True, port=5000)
