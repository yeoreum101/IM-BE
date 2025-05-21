from app.clients.oauth_client import OAuthClient
from app.services.member_service import MemberService
from app.utils.exceptions import ExternalAPIException, UnauthorizedException
import logging

logger = logging.getLogger(__name__)

class OAuthService:
    """OAuth 인증 서비스"""
    
    @staticmethod
    def get_google_access_token(code):
        """구글 액세스 토큰 획득
        
        Args:
            code: 인증 코드
            
        Returns:
            액세스 토큰
            
        Raises:
            ExternalAPIException: 토큰 획득 중 오류 발생 시
        """
        try:
            token_response = OAuthClient.get_google_token(code)
            access_token = token_response.get('access_token')
            
            if not access_token:
                logger.error("Google OAuth 응답에 액세스 토큰이 없습니다.")
                raise UnauthorizedException("인증에 실패했습니다.")
            
            return access_token
        except ExternalAPIException as e:
            logger.error(f"Google 액세스 토큰 획득 실패: {str(e)}")
            raise
    
    @staticmethod
    def get_google_user_info(access_token):
        """구글 사용자 정보 획득
        
        Args:
            access_token: 액세스 토큰
            
        Returns:
            사용자 정보
            
        Raises:
            ExternalAPIException: 사용자 정보 획득 중 오류 발생 시
        """
        try:
            user_info = OAuthClient.get_google_user_info(access_token)
            
            if not user_info or not user_info.get('id'):
                logger.error("Google 사용자 정보 응답에 ID가 없습니다.")
                raise UnauthorizedException("사용자 정보를 가져올 수 없습니다.")
            
            filtered_info = {
                'id': user_info.get('id'),
                'name': user_info.get('name')
            }
            
            return user_info
        except ExternalAPIException as e:
            logger.error(f"Google 사용자 정보 획득 실패: {str(e)}")
            raise
    
    @staticmethod
    def process_google_login(code):
        """구글 로그인 처리
        
        Args:
            code: 인증 코드
            
        Returns:
            JWT 토큰이 포함된 응답
            
        Raises:
            UnauthorizedException: 인증 실패 시
        """
        try:
            # 액세스 토큰 획득
            access_token = OAuthService.get_google_access_token(code)
            
            # 사용자 정보 획득
            user_info = OAuthService.get_google_user_info(access_token)
            
            # 회원 찾기 또는 생성 및 JWT 토큰 생성
            jwt_token = MemberService.find_or_create_member_by_google_id(user_info)
            
            return {
                'accessToken': jwt_token
            }
        except Exception as e:
            logger.error(f"Google 로그인 처리 실패: {str(e)}")
            if isinstance(e, (UnauthorizedException, ExternalAPIException)):
                raise
            raise UnauthorizedException("로그인 처리 중 오류가 발생했습니다.")