from marshmallow import Schema, fields, validate, ValidationError

class MusicGenWithTextRequestSchema(Schema):
    """텍스트 기반 음악 생성 요청 스키마"""
    prompt1 = fields.String(required=True, validate=validate.Length(min=1, max=500), 
                            error_messages={'required': '프롬프트가 필요합니다.'})


class MusicGenWithTextResponseSchema(Schema):
    """텍스트 기반 음악 생성 응답 스키마"""
    musicUrl = fields.String(required=True)
    title = fields.String(required=True)


class MusicResponseSchema(Schema):
    """음악 정보 응답 스키마"""
    id = fields.Integer(required=True)
    musicUrl = fields.String(required=True, attribute='music_url')
    title = fields.String(required=True)
    duration = fields.Integer(allow_none=True)
    thumbnailUrl = fields.String(attribute='thumbnail_url', allow_none=True)
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