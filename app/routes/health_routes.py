# 백엔드에 추가할 헬스 체크 엔드포인트
# app/routes/health_routes.py (새 파일 생성)

from flask import Blueprint, jsonify
from app.utils.api_response import ApiResponse
import logging

health_bp = Blueprint('health', __name__)
logger = logging.getLogger(__name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    """헬스 체크 엔드포인트"""
    try:
        # 데이터베이스 연결 확인
        from app import db
        db.session.execute('SELECT 1').fetchone()
        
        return ApiResponse.success({
            'status': 'healthy',
            'message': '백엔드 서버가 정상적으로 실행 중입니다.',
            'database': 'connected',
            'timestamp': datetime.utcnow().isoformat()
        })
    except Exception as e:
        logger.error(f"헬스 체크 실패: {str(e)}")
        return ApiResponse.error(
            message="서버에 문제가 있습니다.",
            status_code=503
        )

@health_bp.route('/status', methods=['GET'])
def status_check():
    """상세 상태 확인"""
    try:
        from app import db
        from app.models.member import Member
        from app.models.music import Music
        
        # 데이터베이스 테이블 확인
        member_count = Member.query.count()
        music_count = Music.query.count()
        
        return ApiResponse.success({
            'status': 'operational',
            'database': {
                'connected': True,
                'members': member_count,
                'music': music_count
            },
            'services': {
                'auth': 'operational',
                'music_generation': 'operational'
            }
        })
    except Exception as e:
        logger.error(f"상태 체크 실패: {str(e)}")
        return ApiResponse.error(
            message="상태 확인 중 오류가 발생했습니다.",
            status_code=500
        )