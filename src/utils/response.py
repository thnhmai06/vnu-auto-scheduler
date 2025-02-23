from flask import jsonify
from typing import Any, Dict, Optional

class APIError(Exception):
    """Custom exception cho API errors"""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

def make_response(data: Any, status: int = 200, message: Optional[str] = None) -> Dict:
    """
    Tạo response format chuẩn cho API
    
    Args:
        data: Data trả về
        status: HTTP status code
        message: Message tùy chọn
        
    Returns:
        Dict chứa response đã được format
    """
    response = {
        'status': status,
        'data': data
    }
    
    if message:
        response['message'] = message
        
    return jsonify(response) 