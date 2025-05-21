from marshmallow import Schema, fields, validate, ValidationError

class MemberResponseSchema(Schema):
    """회원 정보 응답 스키마"""
    id = fields.Integer(required=True)
    googleId = fields.String(attribute='google_id', required=True)
    name = fields.String(required=True)
    createdAt = fields.DateTime(attribute='created_at')


class OAuthTokenRequestSchema(Schema):
    """OAuth 토큰 요청 스키마"""
    code = fields.String(required=True, validate=validate.Length(min=1),
                        error_messages={'required': '인증 코드가 필요합니다.'})


class TokenResponseSchema(Schema):
    """토큰 응답 스키마"""
    accessToken = fields.String(required=True)