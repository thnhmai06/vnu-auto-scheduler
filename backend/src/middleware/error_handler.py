from flask import jsonify
from utils.response import APIError

def register_error_handlers(app):
    logger = app.logger
    
    @app.errorhandler(APIError)
    def handle_api_error(error):  # noqa
        """Xử lý APIError được raise từ code"""
        response = {
            'error': error.message,
            'status': error.status_code
        }
        return jsonify(response), error.status_code

    @app.errorhandler(Exception)
    def handle_generic_error(error):  # noqa
        """Xử lý các lỗi không mong muốn"""
        logger.exception("Unexpected error occurred")
        response = {
            'error': str(error),
            'status': 500
        }
        return jsonify(response), 500 