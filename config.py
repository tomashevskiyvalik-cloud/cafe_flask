<<<<<<< HEAD
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'supersecretkey'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///cafe.db'
=======
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'supersecretkey'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///cafe.db'
>>>>>>> 09f9dca (add files)
    SQLALCHEMY_TRACK_MODIFICATIONS = False