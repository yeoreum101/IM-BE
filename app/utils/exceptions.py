class APIException(Exception):
    """API 예외의 기본 클래스"""
    def __init__(self, message, status_code=400, error_code=None):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(self.message)


class BadRequestException(APIException):
    """잘못된 요청 예외"""
    def __init__(self, message="잘못된 요청입니다.", error_code="BAD_REQUEST"):
        super().__init__(message=message, status_code=400, error_code=error_code)


class UnauthorizedException(APIException):
    """인증 실패 예외"""
    def __init__(self, message="인증에 실패했습니다.", error_code="UNAUTHORIZED"):
        super().__init__(message=message, status_code=401, error_code=error_code)


class ForbiddenException(APIException):
    """권한 없음 예외"""
    def __init__(self, message="권한이 없습니다.", error_code="FORBIDDEN"):
        super().__init__(message=message, status_code=403, error_code=error_code)


class NotFoundException(APIException):
    """리소스를 찾을 수 없음 예외"""
    def __init__(self, message="요청한 리소스를 찾을 수 없습니다.", error_code="NOT_FOUND"):
        super().__init__(message=message, status_code=404, error_code=error_code)


class MemberNotFoundException(NotFoundException):
    """회원을 찾을 수 없음 예외"""
    def __init__(self, message="회원을 찾을 수 없습니다.", error_code="MEMBER_NOT_FOUND"):
        super().__init__(message=message, error_code=error_code)


class MusicNotFoundException(NotFoundException):
    """음악을 찾을 수 없음 예외"""
    def __init__(self, message="음악을 찾을 수 없습니다.", error_code="MUSIC_NOT_FOUND"):
        super().__init__(message=message, error_code=error_code)


class AIServerException(APIException):
    """AI 서버 관련 예외"""
    def __init__(self, message="AI 서버 처리 중 오류가 발생했습니다.", error_code="AI_SERVER_ERROR"):
        super().__init__(message=message, status_code=500, error_code=error_code)


class DuplicateDataException(APIException):
    """중복 데이터 예외"""
    def __init__(self, message="이미 존재하는 데이터입니다.", error_code="DUPLICATE_DATA"):
        super().__init__(message=message, status_code=409, error_code=error_code)


class ValidationException(APIException):
    """데이터 검증 예외"""
    def __init__(self, message="데이터 검증에 실패했습니다.", errors=None, error_code="VALIDATION_ERROR"):
        self.errors = errors
        super().__init__(message=message, status_code=400, error_code=error_code)


class ExternalAPIException(APIException):
    """외부 API 호출 예외"""
    def __init__(self, message="외부 API 호출 중 오류가 발생했습니다.", status_code=500, error_code="EXTERNAL_API_ERROR"):
        super().__init__(message=message, status_code=status_code, error_code=error_code)