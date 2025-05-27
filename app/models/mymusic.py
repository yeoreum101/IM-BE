from app import db
from app.models.base import BaseModel

class MyMusic(db.Model, BaseModel):
    __tablename__ = 'mymusic_tb'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # 외래키 - Music 테이블 참조
    music_id = db.Column(db.Integer, db.ForeignKey('music_tb.id', ondelete='CASCADE'), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('member_tb.id', ondelete='CASCADE'), nullable=False)
    
    # Music 테이블과의 관계 설정
    music = db.relationship('Music', backref='my_musics', lazy=True)
    
    def __init__(self, music_id, member_id):
        self.music_id = music_id
        self.member_id = member_id
    
    def to_dict(self):
        """내 음악 객체를 딕셔너리로 변환"""
        return {
            'id': self.id,
            'music_id': self.music_id,
            'music_url': self.music.music_url if self.music else None,
            'title': self.music.title if self.music else None,
            'member_id': self.member_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @classmethod
    def find_by_member_id(cls, member_id, limit=10):
        """회원 ID로 내 음악 목록 조회 (Music과 조인)"""
        return cls.query.join(cls.music).filter(cls.member_id == member_id)\
                      .order_by(cls.created_at.desc()).limit(limit).all()
    
    @classmethod
    def find_by_id_and_member_id(cls, id, member_id):
        """내 음악 ID와 회원 ID로 내 음악 찾기"""
        return cls.query.filter_by(id=id, member_id=member_id).first()
    
    @classmethod
    def find_by_music_id_and_member_id(cls, music_id, member_id):
        """음악 ID와 회원 ID로 내 음악 찾기"""
        return cls.query.filter_by(music_id=music_id, member_id=member_id).first()
    
    @classmethod
    def delete_by_music_id(cls, music_id):
        """특정 음악 ID의 모든 MyMusic 레코드 삭제"""
        cls.query.filter_by(music_id=music_id).delete()
        db.session.commit()