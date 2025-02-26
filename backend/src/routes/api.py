import importlib
from flask import request
from utils.response import make_response, APIError

def register_api_routes(app):
    logger = app.logger
    
    @app.route('/api/v<version>/<string:name>', methods=['GET', 'POST'])
    def handle_api_request(version, name):  # noqa
        """Xử lý các API request"""
        logger.info(f"Processing {request.method} request for API v{version}/{name}")
        
        # Xác định handler cho API
        module_name = f'API.v{version}.{name}'
        logger.debug(f"Importing module: {module_name}")
        
        try:
            module = importlib.import_module(module_name)
        except ModuleNotFoundError:
            logger.error(f"API not found: {module_name}")
            raise APIError(f"API v{version}/{name} not found", status_code=404)
            
        # Lấy tham số từ request
        args = request.args
        argv = request.json if request.method == 'POST' else {}
        logger.debug(f"Request parameters - args: {args}, body: {argv}")

        # Gọi hàm xử lý request
        logger.info("Calling handler function")
        result = module.handle_request(request, args, argv)
        
        return make_response(result) 