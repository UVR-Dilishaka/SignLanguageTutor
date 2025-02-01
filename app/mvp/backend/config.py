
from decouple import config
import os 

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class Config:
    SEAcret_KEY = config("KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = config('SQLALCHEMY_TRACK_MODIFICATIONS',cast = bool)

class Devconfig(Config):
    SQLALCHEMY_DATABASE_URI ="sqlite:///"+os.path.join(BASE_DIR,'dev.db')
    DEBUG=True
    SQLALCHEMY_ECHO=True


class Prodconfig(Config):
    pass

class Testconfig():
    pass