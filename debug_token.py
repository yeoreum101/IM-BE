# debug_token.py
import jwt
from app import create_app

try:
    app = create_app()
    
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NzkwMDc1MiwianRpIjoiNmZjNjIyMDYtZjU3Zi00MGQyLWIwZDYtMWUwNTAzODliZjBiIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjEiLCJuYmYiOjE3NDc5MDA3NTIsImV4cCI6MTc0Nzk4NzE1MiwiZ29vZ2xlX2lkIjoidGVzdF9nb29nbGVfaWQiLCJuYW1lIjoiVGVzdCBVc2VyIn0.i6dVRe2-HUZJ98e_vllVN0FZssDXLruzIfoqjoS8t-c"
    
    with app.app_context():
        # JWT 비밀키 확인
        secret_key = app.config.get('JWT_SECRET_KEY')
        print(f"JWT 비밀키: {secret_key}")
        
        # 토큰 디코딩 (검증 없이)
        decoded = jwt.decode(token, options={"verify_signature": False})
        print(f"토큰 내용: {decoded}")
        
        # 토큰 만료 시간 확인
        import time
        current_time = time.time()
        exp_time = decoded.get('exp')
        print(f"현재 시간: {current_time}")
        print(f"만료 시간: {exp_time}")
        print(f"만료까지 남은 시간: {exp_time - current_time}초")
        
        # 토큰 검증
        try:
            verified = jwt.decode(token, secret_key, algorithms=['HS256'])
            print("토큰 검증 성공!")
            print(f"검증된 내용: {verified}")
        except Exception as e:
            print(f"토큰 검증 실패: {e}")
            
except Exception as e:
    print(f"오류: {e}")
    import traceback
    traceback.print_exc()