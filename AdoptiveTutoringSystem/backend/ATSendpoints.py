from flask import Flask, request
from flask_restx import Api, Namespace, Resource
from flask_cors import CORS
import numpy as np
import pickle
from pyBKT.models import Model, Roster


roster_ns = Namespace('roster', description='Operations related to student skill mastery using BKT')


def load_model():
    with open('pybkt_model.pkl', 'rb') as file:
        model = pickle.load(file)
    return model


model = load_model()
students = ['Jeff', 'Bob', 'Sarah']  
skills = ['Calculate unit rate']     
roster = Roster(students=students, skills=skills, model=model)

def create_app():
    app = Flask(__name__)
    
    
    CORS(app)
    
 
    api = Api(app, doc='/docs')
    

    api.add_namespace(roster_ns)

    return app

@roster_ns.route('/<string:student>/<string:skill>')
class RosterResource(Resource):
    def get(self, student, skill):
        """
        Get student's mastery state and probability for a specific skill
        """
        mastery_type = roster.get_state_type(skill, student)
        mastery_prob = roster.get_mastery_prob(skill, student)
        return {
            'student': student,
            'skill': skill,
            'mastery_state': mastery_type.name,
            'mastery_probability': mastery_prob
        }

    def put(self, student, skill):
        """
        Update student's mastery state based on responses (correct or incorrect).
        Expects a list of responses (1 for correct, 0 for incorrect).
        """
        data = request.get_json()  # Get the JSON data from the request
        if 'responses' not in data:
            return {'message': 'Responses list is required.'}, 400
        
        responses = np.array(data['responses'])
        
        # Update student's state with the responses
        updated_state = roster.update_state(skill, student, responses)
        
        # Return the updated mastery state and probability
        mastery_type = roster.get_state_type(skill, student)
        mastery_prob = roster.get_mastery_prob(skill, student)
        
        return {
            'student': student,
            'skill': skill,
            'mastery_state': mastery_type.name,
            'mastery_probability': mastery_prob
        }


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
