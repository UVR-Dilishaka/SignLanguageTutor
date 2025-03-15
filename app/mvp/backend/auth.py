from flask_restx import Namespace, Resource,fields
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from model import User
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required


auth_ns = Namespace('auth', description='Authentication operations')

signup_model = auth_ns.model(
    'Signup', {
        'username': fields.String(required=True),
        'email': fields.String(required=True),
        'password': fields.String(required=True),
        'isteacher': fields.Boolean(required=True)
    }
)


login_model = auth_ns.model(
    'Login', {
        'username': fields.String(required=True),
        'password': fields.String(required=True)
    }
)


#jwt authentication
@auth_ns.route('/signup')
class Signup(Resource):

    
    @auth_ns.expect(signup_model)
    def post(self):
        data = request.get_json()

        username = data.get('username')
        db_user = User.query.filter_by(username=username).first()

        if db_user is not None:
            return 400

        new_user = User(
            username=data.get('username'),
            email=data.get('email'),
            password=generate_password_hash(data.get('password')),
            isteacher= bool(data.get('isteacher'))
        )

        new_user.save()
        return 201





@auth_ns.route('/login')
class Login(Resource):

    @auth_ns.expect(login_model)
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        
        db_user = User.query.filter_by(username=username).first()

        if db_user is None:
            return jsonify({"message":f"User with username {username} does not exist"})
        
        if check_password_hash(db_user.password, password):
            access_token = create_access_token(identity=db_user.username)
            refresh_token = create_refresh_token(identity=db_user.username)
            return jsonify({"access_token":access_token,"refresh_token":refresh_token})


@auth_ns.route('/refresh')
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return jsonify({"access_token":access_token})
    
