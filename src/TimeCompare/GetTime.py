from . import TIME
from datetime import time
import re

def get_time_period(period: str, start_header: str = "Bắt đầu", end_header: str = "Kết thúc") -> tuple[time, time]:
    """
    Lấy thời gian bắt đầu và kết thúc của một tiết học

    Args:
        period (str): Độ dài tiết học (Từ tiết mấy đến tiết mấy)
        start_header (str, optional): Cột chứa thời gian bắt đầu. Mặc định là "Bắt đầu".
        end_header (str, optional): Cột chứa thời gian kết thúc. Mặc định là "Kết thúc".

    Returns:
        tuple[time, time]: Thời gian bắt đầu và kết thúc của tiết học
    """
    PATTERN = r"\d+(-\d+)?"

    match = re.search(PATTERN, period)
    start_period = int(match.group()) - 1
    end_period = start_period if "-" not in period else int(match.group().split('-')[-1]) - 1

    start_time = TIME[start_period][start_header]
    end_time = TIME[end_period][end_header]

    return start_time, end_time
