import os

base_url = os.path.dirname(os.path.abspath(__name__))
class Config:
    DEBUG = True
    JWT_SECRET_KEY = 'X-ACCESS-LOGIN-FOUNDATIONS-PROJECT'
    JWT_ACCESS_TOKEN_EXPIRES = 3600
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = base_url
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_url, 'Database.db')
    SECRET_KEY = "7JNJHGHjhhjjFF"
    SECURITY_PASSWORD_SALT = "jdjkldkkklfk"
    SECURITY_PASSWORD_HASH = "sha512_crypt"