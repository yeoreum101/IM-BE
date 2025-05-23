from flask import Blueprint, request
from app.services.oauth_service import OAuthService
from app.services.member_service import MemberService
from app.utils.api_response import ApiResponse
from app.schemas.member_schemas import OAuthTokenRequestSchema, TokenResponseSchema, MemberResponseSchema
from app.utils.exceptions import ValidationException, UnauthorizedException, MemberNotFoundException
from app.auth.token_auth import auth_required
import logging

member_bp = Blueprint('member', __name__)
logger = logging.getLogger(__name__)

@member_bp.route('/auth/google/callback', methods=['GET', 'POST'])
def oauth_login():
    """구글 OAuth 로그인 콜백
    
    GET: 기존 방식 (인증 코드 사용)
    POST: 프론트엔드에서 사용자 정보 직접 전송
    
    Returns:
        JWT 토큰 정보
    """
    try:
        if request.method == 'GET':
            # 기존 방식: 인증 코드 사용
            schema = OAuthTokenRequestSchema()
            errors = schema.validate(request.args)
            if errors:
                raise ValidationException("유효하지 않은 요청입니다.", errors=errors)
            
            code = request.args.get('code')
            logger.info(f"Google OAuth 로그인 요청: 코드 길이 {len(code)}")
            
            # 로그인 처리
            response = OAuthService.process_google_login(code)
            
        elif request.method == 'POST':
            # 새로운 방식: 프론트엔드에서 사용자 정보 직접 전송
            data = request.get_json()
            user_info = data.get('user_info')
            
            if not user_info:
                raise ValidationException("사용자 정보가 필요합니다.")
            
            logger.info(f"프론트엔드에서 사용자 정보 전송: {user_info.get('email')}")
            
            # 사용자 정보 직접 처리
            response = OAuthService.process_google_login_direct(user_info)
        
        # 응답 스키마 적용
        result = TokenResponseSchema().dump(response)
        return ApiResponse.success(result)
    
    except ValidationException as e:
        logger.warning(f"OAuth 로그인 검증 실패: {e.message}")
        return ApiResponse.error(e.message, e.status_code, e.error_code, e.errors)
    
    except UnauthorizedException as e:
        logger.warning(f"OAuth 로그인 인증 실패: {e.message}")
        return ApiResponse.error(e.message, e.status_code, e.error_code)
    
    except Exception as e:
        logger.error(f"OAuth 로그인 오류: {str(e)}")
        return ApiResponse.error("로그인 처리 중 오류가 발생했습니다.", 500)

@member_bp.route('/me', methods=['GET'])
@auth_required
def get_member_profile(user_info):
    """현재 로그인한 회원 정보 조회
    
    Returns:
        회원 프로필 정보
    """
    try:
        logger.info(f"회원 프로필 조회: {user_info.get('id')}")
        
        # ID로 회원 조회
        member_id = user_info.get('id')
        member_data = MemberService.get_member_profile(member_id)
        
        # 응답 스키마 적용
        result = MemberResponseSchema().dump(member_data)
        return ApiResponse.success(result)
    
    except MemberNotFoundException as e:
        logger.warning(f"회원 프로필 조회 실패: {e.message}")
        return ApiResponse.error(e.message, e.status_code, e.error_code)
    
    except Exception as e:
        logger.error(f"회원 프로필 조회 오류: {str(e)}")
        return ApiResponse.error("회원 정보 조회 중 오류가 발생했습니다.", 500)