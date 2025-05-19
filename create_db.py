from app import create_app, db
from app.models.member import Member
from app.models.music import Music
from app.models.mymusic import MyMusic
from app.models.like import Like

app = create_app()

with app.app_context():
    db.create_all()
    print("데이터베이스 테이블이 생성되었습니다.")