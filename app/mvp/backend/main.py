from flask import Flask
from flask_restx import Api
from model import User,Sign,Activity,PerformanceHistory,StudentSignMastery
from ext import db,socketio
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

import atexit
from config import Devconfig


from auth import auth_ns
from data import data_ns
from TamilSignClassification import Tamil_predict_ns
from AdoptiveTutoringSystem import adoptiveTutoring_ns
from PoseEstimation import poseEstimation_ns



print(type(poseEstimation_ns))

def shutdown_logic():
    print("Flask app is shutting down...")




def create_app(config):
    

    app=Flask(__name__)
    atexit.register(shutdown_logic)
    app.config.from_object(config)
    db.init_app(app)
    migrate = Migrate(app, db)
    JWTManager(app)
    api = Api(app,doc='/docs')
    
    CORS(app)
    api.add_namespace(auth_ns)
    api.add_namespace(data_ns) 
    api.add_namespace(Tamil_predict_ns) 
    api.add_namespace(poseEstimation_ns)
    api.add_namespace(adoptiveTutoring_ns)  
    
    
    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'User': User, 'Sign': Sign, 'Activity': Activity, 'PerformanceHistory': PerformanceHistory, 'StudentSignMastery': StudentSignMastery}

    return app


app = create_app(Devconfig)
socketio.init_app(app)

@socketio.on("connect")
def test_connect():
    print("Client connected")
    socketio.emit("server_message", {"message": "Connected to server"})


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000)
