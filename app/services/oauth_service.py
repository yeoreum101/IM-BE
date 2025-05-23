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
        """구글 로그인 처리 (기존 방식)
        
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
    
    @staticmethod
    def process_google_login_direct(user_info):
        """구글 로그인 처리 (프론트엔드에서 사용자 정보 직접 전송)
        
        Args:
            user_info: 구글 사용자 정보
            
        Returns:
            JWT 토큰이 포함된 응답
            
        Raises:
            UnauthorizedException: 인증 실패 시
        """
        try:
            # 사용자 정보 검증
            if not user_info or not user_info.get('id'):
                logger.error("전달받은 사용자 정보에 ID가 없습니다.")
                raise UnauthorizedException("유효하지 않은 사용자 정보입니다.")
            
            # member_tb 구조에 맞는 정보만 추출
            # member_tb: id, google_id, name, created_at, updated_at
            processed_user_info = {
                'id': user_info.get('id'),  # google_id로 사용됨
                'name': user_info.get('name', '사용자')  # name 필드
            }
            
            logger.info(f"프론트엔드에서 받은 사용자 정보 처리: ID={processed_user_info['id']}, Name={processed_user_info['name']}")
            
            # 회원 찾기 또는 생성 및 JWT 토큰 생성
            jwt_token = MemberService.find_or_create_member_by_google_id(processed_user_info)
            
            return {
                'accessToken': jwt_token
            }
        except Exception as e:
            logger.error(f"프론트엔드 구글 로그인 처리 실패: {str(e)}")
            if isinstance(e, UnauthorizedException):
                raise
            raise UnauthorizedException("로그인 처리 중 오류가 발생했습니다.")