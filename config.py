import os


class Config:
    # SQLAlchemy 配置
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask 配置
    DEBUG = True
    SECRET_KEY = 'your-secret-key-change-this'