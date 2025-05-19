from app import db
from datetime import datetime
from sqlalchemy import Column, DateTime

class BaseModel:
    """모든 모델의 기본 클래스"""
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def save(self):
        """객체를 저장하고 커밋"""
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        """객체를 삭제하고 커밋"""
        db.session.delete(self)
        db.session.commit()