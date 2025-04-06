import atexit
import pickle
from flask import Flask, request
from flask_cors import CORS
from flask_restx import Api, Resource, fields
import numpy as np

app = Flask(__name__)
CORS(app)
api = Api(app, title="BKT API", version="1.0", doc="/docs")

skills = [str(i) for i in range(1, 25)] 


# === Load model and/or roster ===

with open('Model/bkt_model.pkl', 'rb') as f:
    roster = pickle.load(f)
    print("Roster loaded from bkt_model.pkl.")
    print(roster)

# === Save model/roster on shutdown ===
@atexit.register
def save_roster():
    with open('Model/bkt_model.pkl', 'wb') as f:
        pickle.dump(roster, f)
    print("Roster saved to bkt_model.pkl on shutdown.")

# === API Models ===
student_model = api.model('Student', {
    'student': fields.String(required=True),
})

update_model = api.model('Update', {
    'student': fields.String(required=True),
    'skill': fields.String(required=True),
    'response': fields.Integer(required=True) 
})

# === Routes ===

@api.route('/add_student')
class AddStudent(Resource):
    @api.expect(student_model)
    def post(self):
        data = request.get_json()
        student = data['student']
        for skill in skills:
            roster.add_student(skill, student)
            print(f"Student '{student}' added for skill '{skill}'.")
        return {"message": f"Student '{student}' added for all skills."}




@api.route('/update_student')
class UpdateStudent(Resource):
    @api.expect(update_model)
    def post(self):
        data = request.get_json()
        student = data['student']
        skill = data['skill']
        response = data['response'] 
        state = roster.update_state(skill, student, response)  
        return {
            'message': f"Updated '{student}' for skill '{skill}'",
            'mastery_prob': state.get_mastery_prob(),
            'correct_prob': state.get_correct_prob()
        }


@api.route('/get_mastery')
@api.doc(params={'student': 'Student name', 'skill': 'Skill name'})
class GetMastery(Resource):
    def get(self):
        student = request.args.get('student')
        skill = request.args.get('skill')
        prob = roster.get_mastery_prob(skill, student)
        return {
            'student': student,
            'skill': skill,
            'mastery_prob': prob
        }

# === Start Flask ===
if __name__ == '__main__':
    app.run(debug=True,port=5005)
