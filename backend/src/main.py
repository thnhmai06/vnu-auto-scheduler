from flask import Flask
from config.logging import setup_logging
from middleware.error_handler import register_error_handlers
from routes.api import register_api_routes

app = Flask(__name__)
setup_logging(app)  # Sử dụng cấu hình logging từ config
logger = app.logger

# Đăng ký các routes
register_api_routes(app)

# Đăng ký error handlers
register_error_handlers(app)

if __name__ == '__main__':
    logger.info("Starting server...")
    app.run(debug=True)