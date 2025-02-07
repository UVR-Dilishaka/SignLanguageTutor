from flask import Flask,request,jsonify
from flask_restx import Api,Resource,fields
from config import Devconfig
from model import User,Sign,Activity,PerformanceHistory,StudentSignMastery
from ext import db
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager,create_access_token,create_refresh_token,jwt_required



app=Flask(__name__)
app.config.from_object(Devconfig)

db.init_app(app)
migrate = Migrate(app, db)
JWTManager(app)

api = Api(app,doc='/docs')

#setting up db model json templates


user_model = api.model(
    'User', {
        'id': fields.Integer(),
        'username': fields.String(required=True),
        'email': fields.String(required=True),
        'password': fields.String(required=True),
        'isteacher': fields.Boolean(required=True)
    }
)


sign_model = api.model(
    'Sign', {
        'id': fields.Integer(),
        'language': fields.String(required=True),
        'mono_code_characters': fields.String(required=True),
        'predictive_label': fields.String()
    }
)


activity_model = api.model(
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

performance_history_model = api.model(
    'PerformanceHistory', {
        'id': fields.Integer(),
        'student_id': fields.Integer(required=True),
        'sign_id': fields.Integer(required=True),
        'mastery_level': fields.Float(),
        'timestamp': fields.DateTime()
    }
)

student_sign_mastery_model = api.model(
    'StudentSignMastery', {
        'student_id': fields.Integer(required=True),
        'sign_id': fields.Integer(required=True),
        'current_mastery_level': fields.Float(),
        'last_updated': fields.DateTime()
    }
)



@api.route('/hello')
class HelloResource(Resource):
    
    @jwt_required()
    def get (self):
        return {"txt":"Hi am online and i am a projected route"}
    



#setting up routes for db crud operations

    
@api.route('/users')
class UserResource(Resource):

    @api.marshal_list_with(user_model)  
    def get(self):
        """Get all users"""
        users = User.query.all()
        return users

    @api.marshal_with(user_model)
    @api.expect(user_model)
    def post(self):
        """Create a new user"""
        data = request.get_json()
        new_user = User(
            username=data.get('username'),
            email=data.get('email'),
            password=data.get('password'),
            isteacher=data.get('isteacher')
        )
        new_user.save()
        return new_user, 201


@api.route('/user/<int:id>')
class SingleUserResource(Resource):

    @api.marshal_with(user_model)
    def get(self, id):
        """Get a user by ID"""
        user = User.query.get_or_404(id)
        return user

    @api.marshal_with(user_model)
    def put(self, id):
        """Update a user by ID"""
        user_to_update = User.query.get_or_404(id)
        data = request.get_json()
        user_to_update.update(data.get('username'), data.get('password'))
        return user_to_update

    @api.marshal_with(user_model)
    def delete(self, id):
        """Delete a user by ID"""
        user_to_delete = User.query.get_or_404(id)
        user_to_delete.delete()
        return user_to_delete




@api.route('/signs')
class SignResource(Resource):

    @api.marshal_with(sign_model)
    def get(self):
        """Get all signs"""
        signs = Sign.query.all()
        return signs

    @api.marshal_with(sign_model)
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


@api.route('/signs/<int:id>')
class SingleSignResource(Resource):

    @api.marshal_with(sign_model)
    def get(self, id):
        """Get a sign by ID"""
        sign = Sign.query.get_or_404(id)
        return sign

    @api.marshal_with(sign_model)
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

    @api.marshal_with(sign_model)
    def delete(self, id):
        """Delete a sign by ID"""
        sign_to_delete = Sign.query.get_or_404(id)
        sign_to_delete.delete()
        return sign_to_delete





@api.route('/activities')
class ActivityResource(Resource):

    @api.marshal_with(activity_model)
    def get(self):
        """Get all activities"""
        activities = Activity.query.all()
        return activities

    @api.marshal_with(activity_model)
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


@api.route('/activities/<int:id>')
class SingleActivityResource(Resource):

    @api.marshal_with(activity_model)
    def get(self, id):
        """Get an activity by ID"""
        activity = Activity.query.get_or_404(id)
        return activity

    @api.marshal_with(activity_model)
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

    @api.marshal_with(activity_model)
    def delete(self, id):
        """Delete an activity by ID"""
        activity_to_delete = Activity.query.get_or_404(id)
        activity_to_delete.delete()
        return activity_to_delete




@api.route('/performance_histories')
class PerformanceHistoryResource(Resource):

    @api.marshal_with(performance_history_model)
    def get(self):
        """Get all performance histories"""
        performance_histories = PerformanceHistory.query.all()
        return performance_histories

    @api.marshal_with(performance_history_model)
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


@api.route('/performance_histories/<int:id>')
class SinglePerformanceHistoryResource(Resource):

    @api.marshal_with(performance_history_model)
    def get(self, id):
        """Get a performance history by ID"""
        performance_history = PerformanceHistory.query.get_or_404(id)
        return performance_history

    @api.marshal_with(performance_history_model)
    def put(self, id):
        """Update a performance history by ID"""
        performance_history_to_update = PerformanceHistory.query.get_or_404(id)
        data = request.get_json()
        performance_history_to_update.update(
            data.get('mastery_level')
        )
        return performance_history_to_update

    @api.marshal_with(performance_history_model)
    def delete(self, id):
        """Delete a performance history by ID"""
        performance_history_to_delete = PerformanceHistory.query.get_or_404(id)
        performance_history_to_delete.delete()
        return performance_history_to_delete





@api.route('/masteries')
class StudentSignMasteryResource(Resource):

    @api.marshal_with(student_sign_mastery_model)
    def get(self):
        """Get all student sign masteries"""
        masteries = StudentSignMastery.query.all()
        return masteries

    @api.marshal_with(student_sign_mastery_model)
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


@api.route('/masteries/<int:student_id>/<int:sign_id>')
class SingleStudentSignMasteryResource(Resource):

    @api.marshal_with(student_sign_mastery_model)
    def get(self, student_id, sign_id):
        """Get a student sign mastery by student_id and sign_id"""
        mastery = StudentSignMastery.query.filter_by(student_id=student_id, sign_id=sign_id).first_or_404()
        return mastery

    @api.marshal_with(student_sign_mastery_model)
    def put(self, student_id, sign_id):
        """Update a student sign mastery by student_id and sign_id"""
        mastery_to_update = StudentSignMastery.query.filter_by(student_id=student_id, sign_id=sign_id).first_or_404()
        data = request.get_json()
        mastery_to_update.update(
            data.get('current_mastery_level')
        )
        return mastery_to_update

    @api.marshal_with(student_sign_mastery_model)
    def delete(self, student_id, sign_id):
        """Delete a student sign mastery by student_id and sign_id"""
        mastery_to_delete = StudentSignMastery.query.filter_by(student_id=student_id, sign_id=sign_id).first_or_404()
        mastery_to_delete.delete()
        return mastery_to_delete


if __name__ == '__main__':
    app.run()





@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Sign': Sign, 'Activity': Activity, 'PerformanceHistory': PerformanceHistory, 'StudentSignMastery': StudentSignMastery}



