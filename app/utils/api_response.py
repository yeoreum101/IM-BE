from flask import jsonify
from typing import Optional, Dict, Any, Union, Tuple, List

class ApiResponse:
    @staticmethod
    def success(
        data: Optional[Union[Dict[str, Any], List[Any]]] = None, 
        status_code: int = 200, 
        message: Optional[str] = None
    ) -> Tuple[Dict[str, Any], int]:
        """성공 응답 생성
        
        Args:
            data: 응답 데이터
            status_code: HTTP 상태 코드
            message: 응답 메시지
            
        Returns:
            JSON 응답과 HTTP 상태 코드
        """
        response = {
            'success': True,
            'status': status_code
        }
        
        if data is not None:
            response['data'] = data
            
        if message is not None:
            response['message'] = message
            
        return jsonify(response), status_code
    
    @staticmethod
    def error(
        message: str, 
        status_code: int = 400, 
        error_code: Optional[str] = None,
        errors: Optional[Dict[str, List[str]]] = None
    ) -> Tuple[Dict[str, Any], int]:
        """에러 응답 생성
        
        Args:
            message: 에러 메시지
            status_code: HTTP 상태 코드
            error_code: 에러 코드
            errors: 상세 에러 정보
            
        Returns:
            JSON 응답과 HTTP 상태 코드
        """
        response = {
            'success': False,
            'status': status_code,
            'message': message
        }
        
        if error_code is not None:
            response['error_code'] = error_code
            
        if errors is not None:
            response['errors'] = errors
        
        return jsonify(response), status_code