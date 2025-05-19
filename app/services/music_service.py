from app import db
from app.models.music import Music
from app.models.mymusic import MyMusic
from app.models.like import Like
from app.models.member import Member
from app.utils.exceptions import MusicNotFoundException, MemberNotFoundException, DuplicateDataException, AIServerException
from app.clients.ai_client import AIClient
from sqlalchemy import func, desc
from flask import current_app
import os
import logging

logger = logging.getLogger(__name__)

class MusicService:
    """음악 생성 및 관리 서비스"""
    
    @staticmethod
    def generate_music_with_text(prompt1, user_info=None):
        """텍스트 기반 음악 생성
        
        Args:
            prompt1: 텍스트 프롬프트
            user_info: 사용자 정보 (선택)
            
        Returns:
            생성된 음악 정보
            
        Raises:
            AIServerException: AI 서버 처리 중 오류 발생 시
            MemberNotFoundException: 회원을 찾을 수 없는 경우
        """
        try:
            # AI 서버 호출
            ai_client = AIClient()
            response = ai_client.generate_music_with_text(prompt1)
            
            s3_url = response.get('music_url')
            duration = response.get('duration')
            
            if not s3_url:
                raise AIServerException("음악 생성에 실패했습니다.")
            
            # Music 테이블에 저장
            music = Music(
                music_url=s3_url, 
                title=prompt1,
                duration=duration
            )
            db.session.add(music)
            
            # 인증된 사용자라면 MyMusic에도 저장
            if user_info:
                member = Member.find_by_google_id(user_info.get('google_id'))
                if not member:
                    raise MemberNotFoundException()
                
                my_music = MyMusic(
                    music_url=s3_url, 
                    title=prompt1, 
                    member_id=member.id,
                    duration=duration
                )
                db.session.add(my_music)
            
            db.session.commit()
            logger.info(f"음악 생성 완료: {prompt1}")
            
            return {
                'musicUrl': s3_url,
                'title': prompt1,
                'duration': duration
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"텍스트 기반 음악 생성 오류: {str(e)}")
            if isinstance(e, (AIServerException, MemberNotFoundException)):
                raise
            raise AIServerException("음악 생성 중 오류가 발생했습니다.")
    
    @staticmethod
    def generate_music_with_image(image_file, user_info=None):
        """이미지 기반 음악 생성
        
        Args:
            image_file: 이미지 파일
            user_info: 사용자 정보 (선택)
            
        Returns:
            생성된 음악 정보
            
        Raises:
            AIServerException: AI 서버 처리 중 오류 발생 시
            MemberNotFoundException: 회원을 찾을 수 없는 경우
        """
        try:
            # AI 서버 호출
            ai_client = AIClient()
            response = ai_client.generate_music_with_image(image_file)
            
            s3_url = response.get('music_url')
            title = response.get('title')
            duration = response.get('duration')
            
            if not s3_url or not title:
                raise AIServerException("음악 생성에 실패했습니다.")
            
            # Music 테이블에 저장
            music = Music(
                music_url=s3_url, 
                title=title,
                duration=duration
            )
            db.session.add(music)
            
            # 인증된 사용자라면 MyMusic에도 저장
            if user_info:
                member = Member.find_by_google_id(user_info.get('google_id'))
                if not member:
                    raise MemberNotFoundException()
                
                my_music = MyMusic(
                    music_url=s3_url, 
                    title=title, 
                    member_id=member.id,
                    duration=duration
                )
                db.session.add(my_music)
            
            db.session.commit()
            logger.info(f"이미지 기반 음악 생성 완료: {title}")
            
            return {
                'musicUrl': s3_url,
                'title': title,
                'duration': duration
            }
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"이미지 기반 음악 생성 오류: {str(e)}")
            if isinstance(e, (AIServerException, MemberNotFoundException)):
                raise
            raise AIServerException("음악 생성 중 오류가 발생했습니다.")
    
    @staticmethod
    def get_my_playlist(user_info, limit=10):
        """내 플레이리스트 조회
        
        Args:
            user_info: 사용자 정보
            limit: 조회할 최대 항목 수
            
        Returns:
            플레이리스트 정보
            
        Raises:
            MemberNotFoundException: 회원을 찾을 수 없는 경우
        """
        if not user_info:
            raise MemberNotFoundException("인증되지 않은 사용자입니다.")
        
        member = Member.find_by_google_id(user_info.get('google_id'))
        if not member:
            raise MemberNotFoundException("회원 정보를 찾을 수 없습니다.")
        
        # 최근 생성된 순서로 조회
        my_musics = MyMusic.find_by_member_id(member.id, limit)
        
        # 응답 형식에 맞게 변환
        music_list = []
        for music in my_musics:
            music_list.append({
                'id': music.id,
                'musicUrl': music.music_url,
                'title': music.title,
                'duration': music.duration,
                'thumbnailUrl': music.thumbnail_url,
                'createdAt': music.created_at
            })
        
        return {
            'name': member.name,
            'musicList': music_list
        }
    
    @staticmethod
    def get_playlist(user_info=None, limit=10):
        """전체 플레이리스트 조회
        
        Args:
            user_info: 사용자 정보 (선택)
            limit: 조회할 최대 항목 수
            
        Returns:
            플레이리스트 정보
        """
        # 최근 생성된 순서로 조회
        musics = Music.find_recent(limit)
        
        # 응답 형식에 맞게 변환
        music_list = []
        member_id = None
        
        # 인증된 사용자인 경우 회원 ID 조회
        if user_info:
            member = Member.find_by_google_id(user_info.get('google_id'))
            if member:
                member_id = member.id
        
        for music in musics:
            like_count = Like.count_by_music(music.id)
            pressed = False
            
            # 인증된 사용자면 좋아요 여부 확인
            if member_id:
                pressed = Like.find_by_member_and_music(member_id, music.id) is not None
            
            music_list.append({
                'id': music.id,
                'musicUrl': music.music_url,
                'title': music.title,
                'duration': music.duration,
                'thumbnailUrl': music.thumbnail_url,
                'likeCount': like_count,
                'pressed': pressed,
                'createdAt': music.created_at
            })
        
        return {
            'musicList': music_list
        }
    
    @staticmethod
    def get_popular_playlist(user_info=None, limit=10):
        """인기 플레이리스트 조회
        
        Args:
            user_info: 사용자 정보 (선택)
            limit: 조회할 최대 항목 수
            
        Returns:
            인기 플레이리스트 정보
        """
        # 좋아요 수가 많은 순서로 조회
        musics = Music.find_popular(limit)
        
        # 응답 형식에 맞게 변환
        music_list = []
        member_id = None
        
        # 인증된 사용자인 경우 회원 ID 조회
        if user_info:
            member = Member.find_by_google_id(user_info.get('google_id'))
            if member:
                member_id = member.id
        
        for music in musics:
            like_count = Like.count_by_music(music.id)
            pressed = False
            
            # 인증된 사용자면 좋아요 여부 확인
            if member_id:
                pressed = Like.find_by_member_and_music(member_id, music.id) is not None
            
            music_list.append({
                'id': music.id,
                'musicUrl': music.music_url,
                'title': music.title,
                'duration': music.duration,
                'thumbnailUrl': music.thumbnail_url,
                'likeCount': like_count,
                'pressed': pressed,
                'createdAt': music.created_at
            })
        
        return {
            'musicList': music_list
        }
    
    @staticmethod
    def like_music(music_id, user_info):
        """음악 좋아요
        
        Args:
            music_id: 음악 ID
            user_info: 사용자 정보
            
        Returns:
            True (성공 시)
            
        Raises:
            MemberNotFoundException: 회원을 찾을 수 없는 경우
            MusicNotFoundException: 음악을 찾을 수 없는 경우
            DuplicateDataException: 이미 좋아요한 경우
        """
        if not user_info:
            raise MemberNotFoundException("인증되지 않은 사용자입니다.")
        
        member = Member.find_by_google_id(user_info.get('google_id'))
        if not member:
            raise MemberNotFoundException("회원 정보를 찾을 수 없습니다.")
        
        music = Music.find_by_id(music_id)
        if not music:
            raise MusicNotFoundException(f"ID가 {music_id}인 음악을 찾을 수 없습니다.")
        
        # 이미 좋아요를 눌렀는지 확인
        existing_like = Like.find_by_member_and_music(member.id, music_id)
        if existing_like:
            raise DuplicateDataException("이미 좋아요를 누른 노래입니다.")
        
        try:
            # 좋아요 추가
            like = Like(member_id=member.id, music_id=music_id)
            db.session.add(like)
            db.session.commit()
            logger.info(f"좋아요 추가: 회원 ID {member.id}, 음악 ID {music_id}")
            
            return True
        except Exception as e:
            db.session.rollback()
            logger.error(f"좋아요 추가 실패: {str(e)}")
            raise
    
    @staticmethod
    def unlike_music(music_id, user_info):
        """음악 좋아요 취소
        
        Args:
            music_id: 음악 ID
            user_info: 사용자 정보
            
        Returns:
            True (성공 시)
            
        Raises:
            MemberNotFoundException: 회원을 찾을 수 없는 경우
            MusicNotFoundException: 음악을 찾을 수 없는 경우
        """
        if not user_info:
            raise MemberNotFoundException("인증되지 않은 사용자입니다.")
        
        member = Member.find_by_google_id(user_info.get('google_id'))
        if not member:
            raise MemberNotFoundException("회원 정보를 찾을 수 없습니다.")
        
        # 이미 좋아요를 눌렀는지 확인
        existing_like = Like.find_by_member_and_music(member.id, music_id)
        if not existing_like:
            # 좋아요가 없으면 성공으로 간주 (멱등성 보장)
            return True
        
        try:
            # 좋아요 삭제
            db.session.delete(existing_like)
            db.session.commit()
            logger.info(f"좋아요 취소: 회원 ID {member.id}, 음악 ID {music_id}")
            
            return True
        except Exception as e:
            db.session.rollback()
            logger.error(f"좋아요 취소 실패: {str(e)}")
            raise