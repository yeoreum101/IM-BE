from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()

# 데이터베이스 및 JWT 초기화
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_class=None):
    app = Flask(__name__)
    
    # 설정 로드
    if config_class is None:
        app.config.from_object('app.config.Config')
    else:
        app.config.from_object(config_class)
    
    # CORS 설정
    CORS(app, resources={
        r"/api/*": {
            "origins": app.config.get('CORS_ORIGINS', '*'),
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # 데이터베이스 초기화
    db.init_app(app)
    migrate.init_app(app, db)
    
    # JWT 초기화
    jwt.init_app(app)
    
    # JWT 에러 핸들러 설정
    from app.auth.jwt_callbacks import register_jwt_callbacks
    register_jwt_callbacks(jwt)
    
    # 블루프린트 등록
    from app.routes.member_routes import member_bp
    from app.routes.music_routes import music_bp
    
    app.register_blueprint(member_bp, url_prefix='/api')
    app.register_blueprint(music_bp, url_prefix='/api')
    
    # 헬스 체크 라우트 추가
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """헬스 체크 엔드포인트"""
        from flask import jsonify
        from datetime import datetime
        
        return jsonify({
            'success': True,
            'status': 200,
            'data': {
                'status': 'healthy',
                'message': '백엔드 서버가 정상적으로 실행 중입니다.',
                'timestamp': datetime.utcnow().isoformat()
            }
        }), 200
    
    # 에러 핸들러 등록
    from app.utils.error_handler import register_error_handlers
    register_error_handlers(app)
    
    return app