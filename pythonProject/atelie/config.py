import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ваш_секретный_ключ'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.dirname(__file__), 'instance', 'atelier.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False