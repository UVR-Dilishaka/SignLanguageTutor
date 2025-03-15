from flask import request, jsonify
from flask_restx import Namespace, Resource
import pickle
import numpy as np


Tamil_predict_ns = Namespace('tamilSignPredict', description='Prediction endpoint for Tamil Sign Language Classification')


with open('./Model/RF.pkl', 'rb') as file:
    model = pickle.load(file)

@Tamil_predict_ns.route('/')
class Predict(Resource):
    def post(self):
        data = request.get_json(force=True)

    
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

        
        prediction = model.predict(features)

        return jsonify({'prediction': int(prediction[0])})
