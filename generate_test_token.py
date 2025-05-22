from app import create_app
from app.auth.token_auth import generate_token
from app.models.member import Member

try:
    app = create_app()

    with app.app_context():
        # 기존 멤버 조회 (데이터베이스에 있는 멤버 사용)
        member = Member.query.first()
        if member:
            print(f"멤버 정보: ID={member.id}, 구글ID={member.google_id}, 이름={member.name}")
            token = generate_token(member)
            print(f"\n생성된 테스트 토큰:")
            print(f"{token}")
            print(f"\n사용법:")
            print(f'curl -H "Authorization: Bearer {token}" http://localhost:5000/api/myplaylist')
        else:
            print("데이터베이스에 멤버가 없습니다.")
            print("먼저 멤버를 생성해야 합니다.")
            
except Exception as e:
    print(f"오류 발생: {str(e)}")
    import traceback
    traceback.print_exc()