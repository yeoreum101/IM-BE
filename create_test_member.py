from app import create_app, db
from app.models.member import Member
from app.auth.token_auth import generate_token

app = create_app()

with app.app_context():
    # 테스트용 회원 생성
    test_google_id = "test_user_123456789"
    test_name = "테스트 사용자"
    
    # 기존 회원 확인
    existing_member = Member.find_by_google_id(test_google_id)
    
    if not existing_member:
        # 새 회원 생성
        test_member = Member(
            google_id=test_google_id,
            name=test_name
        )
        db.session.add(test_member)
        db.session.commit()
        print(f"테스트 회원 생성 완료: {test_name} (ID: {test_member.id})")
        
        # JWT 토큰 생성
        token = generate_token(test_member)
        print(f"JWT 토큰: {token}")
        print("\n이 토큰을 사용해서 API 테스트를 진행하세요!")
        
    else:
        print(f"이미 존재하는 회원: {existing_member.name} (ID: {existing_member.id})")
        # 기존 회원으로 토큰 생성
        token = generate_token(existing_member)
        print(f"JWT 토큰: {token}")