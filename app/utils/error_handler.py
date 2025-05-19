from flask import jsonify
from app.utils.exceptions import (
    APIException, BadRequestException, UnauthorizedException, 
    ForbiddenException, NotFoundException, MemberNotFoundException,
    MusicNotFoundException, AIServerException, ValidationException
)
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest, InternalServerError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import traceback
import logging

logger = logging.getLogger(__name__)

def register_error_handlers(app):
    """앱에 에러 핸들러 등록"""
    
    @app.errorhandler(APIException)
    def handle_api_exception(error):
        response = {
            'success': False,
            'status': error.status_code,
            'message': error.message
        }
        
        if error.error_code:
            response['error_code'] = error.error_code
            
        if hasattr(error, 'errors') and error.errors:
            response['errors'] = error.errors
            
        return jsonify(response), error.status_code
    
    @app.errorhandler(BadRequestException)
    def handle_bad_request_exception(error):
        return handle_api_exception(error)
    
    @app.errorhandler(UnauthorizedException)
    def handle_unauthorized_exception(error):
        return handle_api_exception(error)
    
    @app.errorhandler(ForbiddenException)
    def handle_forbidden_exception(error):
        return handle_api_exception(error)
    
    @app.errorhandler(NotFoundException)
    def handle_not_found_exception(error):
        return handle_api_exception(error)
    
    @app.errorhandler(MemberNotFoundException)
    def handle_member_not_found_exception(error):
        return handle_api_exception(error)
    
    @app.errorhandler(MusicNotFoundException)
    def handle_music_not_found_exception(error):
        return handle_api_exception(error)
    
    @app.errorhandler(ValidationException)
    def handle_validation_exception(error):
        return handle_api_exception(error)
    
    @app.errorhandler(404)
    def handle_404(error):
        response = {
            'success': False,
            'status': 404,
            'message': '요청한 리소스를 찾을 수 없습니다.',
            'error_code': 'NOT_FOUND'
        }
        return jsonify(response), 404
    
    @app.errorhandler(405)
    def handle_405(error):
        response = {
            'success': False,
            'status': 405,
            'message': '지원하지 않는 HTTP 메서드입니다.',
            'error_code': 'METHOD_NOT_ALLOWED'
        }
        return jsonify(response), 405
    
    @app.errorhandler(400)
    def handle_400(error):
        response = {
            'success': False,
            'status': 400,
            'message': '잘못된 요청입니다.',
            'error_code': 'BAD_REQUEST'
        }
        return jsonify(response), 400
    
    @app.errorhandler(500)
    def handle_500(error):
        # 에러 로깅
        logger.error(f"Internal Server Error: {str(error)}")
        logger.error(traceback.format_exc())
        
        response = {
            'success': False,
            'status': 500,
            'message': '서버 내부 오류가 발생했습니다.',
            'error_code': 'INTERNAL_SERVER_ERROR'
        }
        return jsonify(response), 500
    
    @app.errorhandler(SQLAlchemyError)
    def handle_sqlalchemy_error(error):
        # 에러 로깅
        logger.error(f"Database Error: {str(error)}")
        logger.error(traceback.format_exc())
        
        # 무결성 제약 조건 오류 처리
        if isinstance(error, IntegrityError):
            response = {
                'success': False,
                'status': 409,
                'message': '데이터 무결성 제약 조건을 위반했습니다.',
                'error_code': 'INTEGRITY_ERROR'
            }
            return jsonify(response), 409
        
        # 기타 데이터베이스 오류
        response = {
            'success': False,
            'status': 500,
            'message': '데이터베이스 오류가 발생했습니다.',
            'error_code': 'DATABASE_ERROR'
        }
        return jsonify(response), 500