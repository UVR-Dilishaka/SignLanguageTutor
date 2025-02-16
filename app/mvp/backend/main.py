from flask import Flask
from flask_restx import Api
from model import User,Sign,Activity,PerformanceHistory,StudentSignMastery
from ext import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from auth import auth_ns
from data import data_ns



def create_app(config):
    app=Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    migrate = Migrate(app, db)
    JWTManager(app)
    api = Api(app,doc='/docs')
    CORS(app)

    api.add_namespace(auth_ns)
    api.add_namespace(data_ns) 

     

    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'User': User, 'Sign': Sign, 'Activity': Activity, 'PerformanceHistory': PerformanceHistory, 'StudentSignMastery': StudentSignMastery}

    return app




