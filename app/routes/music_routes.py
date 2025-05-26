from flask import Blueprint, request
from app.services.music_service import MusicService
from app.utils.api_response import ApiResponse
from app.auth.token_auth import auth_required, optional_auth
from app.schemas.music_schemas import (
    MusicGenWithTextRequestSchema, MusicGenWithTextResponseSchema,
    MusicResponseSchema, PlaylistResponseSchema, MyPlaylistResponseSchema
)
from app.utils.exceptions import (
    ValidationException, AIServerException, MemberNotFoundException,
    MusicNotFoundException, DuplicateDataException
)
import logging

music_bp = Blueprint('music', __name__)
logger = logging.getLogger(__name__)

@music_bp.route('/generate-music', methods=['POST'])
@optional_auth
def generate_music(user_info):
    """텍스트 기반 음악 생성
    
    Returns:
        생성된 음악 정보
    """
    try:
        # 입력 유효성 검사
        schema = MusicGenWithTextRequestSchema()
        errors = schema.validate(request.json)
        if errors:
            raise ValidationException("입력 형식이 잘못되었습니다.", errors=errors)
        
        data = request.json
        prompt1 = data.get('prompt1')
        prompt2 = data.get('prompt2', "")
        logger.info(f"텍스트 기반 음악 생성 요청: '{prompt1}'")
        
        # 서비스 호출
        response = MusicService.generate_music_with_text(prompt1, prompt2, user_info)
        
        # 응답 스키마 적용
        result = MusicGenWithTextResponseSchema().dump(response)
        return ApiResponse.success(result)
    
    except ValidationException as e:
        logger.warning(f"음악 생성 검증 실패: {e.message}")
        return ApiResponse.error(e.message, e.status_code, e.error_code, e.errors)
    
    except AIServerException as e:
        logger.error(f"AI 서버 오류: {e.message}")
        return ApiResponse.error(e.message, e.status_code, e.error_code)
    
    except MemberNotFoundException as e:
        logger.warning(f"회원 찾기 실패: {e.message}")
        return ApiResponse.error(e.message, e.status_code, e.error_code)
    
    except Exception as e:
        logger.error(f"음악 생성 오류: {str(e)}")
        return ApiResponse.error("음악 생성 중 오류가 발생했습니다.", 500)

@music_bp.route('/generate-music/image', methods=['POST'])
@optional_auth
def generate_music_with_image(user_info):
    """이미지 기반 음악 생성
    
    Returns:
        생성된 음악 정보
    """
    try:
        if 'image' not in request.files:
            raise ValidationException("이미지가 제공되지 않았습니다.")
        
        image_file = request.files['image']
        
        if image_file.filename == '':
            raise ValidationException("이미지가 선택되지 않았습니다.")
            
        # 파일 확장자 검사
        allowed_extensions = {'jpg', 'jpeg', 'png', 'gif'}
        if '.' not in image_file.filename or image_file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            raise ValidationException("지원하지 않는 이미지 형식입니다.")
        
        logger.info(f"이미지 기반 음악 생성 요청: {image_file.filename}")
        
        # 서비스 호출
        response = MusicService.generate_music_with_image(image_file, user_info)
        
        return ApiResponse.success(response)
    
    except ValidationException as e:
        logger.warning(f"이미지 음악 생성 검증 실패: {e.message}")
        return ApiResponse.error(e.message, e.status_code, e.error_code)
    
    except AIServerException as e:
        logger.error(f"AI 서버 오류: {e.message}")
        return ApiResponse.error(e.message, e.status_code, e.error_code)
    
    except MemberNotFoundException as e:
        logger.warning(f"회원 찾기 실패: {e.message}")
        return ApiResponse.error(e.message, e.status_code, e.error_code)
    
    except Exception as e:
        logger.error(f"이미지 음악 생성 오류: {str(e)}")
        return ApiResponse.error("음악 생성 중 오류가 발생했습니다.", 500)

@music_bp.route('/myplaylist', methods=['GET'])
@auth_required
def get_my_playlist(user_info):
    """내 플레이리스트 조회
    
    Returns:
        내 플레이리스트 정보
    """
    try:
        logger.info(f"내 플레이리스트 조회: 사용자 ID {user_info.get('id')}")
        
        # 서비스 호출
        response = MusicService.get_my_playlist(user_info)
        
        # 스키마 없이 직접 반환
        return ApiResponse.success(response)
    
    except MemberNotFoundException as e:
        logger.warning(f"회원 찾기 실패: {e.message}")
        return ApiResponse.error(e.message, e.status_code, e.error_code)
    
    except Exception as e:
        logger.error(f"내 플레이리스트 조회 오류: {str(e)}")
        return ApiResponse.error("플레이리스트 조회 중 오류가 발생했습니다.", 500)

@music_bp.route('/music/<int:music_id>', methods=['DELETE'])
@auth_required
def delete_music(user_info, music_id):
    """음악 삭제 (내 플레이리스트에서만)
    
    Args:
        music_id: 음악 ID
        
    Returns:
        성공 메시지
    """
    try:
        logger.info(f"음악 삭제 요청: 사용자 ID {user_info.get('id')}, 음악 ID {music_id}")
        
        # 서비스 호출
        MusicService.delete_my_music(music_id, user_info)
        
        return ApiResponse.success(message="음악이 삭제되었습니다.")
    
    except MemberNotFoundException as e:
        logger.warning(f"회원 찾기 실패: {e.message}")
        return ApiResponse.error(e.message, e.status_code, e.error_code)
    
    except MusicNotFoundException as e:
        logger.warning(f"음악 찾기 실패: {e.message}")
        return ApiResponse.error(e.message, e.status_code, e.error_code)
    
    except ForbiddenException as e:
        logger.warning(f"권한 없음: {e.message}")
        return ApiResponse.error(e.message, e.status_code, e.error_code)
    
    except Exception as e:
        logger.error(f"음악 삭제 오류: {str(e)}")
        return ApiResponse.error("음악 삭제 중 오류가 발생했습니다.", 500)

@music_bp.route('/playlist', methods=['GET'])
@optional_auth
def get_playlist(user_info):
    """전체 플레이리스트 조회
    
    Returns:
        전체 플레이리스트 정보
    """
    try:
        logger.info("전체 플레이리스트 조회")
        
        # 서비스 호출
        response = MusicService.get_playlist(user_info)
        
        # 스키마 없이 직접 반환 (모든 필드 포함)
        return ApiResponse.success(response)
    
    except Exception as e:
        logger.error(f"플레이리스트 조회 오류: {str(e)}")
        return ApiResponse.error("플레이리스트 조회 중 오류가 발생했습니다.", 500)

@music_bp.route('/popular-playlist', methods=['GET'])
@optional_auth
def get_popular_playlist(user_info):
    """인기 플레이리스트 조회
    
    Returns:
        인기 플레이리스트 정보
    """
    try:
        logger.info("인기 플레이리스트 조회")
        
        # 서비스 호출
        response = MusicService.get_popular_playlist(user_info)
        
        # 스키마 없이 직접 반환 (모든 필드 포함)
        return ApiResponse.success(response)
    
    except Exception as e:
        logger.error(f"인기 플레이리스트 조회 오류: {str(e)}")
        return ApiResponse.error("인기 플레이리스트 조회 중 오류가 발생했습니다.", 500)

@music_bp.route('/music/<int:music_id>/like', methods=['POST'])
@auth_required
def like_music(user_info, music_id):
    """음악 좋아요
    
    Args:
        music_id: 음악 ID
        
    Returns:
        성공 메시지
    """
    try:
        logger.info(f"음악 좋아요 요청: 사용자 ID {user_info.get('id')}, 음악 ID {music_id}")
        
        # 서비스 호출
        MusicService.like_music(music_id, user_info)
        
        return ApiResponse.success(message="좋아요를 추가했습니다.")
    
    except MemberNotFoundException as e:
        logger.warning(f"회원 찾기 실패: {e.message}")
        return ApiResponse.error(e.message, e.status_code, e.error_code)
    
    except MusicNotFoundException as e:
        logger.warning(f"음악 찾기 실패: {e.message}")
        return ApiResponse.error(e.message, e.status_code, e.error_code)
    
    except DuplicateDataException as e:
        logger.warning(f"좋아요 중복: {e.message}")
        return ApiResponse.error(e.message, e.status_code, e.error_code)
    
    except Exception as e:
        logger.error(f"좋아요 추가 오류: {str(e)}")
        return ApiResponse.error("좋아요 처리 중 오류가 발생했습니다.", 500)

@music_bp.route('/music/<int:music_id>/like', methods=['DELETE'])
@auth_required
def unlike_music(user_info, music_id):
    """음악 좋아요 취소
    
    Args:
        music_id: 음악 ID
        
    Returns:
        성공 메시지
    """
    try:
        logger.info(f"음악 좋아요 취소 요청: 사용자 ID {user_info.get('id')}, 음악 ID {music_id}")
        
        # 서비스 호출
        MusicService.unlike_music(music_id, user_info)
        
        return ApiResponse.success(message="좋아요를 취소했습니다.")
    
    except MemberNotFoundException as e:
        logger.warning(f"회원 찾기 실패: {e.message}")
        return ApiResponse.error(e.message, e.status_code, e.error_code)
    
    except MusicNotFoundException as e:
        logger.warning(f"음악 찾기 실패: {e.message}")
        return ApiResponse.error(e.message, e.status_code, e.error_code)
    
    except Exception as e:
        logger.error(f"좋아요 취소 오류: {str(e)}")
        return ApiResponse.error("좋아요 취소 중 오류가 발생했습니다.", 500)