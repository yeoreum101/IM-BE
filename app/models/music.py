from app import db
from app.models.base import BaseModel
from sqlalchemy import func

class Music(db.Model, BaseModel):
    __tablename__ = 'music_tb'
    
    id = db.Column(db.Integer, primary_key=True)
    music_url = db.Column(db.String(512), nullable=False)
    title = db.Column(db.String(255), nullable=False)

    # Relationships
    likes = db.relationship('Like', backref='music', lazy=True, cascade="all, delete-orphan")
    
    def __init__(self, music_url, title):
        self.music_url = music_url
        self.title = title
    
    def to_dict(self, include_like_count=False):
        """음악 객체를 딕셔너리로 변환"""
        result = {
            'id': self.id,
            'music_url': self.music_url,
            'title': self.title,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        
        if include_like_count:
            from app.models.like import Like
            result['like_count'] = Like.query.filter_by(music_id=self.id).count()
        
        return result
    
    @classmethod
    def find_by_id(cls, music_id):
        """ID로 음악 찾기"""
        return cls.query.filter_by(id=music_id).first()
    
    @classmethod
    def find_recent(cls, limit=10):
        """최근 음악 목록 조회"""
        return cls.query.order_by(cls.created_at.desc()).limit(limit).all()
    
    @classmethod
    def find_popular(cls, limit=10):
        """인기 음악 목록 조회 (좋아요 많은 순)"""
        from app.models.like import Like
        
        subquery = db.session.query(
            Like.music_id, 
            func.count(Like.id).label('like_count')
        ).group_by(Like.music_id).subquery()
        
        return db.session.query(cls).join(
            subquery, 
            cls.id == subquery.c.music_id
        ).order_by(
            subquery.c.like_count.desc()
        ).limit(limit).all()