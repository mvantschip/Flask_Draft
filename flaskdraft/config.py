import os

class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/draft"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.urandom(32)
