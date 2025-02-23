import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime
from colorama import Fore, Style, init

# Khởi tạo colorama
init(autoreset=True)

class ColoredFormatter(logging.Formatter):
    """
    Formatter tùy chỉnh để thêm màu cho log messages sử dụng colorama.
    """
    COLORS = {
        logging.DEBUG: Fore.WHITE + Style.DIM,
        logging.INFO: Fore.BLUE + Style.NORMAL,
        logging.WARNING: Fore.YELLOW + Style.NORMAL,
        logging.ERROR: Fore.RED + Style.NORMAL,
        logging.CRITICAL: Fore.RED + Style.BRIGHT
    }

    def format(self, record: logging.LogRecord) -> str:
        # Thêm thông tin thời gian
        record.time = datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M:%S")
        
        # Lấy tên file ngắn gọn
        record.shortpath = record.pathname.split('/')[-1] if '/' in record.pathname else record.pathname
        
        # Thêm màu cho level name
        color = self.COLORS.get(record.levelno, '')
        # Lưu levelname gốc
        original_levelname = record.levelname
        record.levelname = f"{color}{record.levelname}{Style.RESET_ALL}"
        
        # Định dạng message với màu
        formatted_message = super().format(record)
        
        # Khôi phục levelname gốc để tránh tích tụ mã màu
        record.levelname = original_levelname
        
        if record.exc_info:
            text = self.formatException(record.exc_info)
            formatted_message += f"\n{Fore.RED}{text}{Style.RESET_ALL}"
            
        return formatted_message

def setup_logging(app):
    # Tạo đường dẫn tuyệt đối đến thư mục logs
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    log_dir = os.path.join(project_root, 'logs')
    
    # Tạo thư mục logs nếu chưa tồn tại
    os.makedirs(log_dir, exist_ok=True)
    
    # Tạo tên file log với timestamp
    current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = os.path.join(log_dir, f'app_{current_time}.log')
    
    # Cấu hình formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # File handler với rotation
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=1024 * 1024,  # 1MB
        backupCount=10,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    
    # Stream handler cho console
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.INFO)
    
    # Cấu hình cho app logger
    app.logger.addHandler(file_handler)
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO)
    
    # Log startup message
    app.logger.info('Logging system initialized')

    # Thêm handler cho các module khác
    for logger_name in logging.root.manager.loggerDict:
        if logger_name.startswith('src.'):
            logger = logging.getLogger(logger_name)
            logger.addHandler(stream_handler)
            logger.addHandler(file_handler)
            logger.setLevel(logging.INFO) 