import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'supersecretkey')

    DATABASE_PATH = os.environ.get('DATABASE_PATH', 'cafe.db')

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE_PATH}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False