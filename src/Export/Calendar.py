import os
from icalendar import Calendar

def ics(calendar: Calendar, location: str, file_name: str) -> str | Exception:
    '''
    Xuất lịch dưới dạng file .ics

    Parameters:
        calendar (Calendar): Lịch cần xuất
        location (str): Đường dẫn lưu file
        file_name (str): Tên file

    Returns:
        str | Exception: Đường dẫn file hoặc lỗi nếu có
    '''
    data = calendar.to_ical()
    location = os.path.abspath(location)
    full_path = os.path.join(location, f"{file_name}.ics")
    try:
        with open(full_path, 'wb', encoding='utf-8') as file:
            file.write(data)
    except Exception as e:
        return e
    return full_path