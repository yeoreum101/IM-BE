from app import db
from app.models.base import BaseModel

class MyMusic(db.Model, BaseModel):
    __tablename__ = 'mymusic_tb'
    
    id = db.Column(db.Integer, primary_key=True)
    music_url = db.Column(db.String(512), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    
    # 외래키
    member_id = db.Column(db.Integer, db.ForeignKey('member_tb.id', ondelete='CASCADE'), nullable=False)
    
    def __init__(self, music_url, title, member_id):
        self.music_url = music_url
        self.title = title
        self.member_id = member_id
    
    def to_dict(self):
        """내 음악 객체를 딕셔너리로 변환"""
        return {
            'id': self.id,
            'music_url': self.music_url,
            'title': self.title,
            'member_id': self.member_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @classmethod
    def find_by_member_id(cls, member_id, limit=10):
        """회원 ID로 내 음악 목록 조회"""
        return cls.query.filter_by(member_id=member_id).order_by(cls.created_at.desc()).limit(limit).all()
    
    @classmethod
    def find_by_id_and_member_id(cls, mymusic_id, member_id):
        """내 음악 ID와 회원 ID로 내 음악 찾기"""
        return cls.query.filter_by(id=mymusic_id, member_id=member_id).first()
    
    @classmethod
    def find_by_music_id_and_member_id(cls, music_id, member_id):
        """음악 ID와 회원 ID로 내 음악 찾기 (새로 추가)"""
        # music_url 기반으로 찾거나, 별도의 music_id 컬럼이 필요할 수 있음
        # 현재 구조에서는 id를 사용
        return cls.query.filter_by(id=music_id, member_id=member_id).first()