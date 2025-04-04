from flask import jsonify
from flask_restx import Namespace, Resource
from model import StudentSignMastery,PerformanceHistory,Sign
import numpy as np
import random
import pickle

from ext import db

adoptiveTutoring_ns = Namespace('tutorSystem', description='API endpoints for the adaptive tutoring system')




def selectSigns(student_id, language):
    # Join StudentSignMastery with Sign to filter by language
    mastery_records = (
        db.session.query(StudentSignMastery)
        .join(Sign, StudentSignMastery.sign_id == Sign.id)
        .filter(StudentSignMastery.student_id == student_id, Sign.language == language)
        .all()
    )

    if not mastery_records:
        return None

    sign_ids = [record.sign_id for record in mastery_records]
    mastery_levels = np.array([float(record.current_mastery_level) for record in mastery_records])

    # epsilon = 0.1
    # if random.random() < epsilon:
    #     selected_signs = random.sample(sign_ids, min(4, len(sign_ids)))  # Avoid out-of-range errors

    # else:
    #     selected_indices = np.argsort(mastery_levels)[:4]
    #     selected_signs = [sign_ids[i] for i in selected_indices]

    selected_signs = random.sample(sign_ids, min(4, len(sign_ids)))
    return selected_signs


@adoptiveTutoring_ns.route('/getnextsigns/<int:student_id>/<string:language>')
class MultiarmedBandit(Resource):
    def get(self, student_id, language):
        selected_signs = selectSigns(student_id, language)

        if not selected_signs:
            return {"error": "No mastery records found for this student or language"}, 404

        return {
            "student_id": student_id,
            "language": language,
            "selected_signs": selected_signs
        }, 200




# with open('rouster_model.pkl', 'rb') as file:
#     model = pickle.load(file)

# @adoptiveTutoring_ns.route('/updatestudentmastery/<int:student_id>/<int:sign_id>/<int:correct>')
# class UpdateMastery(Resource):


#     def post(self, student_id, sign_id, correct):
#         new_state = model.update_state(sign_id, student_id, correct)
#         new_estimated_mastery = model.get_mastery_prob(sign_id, student_id)
#         performance_history = PerformanceHistory(student_id=student_id, sign_id=sign_id, mastery_level=new_estimated_mastery)
#         performance_history.save()
#         student_sign_mastery = StudentSignMastery.query.filter_by(student_id=student_id, sign_id=sign_id).first()






