import requests
from flask import current_app
import logging
from app.utils.exceptions import AIServerException, ExternalAPIException

logger = logging.getLogger(__name__)

class AIClient:
    """AI 서버 API 클라이언트"""
    
    def __init__(self):
        self.base_url = current_app.config['AI_SERVER_URL']
        if not self.base_url:
            logger.warning("AI_SERVER_URL이 설정되지 않았습니다. 테스트 모드로 작동합니다.")
    
    def generate_music_with_text(self, prompt, prompt2=""):
        """텍스트 기반 음악 생성 API 호출
        
        Args:
            prompt: 텍스트 프롬프트
            
        Returns:
            음악 URL 및 메타데이터를 포함한 딕셔너리
            
        Raises:
            AIServerException: AI 서버 호출 중 오류 발생 시
        """
        # 테스트 모드 (AI 서버 URL이 없을 경우)
        if not self.base_url:
            # 가짜 URL 생성
            fake_url = f"https://example.com/fake_music_{prompt.replace(' ', '_')}.mp3"
            return {
                'music_url': fake_url,
                'title': prompt
            }
        
        try:
            url = f"{self.base_url}/generate_audio"
            headers = {'Content-Type': 'application/json'}
            payload = {
                'prompt1': prompt,
                'prompt2': prompt2
            }
            
            logger.info(f"AI 서버 호출: {url}, 프롬프트: {prompt}")
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code != 200:
                logger.error(f"AI 서버 오류: {response.status_code}, {response.text}")
                raise AIServerException(f"AI 서버 오류: {response.status_code}")
            
            response_data = response.json()
            music_url = response_data.get('response', {}).get('musicURL')
            
            if not music_url:
                logger.error(f"AI 서버 응답에 음악 URL이 없습니다: {response_data}")
                raise AIServerException("음악 생성에 실패했습니다.")
            
            return {
                'music_url': music_url,
                'title': prompt
            }
            
        except requests.RequestException as e:
            logger.error(f"AI 서버 요청 오류: {str(e)}")
            raise ExternalAPIException(f"AI 서버 연결 오류: {str(e)}")
    
    def generate_music_with_image(self, image_file):
        """이미지 기반 음악 생성 API 호출
        
        Args:
            image_file: 이미지 파일 객체
            
        Returns:
            음악 URL 및 메타데이터를 포함한 딕셔너리
            
        Raises:
            AIServerException: AI 서버 호출 중 오류 발생 시
        """
        # 테스트 모드 (AI 서버 URL이 없을 경우)
        if not self.base_url:
            # 가짜 URL 생성
            filename = image_file.filename if image_file.filename else 'image'
            fake_url = f"https://example.com/fake_image_music_{filename.replace(' ', '_')}.mp3"
            return {
                'music_url': fake_url,
                'title': f'이미지에서 생성된 음악 - {filename}'
            }
        
        try:
            url = f"{self.base_url}/generate_audio_from_image"
            files = {'file': (image_file.filename, image_file, image_file.content_type)}
            
            logger.info(f"AI 서버 호출: {url}, 이미지: {image_file.filename}")
            response = requests.post(url, files=files, timeout=30)
            
            if response.status_code != 200:
                logger.error(f"AI 서버 오류: {response.status_code}, {response.text}")
                raise AIServerException(f"AI 서버 오류: {response.status_code}")
            
            response_data = response.json()
            music_url = response_data.get('musicUrl')
            title = response_data.get('title')
            
            if not music_url or not title:
                logger.error(f"AI 서버 응답에 필요한 데이터가 없습니다: {response_data}")
                raise AIServerException("음악 생성에 실패했습니다.")
            
            return {
                'music_url': music_url,
                'title': title
            }
            
        except requests.RequestException as e:
            logger.error(f"AI 서버 요청 오류: {str(e)}")
            raise ExternalAPIException(f"AI 서버 연결 오류: {str(e)}")