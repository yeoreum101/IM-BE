from marshmallow import Schema, fields, validate, ValidationError

class MusicGenWithTextRequestSchema(Schema):
    """텍스트 기반 음악 생성 요청 스키마"""
    prompt1 = fields.String(required=True, validate=validate.Length(min=1, max=500), 
                            error_messages={'required': '프롬프트가 필요합니다.'})
    prompt2 = fields.String(required=False, validate=validate.Length(max=500), 
                            missing="", default="")


class MusicGenWithTextResponseSchema(Schema):
    """텍스트 기반 음악 생성 응답 스키마"""
    musicUrl = fields.String(required=True)
    title = fields.String(required=True)


class MusicGenWithImageResponseSchema(Schema):
    """이미지 기반 음악 생성 응답 스키마"""
    musicUrl = fields.String(required=True)
    title = fields.String(required=True)


class MusicGenWithVideoResponseSchema(Schema):
    """동영상 기반 음악 생성 응답 스키마"""
    musicUrl = fields.String(required=True)
    title = fields.String(required=True)


class ImageUploadRequestSchema(Schema):
    """이미지 업로드 요청 검증 스키마"""
    
    def validate_image_file(self, file):
        """이미지 파일 검증"""
        if not file:
            raise ValidationError("이미지 파일이 필요합니다.")
        
        if file.filename == '':
            raise ValidationError("이미지가 선택되지 않았습니다.")
        
        # 확장자 검사
        allowed_extensions = {'jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'}
        if '.' not in file.filename:
            raise ValidationError("올바른 이미지 파일을 선택해주세요.")
        
        extension = file.filename.rsplit('.', 1)[1].lower()
        if extension not in allowed_extensions:
            raise ValidationError(f"지원하지 않는 이미지 형식입니다. 지원 형식: {', '.join(allowed_extensions)}")
        
        # 파일 크기 검사
        MAX_SIZE = 10 * 1024 * 1024  # 10MB
        if hasattr(file, 'content_length') and file.content_length:
            if file.content_length > MAX_SIZE:
                raise ValidationError("이미지 파일이 너무 큽니다. 최대 10MB까지 지원합니다.")
        
        return True


class VideoUploadRequestSchema(Schema):
    """동영상 업로드 요청 검증 스키마"""
    
    def validate_video_file(self, file):
        """동영상 파일 검증"""
        if not file:
            raise ValidationError("동영상 파일이 필요합니다.")
        
        if file.filename == '':
            raise ValidationError("동영상이 선택되지 않았습니다.")
        
        # 확장자 검사
        allowed_extensions = {'mp4', 'mov', 'avi', 'mkv', 'webm', 'flv', 'wmv'}
        if '.' not in file.filename:
            raise ValidationError("올바른 동영상 파일을 선택해주세요.")
        
        extension = file.filename.rsplit('.', 1)[1].lower()
        if extension not in allowed_extensions:
            raise ValidationError(f"지원하지 않는 동영상 형식입니다. 지원 형식: {', '.join(allowed_extensions)}")
        
        # 파일 크기 검사
        MAX_SIZE = 100 * 1024 * 1024  # 100MB
        if hasattr(file, 'content_length') and file.content_length:
            if file.content_length > MAX_SIZE:
                raise ValidationError("동영상 파일이 너무 큽니다. 최대 100MB까지 지원합니다.")
        
        return True


class MusicResponseSchema(Schema):
    """음악 정보 응답 스키마"""
    id = fields.Integer(required=True)
    musicUrl = fields.String(required=True, attribute='music_url')
    title = fields.String(required=True)
    likeCount = fields.Integer(attribute='like_count', dump_only=True)
    pressed = fields.Boolean(dump_only=True)
    createdAt = fields.DateTime(attribute='created_at')


class PlaylistResponseSchema(Schema):
    """플레이리스트 응답 스키마"""
    musicList = fields.List(fields.Nested(MusicResponseSchema), required=True)


class MyPlaylistResponseSchema(Schema):
    """내 플레이리스트 응답 스키마"""
    name = fields.String(required=True)
    musicList = fields.List(fields.Nested(MusicResponseSchema), required=True)


# 파일 검증 유틸리티 함수들
class FileValidationUtils:
    """파일 검증 유틸리티"""
    
    @staticmethod
    def validate_image_file(file):
        """이미지 파일 검증 헬퍼"""
        schema = ImageUploadRequestSchema()
        return schema.validate_image_file(file)
    
    @staticmethod
    def validate_video_file(file):
        """동영상 파일 검증 헬퍼"""
        schema = VideoUploadRequestSchema()
        return schema.validate_video_file(file)
    
    @staticmethod
    def get_file_extension(filename):
        """파일 확장자 추출"""
        if '.' not in filename:
            return None
        return filename.rsplit('.', 1)[1].lower()
    
    @staticmethod
    def is_allowed_image(filename):
        """허용된 이미지 형식인지 확인"""
        extension = FileValidationUtils.get_file_extension(filename)
        return extension in {'jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'}
    
    @staticmethod
    def is_allowed_video(filename):
        """허용된 동영상 형식인지 확인"""
        extension = FileValidationUtils.get_file_extension(filename)
        return extension in {'mp4', 'mov', 'avi', 'mkv', 'webm', 'flv', 'wmv'}