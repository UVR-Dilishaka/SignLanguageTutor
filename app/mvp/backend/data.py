
from flask_restx import Namespace, Resource,fields
from flask import request
from model import User,Sign,Activity,PerformanceHistory,StudentSignMastery
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity

data_ns = Namespace('data', description='database operations')


user_model = data_ns.model(
    'User', {
        'id': fields.Integer(),
        'username': fields.String(required=True),
        'email': fields.String(required=True),
        'password': fields.String(required=True),
        'isteacher': fields.Boolean(required=True)
    }
)


sign_model = data_ns.model(
    'Sign', {
        'id': fields.Integer(),
        'language': fields.String(required=True),
        'mono_code_characters': fields.String(required=True),
        'predictive_label': fields.String()
    }
)


activity_model = data_ns.model(
    'Activity', {
        'id': fields.Integer(),
        'student_id': fields.Integer(required=True),
        'sign_id': fields.Integer(required=True),
        'result': fields.Float(required=True),
        'timetaken': fields.Float(),
        'hint_used': fields.Boolean(),
        'timestamp': fields.DateTime()
    }
)

performance_history_model = data_ns.model(
    'PerformanceHistory', {
        'id': fields.Integer(),
        'student_id': fields.Integer(required=True),
        'sign_id': fields.Integer(required=True),
        'mastery_level': fields.Float(),
        'timestamp': fields.DateTime()
    }
)

student_sign_mastery_model = data_ns.model(
    'StudentSignMastery', {
        'student_id': fields.Integer(required=True),
        'sign_id': fields.Integer(required=True),
        'current_mastery_level': fields.Float(),
        'last_updated': fields.DateTime()
    }
)



@data_ns.route('/ping-protected')
class HelloResource(Resource):
    
    @jwt_required()
    def get (self):
        return {"txt":"protected route acessed"}
    

@data_ns.route('/ping')
class HelloResource(Resource):
    def get (self):
        return {"txt":"unprotected route acessed"}
    


    
@data_ns.route('/users')
class UserResource(Resource):

    @data_ns.marshal_list_with(user_model)  
    def get(self):
        """Get all users"""
        users = User.query.all()
        return users



@data_ns.route('/user/<string:username>')
class SingleUserResource(Resource):

    @jwt_required()
    @data_ns.marshal_with(user_model) 
    def get(self, username):
        """Get a user by username"""
        current_user = get_jwt_identity()  # Get the current user's identity from JWT
        user = User.query.filter_by(username=username).first_or_404()

        # Validate if the current user matches the user being accessed
        if user.username != current_user:
            return {"message": "You do not have permission to access this user."}, 403

        return user



@data_ns.route('/is_teacher')
class IsTeacher(Resource):

    @jwt_required()  # Requires a valid JWT to access
    def get(self):
        """Check if the current user is a teacher"""
        current_user = get_jwt_identity()  # Get the current user's identity from JWT
        user = User.query.filter_by(username=current_user).first()

        if user is None:
            return {"message": "User not found"}, 404

        # Return True if the user is a teacher, otherwise False
        return {"is_teacher": user.isteacher}, 200



@data_ns.route('/signs')
class SignResource(Resource):

    @data_ns.marshal_with(sign_model)
    def get(self):
        """Get all signs"""
        signs = Sign.query.all()
        return signs

    @data_ns.marshal_with(sign_model)
    def post(self):
        """Create a new sign"""
        data = request.get_json()
        new_sign = Sign(
            language=data.get('language'),
            mono_code_characters=data.get('mono_code_characters'),
            predictive_label=data.get('predictive_label')
        )
        new_sign.save()
        return new_sign, 201


@data_ns.route('/signs/<int:id>')
class SingleSignResource(Resource):

    @data_ns.marshal_with(sign_model)
    def get(self, id):
        """Get a sign by ID"""
        sign = Sign.query.get_or_404(id)
        return sign

    @data_ns.marshal_with(sign_model)
    def put(self, id):
        """Update a sign by ID"""
        sign_to_update = Sign.query.get_or_404(id)
        data = request.get_json()
        sign_to_update.update(
            data.get('language'),
            data.get('mono_code_characters'),
            data.get('predictive_label')
        )
        return sign_to_update

    @data_ns.marshal_with(sign_model)
    def delete(self, id):
        """Delete a sign by ID"""
        sign_to_delete = Sign.query.get_or_404(id)
        sign_to_delete.delete()
        return sign_to_delete





@data_ns.route('/activities')
class ActivityResource(Resource):

    @data_ns.marshal_with(activity_model)
    def get(self):
        """Get all activities"""
        activities = Activity.query.all()
        return activities

    @data_ns.marshal_with(activity_model)
    def post(self):
        """Create a new activity"""
        data = request.get_json()
        new_activity = Activity(
            student_id=data.get('student_id'),
            sign_id=data.get('sign_id'),
            result=data.get('result'),
            timetaken=data.get('timetaken'),
            hint_used=data.get('hint_used')
        )
        new_activity.save()
        return new_activity, 201


@data_ns.route('/activities/<int:id>')
class SingleActivityResource(Resource):

    @data_ns.marshal_with(activity_model)
    def get(self, id):
        """Get an activity by ID"""
        activity = Activity.query.get_or_404(id)
        return activity

    @data_ns.marshal_with(activity_model)
    def put(self, id):
        """Update an activity by ID"""
        activity_to_update = Activity.query.get_or_404(id)
        data = request.get_json()
        activity_to_update.update(
            data.get('result'),
            data.get('timetaken'),
            data.get('hint_used')
        )
        return activity_to_update

    @data_ns.marshal_with(activity_model)
    def delete(self, id):
        """Delete an activity by ID"""
        activity_to_delete = Activity.query.get_or_404(id)
        activity_to_delete.delete()
        return activity_to_delete




@data_ns.route('/performance_histories')
class PerformanceHistoryResource(Resource):

    @data_ns.marshal_with(performance_history_model)
    def get(self):
        """Get all performance histories"""
        performance_histories = PerformanceHistory.query.all()
        return performance_histories

    @data_ns.marshal_with(performance_history_model)
    def post(self):
        """Create a new performance history"""
        data = request.get_json()
        new_performance_history = PerformanceHistory(
            student_id=data.get('student_id'),
            sign_id=data.get('sign_id'),
            mastery_level=data.get('mastery_level')
        )
        new_performance_history.save()
        return new_performance_history, 201


@data_ns.route('/performance_histories/<int:id>')
class SinglePerformanceHistoryResource(Resource):

    @data_ns.marshal_with(performance_history_model)
    def get(self, id):
        """Get a performance history by ID"""
        performance_history = PerformanceHistory.query.get_or_404(id)
        return performance_history

    @data_ns.marshal_with(performance_history_model)
    def put(self, id):
        """Update a performance history by ID"""
        performance_history_to_update = PerformanceHistory.query.get_or_404(id)
        data = request.get_json()
        performance_history_to_update.update(
            data.get('mastery_level')
        )
        return performance_history_to_update

    @data_ns.marshal_with(performance_history_model)
    def delete(self, id):
        """Delete a performance history by ID"""
        performance_history_to_delete = PerformanceHistory.query.get_or_404(id)
        performance_history_to_delete.delete()
        return performance_history_to_delete





@data_ns.route('/masteries')
class StudentSignMasteryResource(Resource):

    @data_ns.marshal_with(student_sign_mastery_model)
    def get(self):
        """Get all student sign masteries"""
        masteries = StudentSignMastery.query.all()
        return masteries

    @data_ns.marshal_with(student_sign_mastery_model)
    def post(self):
        """Create a new student sign mastery"""
        data = request.get_json()
        new_mastery = StudentSignMastery(
            student_id=data.get('student_id'),
            sign_id=data.get('sign_id'),
            current_mastery_level=data.get('current_mastery_level')
        )
        new_mastery.save()
        return new_mastery, 201


@data_ns.route('/masteries/<int:student_id>/<int:sign_id>')
class SingleStudentSignMasteryResource(Resource):

    @data_ns.marshal_with(student_sign_mastery_model)
    def get(self, student_id, sign_id):
        """Get a student sign mastery by student_id and sign_id"""
        mastery = StudentSignMastery.query.filter_by(student_id=student_id, sign_id=sign_id).first_or_404()
        return mastery

    @data_ns.marshal_with(student_sign_mastery_model)
    def put(self, student_id, sign_id):
        """Update a student sign mastery by student_id and sign_id"""
        mastery_to_update = StudentSignMastery.query.filter_by(student_id=student_id, sign_id=sign_id).first_or_404()
        data = request.get_json()
        mastery_to_update.update(
            data.get('current_mastery_level')
        )
        return mastery_to_update

    @data_ns.marshal_with(student_sign_mastery_model)
    def delete(self, student_id, sign_id):
        """Delete a student sign mastery by student_id and sign_id"""
        mastery_to_delete = StudentSignMastery.query.filter_by(student_id=student_id, sign_id=sign_id).first_or_404()
        mastery_to_delete.delete()
        return mastery_to_delete


@data_ns.route('/masteries/<int:student_id>')
class StudentMasteryListResource(Resource):
    @data_ns.marshal_with(student_sign_mastery_model)
    def get(self, student_id):
        """Get mastery levels for a specific student"""
        masteries = StudentSignMastery.query.filter_by(student_id=student_id).all()
        return masteries
