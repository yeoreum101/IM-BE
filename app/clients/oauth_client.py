import requests
from flask import current_app
import logging
from app.utils.exceptions import ExternalAPIException

logger = logging.getLogger(__name__)

class OAuthClient:
    """OAuth API 클라이언트"""
    
    @staticmethod
    def get_google_token(code):
        """구글 액세스 토큰 획득
        
        Args:
            code: 인증 코드
            
        Returns:
            액세스 토큰 정보
            
        Raises:
            ExternalAPIException: 토큰 획득 중 오류 발생 시
        """
        try:
            url = "https://oauth2.googleapis.com/token"
            data = {
                'code': code,
                'client_id': current_app.config['GOOGLE_CLIENT_ID'],
                'client_secret': current_app.config['GOOGLE_CLIENT_SECRET'],
                'redirect_uri': current_app.config['GOOGLE_REDIRECT_URI'],
                'grant_type': current_app.config['GOOGLE_GRANT_TYPE']
            }
            
            logger.info(f"Google 토큰 요청: {url}")
            response = requests.post(url, data=data, timeout=10)
            
            if response.status_code != 200:
                logger.error(f"Google OAuth 토큰 획득 실패: {response.status_code}, {response.text}")
                raise ExternalAPIException(f"Google OAuth 토큰 획득 실패: {response.status_code}")
            
            return response.json()
            
        except requests.RequestException as e:
            logger.error(f"Google OAuth 요청 오류: {str(e)}")
            raise ExternalAPIException(f"Google 서버 연결 오류: {str(e)}")
    
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
            url = f"https://www.googleapis.com/oauth2/v2/userinfo"
            headers = {'Authorization': f'Bearer {access_token}'}
            
            logger.info(f"Google 사용자 정보 요청: {url}")
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code != 200:
                logger.error(f"Google 사용자 정보 획득 실패: {response.status_code}, {response.text}")
                raise ExternalAPIException(f"Google 사용자 정보 획득 실패: {response.status_code}")
            
            return response.json()
            
        except requests.RequestException as e:
            logger.error(f"Google API 요청 오류: {str(e)}")
            raise ExternalAPIException(f"Google 서버 연결 오류: {str(e)}")