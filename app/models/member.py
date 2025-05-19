from app import db
from app.models.base import BaseModel

class Member(db.Model, BaseModel):
    __tablename__ = 'member_tb'
    
    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=True)
    profile_image = db.Column(db.String(512), nullable=True)
    
    # Relationships
    mymusics = db.relationship('MyMusic', backref='member', lazy=True, cascade="all, delete-orphan")
    likes = db.relationship('Like', backref='member', lazy=True, cascade="all, delete-orphan")
    
    def __init__(self, google_id, name, email=None, profile_image=None):
        self.google_id = google_id
        self.name = name
        self.email = email
        self.profile_image = profile_image
    
    def to_dict(self):
        """멤버 객체를 딕셔너리로 변환"""
        return {
            'id': self.id,
            'google_id': self.google_id,
            'name': self.name,
            'email': self.email,
            'profile_image': self.profile_image,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @classmethod
    def find_by_id(cls, member_id):
        """ID로 멤버 찾기"""
        return cls.query.filter_by(id=member_id).first()
    
    @classmethod
    def find_by_google_id(cls, google_id):
        """구글 ID로 멤버 찾기"""
        return cls.query.filter_by(google_id=google_id).first()
    
    @classmethod
    def find_by_email(cls, email):
        """이메일로 멤버 찾기"""
        return cls.query.filter_by(email=email).first()