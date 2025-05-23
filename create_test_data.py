from app import create_app, db
from app.models.music import Music
from app.models.member import Member
from app.models.mymusic import MyMusic

app = create_app()

with app.app_context():
    # 기존 데이터 확인
    print("기존 음악 데이터 개수:", Music.query.count())
    
    # 테스트용 음악 데이터 생성
    test_musics = [
        {
            'music_url': 'https://example.com/test_music_1.mp3',
            'title': '행복한 봄날의 선율'
        },
        {
            'music_url': 'https://example.com/test_music_2.mp3', 
            'title': '차분한 카페 음악'
        },
        {
            'music_url': 'https://example.com/test_music_3.mp3',
            'title': '에너지 넘치는 운동 음악'
        },
        {
            'music_url': 'https://example.com/test_music_4.mp3',
            'title': '감성적인 저녁 재즈'
        },
        {
            'music_url': 'https://example.com/test_music_5.mp3',
            'title': '집중을 위한 로파이 비트'
        }
    ]
    
    # 음악 데이터 추가
    for music_data in test_musics:
        # 중복 체크
        existing = Music.query.filter_by(title=music_data['title']).first()
        if not existing:
            music = Music(
                music_url=music_data['music_url'],
                title=music_data['title']
            )
            db.session.add(music)
            print(f"추가됨: {music_data['title']}")
        else:
            print(f"이미 존재함: {music_data['title']}")
    
    try:
        db.session.commit()
        print("테스트 음악 데이터 생성 완료!")
        print("총 음악 데이터 개수:", Music.query.count())
        
        # 생성된 음악 목록 출력
        print("\n=== 현재 음악 목록 ===")
        musics = Music.query.all()
        for music in musics:
            print(f"ID: {music.id}, 제목: {music.title}")
            
    except Exception as e:
        db.session.rollback()
        print(f"오류 발생: {str(e)}")