from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from functools import wraps
from flask import jsonify, request, current_app
import datetime
from app.utils.exceptions import UnauthorizedException, ForbiddenException
import logging

logger = logging.getLogger(__name__)

def generate_token(member):
    """JWT 토큰 생성
    
    Args:
        member: 회원 모델 객체
        
    Returns:
        생성된 액세스 토큰
    """
    identity = {
        'id': member.id,
        'google_id': member.google_id,
        'name': member.name
    }
    expires = datetime.timedelta(hours=24)
    access_token = create_access_token(identity=identity, expires_delta=expires)
    logger.info(f"토큰 생성 완료: 사용자 ID {member.id}")
    return access_token

def get_current_user():
    """현재 인증된 사용자 정보 반환
    
    Returns:
        사용자 정보 딕셔너리
        
    Raises:
        UnauthorizedException: 토큰이 유효하지 않은 경우
    """
    try:
        jwt_required()
        current_user = get_jwt_identity()
        return current_user
    except Exception as e:
        logger.error(f"토큰 검증 실패: {str(e)}")
        raise UnauthorizedException()

def auth_required(f):
    """인증 필수 데코레이터
    
    Args:
        f: 인증이 필요한 함수
        
    Returns:
        인증 검사를 수행하는 래퍼 함수
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            jwt_required()
            current_user = get_jwt_identity()
            return f(current_user, *args, **kwargs)
        except Exception as e:
            logger.error(f"인증 실패: {str(e)}")
            raise UnauthorizedException()
    return decorated

def optional_auth(f):
    """선택적 인증 데코레이터 (인증 정보가 있으면 사용, 없으면 None)
    
    Args:
        f: 선택적 인증을 지원하는 함수
        
    Returns:
        선택적 인증 검사를 수행하는 래퍼 함수
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                from flask_jwt_extended import verify_jwt_in_request
                try:
                    verify_jwt_in_request(optional=True)
                    current_user = get_jwt_identity()
                    return f(current_user, *args, **kwargs)
                except Exception as e:
                    logger.warning(f"토큰 검증 실패 (선택적 인증): {str(e)}")
                    # 인증 실패해도 계속 진행, 인증 정보 없이 함수 호출
            
            # 인증되지 않은 경우 None 전달
            return f(None, *args, **kwargs)
        except Exception as e:
            logger.error(f"선택적 인증 처리 중 오류: {str(e)}")
            return f(None, *args, **kwargs)
    
    return decorated