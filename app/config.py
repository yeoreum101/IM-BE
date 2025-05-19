import os
from datetime import timedelta

class Config:
    # 기본 설정
    SECRET_KEY = os.environ.get('JWT_SECRET', 'default-secret-key')
    
    # 데이터베이스 설정
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATASOURCE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT 설정
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET', 'default-jwt-secret')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_ALGORITHM = 'HS256'
    
    # CORS 설정
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    
    # Google OAuth2 설정
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
    GOOGLE_REDIRECT_URI = os.environ.get('GOOGLE_REDIRECT_URI')
    GOOGLE_GRANT_TYPE = os.environ.get('GOOGLE_GRANT_TYPE', 'authorization_code')
    
    # AI 서버 URL
    AI_SERVER_URL = os.environ.get('AI_SERVER_URL')
    
    # S3 설정
    S3_URL = os.environ.get('S3_URL')
    S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
    AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
    AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
    
    # 파일 업로드 설정
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
    
    # 로깅 설정
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_ECHO = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=3600)