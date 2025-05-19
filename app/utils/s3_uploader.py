import boto3
import uuid
from flask import current_app
from werkzeug.utils import secure_filename
import os
import logging

logger = logging.getLogger(__name__)

class S3Uploader:
    """S3 파일 업로드 유틸리티"""
    
    @staticmethod
    def upload_file_to_s3(file, folder="general"):
        """파일을 S3에 업로드하고 URL 반환
        
        Args:
            file: 업로드할 파일 객체
            folder: S3 내 저장할 폴더 경로
            
        Returns:
            업로드된 파일의 URL
            
        Raises:
            Exception: 업로드 실패 시
        """
        if file is None:
            logger.error("업로드할 파일이 없습니다.")
            return None
        
        try:
            # S3 클라이언트 생성
            s3_client = boto3.client(
                's3',
                aws_access_key_id=current_app.config['AWS_ACCESS_KEY'],
                aws_secret_access_key=current_app.config['AWS_SECRET_KEY'],
                region_name=current_app.config.get('AWS_REGION', 'ap-northeast-2')
            )
            
            # 파일명 안전하게 변경 및 유니크한 이름 생성
            filename = secure_filename(file.filename)
            unique_filename = f"{folder}/{uuid.uuid4().hex}_{filename}"
            
            logger.info(f"S3 업로드 시작: {filename} -> {unique_filename}")
            
            # 파일 업로드
            s3_client.upload_fileobj(
                file,
                current_app.config['S3_BUCKET_NAME'],
                unique_filename,
                ExtraArgs={
                    'ACL': 'public-read',
                    'ContentType': file.content_type
                }
            )
            
            # S3 URL 생성
            s3_url = f"{current_app.config['S3_URL']}/{unique_filename}"
            logger.info(f"S3 업로드 완료: {s3_url}")
            
            return s3_url
            
        except Exception as e:
            logger.error(f"S3 업로드 실패: {str(e)}")
            raise Exception(f"S3 업로드 실패: {str(e)}")
    
    @staticmethod
    def delete_file_from_s3(file_url):
        """S3에서 파일 삭제
        
        Args:
            file_url: 삭제할 파일의 URL
            
        Returns:
            True (성공 시)
            
        Raises:
            Exception: 삭제 실패 시
        """
        try:
            # URL에서 키 추출
            s3_base_url = current_app.config['S3_URL']
            if not file_url or not file_url.startswith(s3_base_url):
                logger.warning(f"올바르지 않은 S3 URL: {file_url}")
                return False
            
            s3_key = file_url.replace(f"{s3_base_url}/", "")
            
            # S3 클라이언트 생성
            s3_client = boto3.client(
                's3',
                aws_access_key_id=current_app.config['AWS_ACCESS_KEY'],
                aws_secret_access_key=current_app.config['AWS_SECRET_KEY'],
                region_name=current_app.config.get('AWS_REGION', 'ap-northeast-2')
            )
            
            logger.info(f"S3 파일 삭제 시작: {s3_key}")
            
            # 파일 삭제
            s3_client.delete_object(
                Bucket=current_app.config['S3_BUCKET_NAME'],
                Key=s3_key
            )
            
            logger.info(f"S3 파일 삭제 완료: {file_url}")
            return True
            
        except Exception as e:
            logger.error(f"S3 파일 삭제 실패: {str(e)}")
            raise Exception(f"S3 파일 삭제 실패: {str(e)}")