import logging
from flask import jsonify

logger = logging.getLogger(__name__)

def register_jwt_callbacks(jwt):
    """JWT 콜백 함수 등록
    
    Args:
        jwt: JWTManager 인스턴스
    """
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        """만료된 토큰 처리"""
        logger.warning(f"만료된 토큰 사용 시도: {jwt_payload}")
        return jsonify({
            'success': False,
            'status': 401,
            'message': '만료된 토큰입니다. 다시 로그인해주세요.',
            'error_code': 'TOKEN_EXPIRED'
        }), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        """유효하지 않은 토큰 처리"""
        logger.warning(f"유효하지 않은 토큰 사용 시도: {error}")
        return jsonify({
            'success': False,
            'status': 401,
            'message': '유효하지 않은 토큰입니다.',
            'error_code': 'INVALID_TOKEN'
        }), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        """토큰 없음 처리"""
        logger.warning(f"토큰 없음: {error}")
        return jsonify({
            'success': False,
            'status': 401,
            'message': '인증 토큰이 필요합니다.',
            'error_code': 'MISSING_TOKEN'
        }), 401
    
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        """새로운 토큰 필요 처리"""
        logger.warning(f"새로운 토큰 필요: {jwt_payload}")
        return jsonify({
            'success': False,
            'status': 401,
            'message': '새로운 인증이 필요합니다. 다시 로그인해주세요.',
            'error_code': 'FRESH_TOKEN_REQUIRED'
        }), 401
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        """취소된 토큰 처리"""
        logger.warning(f"취소된 토큰 사용 시도: {jwt_payload}")
        return jsonify({
            'success': False,
            'status': 401,
            'message': '이미 로그아웃된 토큰입니다.',
            'error_code': 'TOKEN_REVOKED'
        }), 401