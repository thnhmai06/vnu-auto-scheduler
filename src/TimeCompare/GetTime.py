import re
from datetime import time
from . import TIME

def get_time_period(period: str, start_header: str = "Bắt đầu", end_header: str = "Kết thúc") -> tuple[time, time]:
    """
    Lấy thời gian bắt đầu và kết thúc của một tiết học

    Parameters:
        period (str): Độ dài tiết học (Từ tiết mấy đến tiết mấy)
        start_header (str, optional): Cột chứa thời gian bắt đầu. Mặc định là "Bắt đầu".
        end_header (str, optional): Cột chứa thời gian kết thúc. Mặc định là "Kết thúc".

    Returns:
        tuple[time, time]: Thời gian bắt đầu và kết thúc của tiết học
    """
    PATTERN = r"\d+(-\d+)?"
    match = re.search(PATTERN, period)
    period = match.group() # Dạng có thể là 01-2, 10-12, 12, 1-5

    if "-" in period:
        start_period, end_period = map(int, period.split("-"))
    else:
        start_period = end_period = int(period)

    start_time = TIME[start_period][start_header]
    end_time = TIME[end_period][end_header]

    return start_time, end_time
