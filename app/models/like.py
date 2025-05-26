from app import db
from datetime import datetime

class Like(db.Model):
    __tablename__ = 'like_tb'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # 외래키
    member_id = db.Column(db.Integer, db.ForeignKey('member_tb.id', ondelete='CASCADE'), nullable=False)
    music_id = db.Column(db.Integer, db.ForeignKey('music_tb.id', ondelete='CASCADE'), nullable=False)
    
    # 유니크 제약조건 (한 사용자가 한 음악에 한 번만 좋아요 가능)
    __table_args__ = (
        db.UniqueConstraint('member_id', 'music_id', name='unique_member_music'),
    )
    
    def __init__(self, member_id, music_id):
        self.member_id = member_id
        self.music_id = music_id
    
    def to_dict(self):
        """좋아요 객체를 딕셔너리로 변환"""
        return {
            'id': self.id,
            'member_id': self.member_id,
            'music_id': self.music_id,
        }
    
    @classmethod
    def find_by_member_and_music(cls, member_id, music_id):
        """회원 ID와 음악 ID로 좋아요 찾기"""
        return cls.query.filter_by(member_id=member_id, music_id=music_id).first()
    
    @classmethod
    def count_by_music(cls, music_id):
        """음악 ID별 좋아요 수 계산 (캐싱 개선)"""
        try:
            return cls.query.filter_by(music_id=music_id).count()
        except Exception as e:
            logger.error(f"좋아요 수 조회 오류 (music_id: {music_id}): {e}")
            return 0  # 에러 시 0 반환