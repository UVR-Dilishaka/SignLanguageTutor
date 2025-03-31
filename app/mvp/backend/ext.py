from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
import pickle

db = SQLAlchemy()
socketio = SocketIO(cors_allowed_origins="*")



with open('./Model/RF.pkl', 'rb') as file:
    TLmodel = pickle.load(file)

with open('./Model/RFSL.pkl', 'rb') as file:
    SLmodel = pickle.load(file)

    