# IM Flask 백엔드

이 프로젝트는 AI를 활용한 음악 생성 플랫폼 "IM"의 백엔드 서버입니다.

## 프로젝트 개요

해당 프로젝트는 텍스트나 이미지를 입력하면 AI가 자동으로 음악을 생성해주는 서비스입니다. 이 백엔드 서버는 다음과 같은 기능을 제공합니다:

- 텍스트 기반 음악 생성
- 이미지 기반 음악 생성
- 음악 플레이리스트 관리
- 인기 플레이리스트 조회
- 음악 좋아요 기능
- 구글 OAuth2 인증

## 기술 스택

- Python 3.9+
- Flask - 웹 프레임워크
- SQLAlchemy - ORM
- Flask-JWT-Extended - 인증
- Flask-Migrate - 데이터베이스 마이그레이션
- Flask-CORS - CORS 지원
- Marshmallow - 데이터 검증 및 직렬화
- MySQL/SQLite - 데이터베이스
- AWS S3 - 파일 저장소
- Gunicorn - WSGI 서버

## 설치 및 실행

### 필요한 패키지 설치

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
