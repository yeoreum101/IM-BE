from app import db
from app.models.member import Member
from app.auth.token_auth import generate_token
from app.utils.exceptions import MemberNotFoundException
import logging

logger = logging.getLogger(__name__)

class MemberService:
    """회원 관련 서비스"""
    
    @staticmethod
    def find_member_by_google_id(google_id):
        """구글 ID로 회원 찾기
        
        Args:
            google_id: 구글 ID
            
        Returns:
            Member 객체 또는 None
        """
        return Member.find_by_google_id(google_id)
    
    @staticmethod
    def create_member(google_id, name, email=None, profile_image=None):
        """회원 생성
        
        Args:
            google_id: 구글 ID
            name: 이름
            
        Returns:
            생성된 Member 객체
        """
        try:
            new_member = Member(
                google_id=google_id, 
                name=name
            )
            db.session.add(new_member)
            db.session.commit()
            logger.info(f"새 회원 생성 완료: {google_id}")
            return new_member
        except Exception as e:
            db.session.rollback()
            logger.error(f"회원 생성 실패: {str(e)}")
            raise
    
    @staticmethod
    def find_or_create_member_by_google_id(user_info):
        """구글 ID로 회원 조회 또는 생성
        
        Args:
            user_info: 구글 사용자 정보
            
        Returns:
            JWT 액세스 토큰
        """
        google_id = user_info.get('id')
        name = user_info.get('name')
        
        if not google_id or not name:
            logger.error(f"회원 정보 부족: {user_info}")
            raise ValueError("유효하지 않은 사용자 정보입니다.")
        
        member = MemberService.find_member_by_google_id(google_id)
        
        if not member:
            # 새 회원 생성
            member = MemberService.create_member(
                google_id=google_id, 
                name=name
            )
        
        # 액세스 토큰 생성
        access_token = generate_token(member)
        
        return access_token
    
    @staticmethod
    def get_member_by_id(member_id):
        """ID로 회원 조회
        
        Args:
            member_id: 회원 ID
            
        Returns:
            Member 객체
            
        Raises:
            MemberNotFoundException: 회원을 찾을 수 없는 경우
        """
        member = Member.find_by_id(member_id)
        if not member:
            raise MemberNotFoundException(f"ID가 {member_id}인 회원을 찾을 수 없습니다.")
        return member
    
    @staticmethod
    def get_member_profile(member_id):
        """회원 프로필 조회
        
        Args:
            member_id: 회원 ID
            
        Returns:
            회원 프로필 정보
            
        Raises:
            MemberNotFoundException: 회원을 찾을 수 없는 경우
        """
        member = MemberService.get_member_by_id(member_id)
        return member.to_dict()