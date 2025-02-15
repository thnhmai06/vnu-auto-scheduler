from icalendar import Event, Alarm
from TimeCompare.GetTime import get_time_period
from datetime import date, timedelta, datetime

def get_date_from_weekday(date_in_week: date, day_of_the_week: int) -> date:
    """
    Lấy ngày trong tuần từ ngày bắt đầu và thứ trong tuần

    Parameters:
        date_in_week (date): Một ngày của tuần
        day_of_the_week (int): Thứ trong tuần (2, 3, ..., 7, 8)

    Returns:
        date: Ngày tương ứng
    """
    day_of_the_week_based_on_0 = day_of_the_week - 2 # Vì thứ 2 là 0, thứ 3 là 1, ..., thứ 7 là 5
    return date_in_week + timedelta(days=day_of_the_week_based_on_0 - date_in_week.weekday())

def create_event(data: dict, name_header: str, day_of_the_week_header: str, start_date: date, 
                 period_header: str, location_header: str, loop: int | date = int(1)) -> Event:
    """
    Tạo sự kiện lịch từ dữ liệu

    Parameters:
        data (dict): Dữ liệu để tạo sự kiện.
        name_header (str): Header của tên sự kiện.
        day_of_the_week_header (str): Header Thứ trong tuần từ dữ liệu.
        start_date (date): Ngày bắt đầu tuần học đầu tiên.
        period_header (str): Header của khoảng thời gian.
        location_header (str): Header của vị trí.
        loop (int | date): Biến để điều khiển lặp lại sự kiện. (int: số lần lặp tính cả ngày ban đầu, date: ngày kết thúc lặp lại). Mặc định là 1

    Returns:
        Event: Đối tượng sự kiện đã tạo.
    """
    # Lấy dữ liệu
    summary: str = data[name_header]
    location: str = data[location_header]
    day_of_the_week: int = data[day_of_the_week_header]
    period = get_time_period(data[period_header])
    description = '\n'.join([f"{key}: {value}" for key, value in data.items()])

    # Gộp ngày tháng với thời gian
    event_date = get_date_from_weekday(start_date, day_of_the_week)
    event_start = datetime.combine(event_date, period[0])
    event_end = datetime.combine(event_date, period[1])

    # Tạo Event
    event = Event()
    event.add('summary', summary)
    event.add('dtstart', event_start)
    event.add('dtend', event_end)
    event.add('location', location)
    event.add('description', description)
    if isinstance(loop, int):
        event.add('rrule', {'freq': 'weekly', 'count': loop})
    elif isinstance(loop, date):
        event.add('rrule', {'freq': 'weekly', 'until': loop.isoformat()})
    
    return event

def import_alarm(event: Event, alarms: Alarm | list[Alarm]) -> Event:
    """
    Thêm nhắc nhở vào sự kiện

    Parameters:
        event (Event): Sự kiện cần thêm nhắc nhở.
        alarms (Alarm | list[Alarm]): Nhắc nhở.

    Returns:
        Event: Sự kiện đã thêm nhắc nhở.
    """

    if isinstance(alarms, Alarm):
        alarms = [alarms]
    for alarm in alarms:
        event.add_component(alarm)
    return event