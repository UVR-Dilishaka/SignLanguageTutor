from flask import request, jsonify
from flask_restx import Namespace, Resource
import pickle
from model import db, StudentSignMastery
import numpy as np
import random


adoptiveTutoring_ns = Namespace('tutorSystem', description='api end points for the adoptive tutoring system')

def greedy_search(student_id):
   
    mastery_records = StudentSignMastery.query.filter_by(student_id=student_id).all()

    if not mastery_records:
        return None 

    num_signs = len(mastery_records)
    sign_ids = [record.sign_id for record in mastery_records]
    mastery_levels = np.array([float(record.current_mastery_level) for record in mastery_records])

    epsilon = 0.1
    if random.random() < epsilon:
        selected_signs = random.sample(sign_ids, 4)
    else:
        
        selected_indices = np.argsort(mastery_levels)[:4]
        selected_signs = [sign_ids[i] for i in selected_indices]

    return selected_signs

class MultiarmedBandit(Resource):
    def get(self, student_id):
        selected_signs = greedy_search(student_id)

        if not selected_signs:
            return jsonify({"error": "No mastery records found for this student"}), 404

        return jsonify({
            "student_id": student_id,
            "selected_signs": selected_signs
        }), 200
    
    
@adoptiveTutoring_ns.route('/getnextsigns/<int:student_id>', methods=['GET'])
def get_greedy_search(student_id):
    
    selected_signs = greedy_search(student_id)

    if not selected_signs:
        return jsonify({"error": "No mastery records found for this student"}), 404
    
    return jsonify({
        "student_id": student_id,
        "selected_signs": selected_signs
    }), 200