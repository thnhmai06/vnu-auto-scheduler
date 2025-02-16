import os
from subject import FulfilledClass
from datetime import timedelta, date, datetime
from icalendar import Event, Alarm, Calendar as ICalendar

class Alarms(list[Alarm]):
    """
    Lớp đại diện cho danh sách các lời nhắc (alarms).
    """
    def add_alarm(self, remind_before: int):
        """
        Thêm một lời nhắc vào danh sách.

        Args:
            remind_before (int): Số phút trước khi sự kiện diễn ra để nhắc nhở.
        """
        alarm = Alarm()
        alarm.add('ACTION', 'DISPLAY')
        alarm.add('TRIGGER', timedelta(minutes=-remind_before))
        self.append(alarm)
        return self
    
    def __new__(cls, remind_before: int | list[int]):
        """
        Args:
            remind_before (int | list[int]): Số phút trước khi sự kiện diễn ra để nhắc nhở.
        """
        self = object().__new__(cls)
        if not isinstance(remind_before, list):
            remind_before = [remind_before]
        for remind in remind_before:
            self.add_alarm(remind)
        return self

def _get_date_from_weekday(date_in_week: date, weekday: int) -> date:
    """
    Trả về ngày của tuần chứa date_in_week mà có thứ là weekday.

    Parameters:
        date_in_week (date): Một ngày của tuần đó
        weekday (int): Thứ của ngày đó ở dạng 0-based (0: Thứ 2, 1: Thứ 3, ..., 6: Chủ nhật)

    Returns:
        date: Ngày tương ứng

    Examples:
        - Lấy ngày Thứ Hai của tuần chứa ngày 16/2/2025
        >>> _get_date_from_weekday(date(2025, 2, 16), 0)
        (2025, 2, 16)

        - Lấy ngày Chủ Nhật của tuần chứa ngày 16/2/2025
        >>> _get_date_from_weekday(date(2025, 2, 16), 6)
        (2025, 2, 16)
    """
    week_startday = date_in_week - timedelta(days=date_in_week.weekday())
    return week_startday + timedelta(days=weekday)

class Events(list[Event]):
    """
    Lớp đại diện cho danh sách các sự kiện (events).
    """
    def __new__(cls, class_: FulfilledClass, start_first_week: date, repeat: int | date = 1):
        """
        Args:
            class_ (FulfilledClass): Lớp học đầy đủ thông tin.
            start_first_week (date): Ngày bắt đầu của tuần học đầu tiên.
            repeat (int | date, optional): Số lần lặp lại (tính cả ngày đầu tiên) hoặc ngày kết thúc lặp lại.
        """
        self = object().__new__(cls)
        for lesson in class_.lessons:
            weekday = lesson.weekday
            event_date = _get_date_from_weekday(start_first_week, weekday)
            event_start_datetime = datetime.combine(event_date, lesson.period.start)
            event_end_datetime = datetime.combine(event_date, lesson.period.end)
            description = f"\
                Mã LHP: {class_.id}\n\
                Giảng viên: {class_.teacher}\
                Nhóm: {lesson.group}\n\
                Số tín chỉ: {class_.subject.credit}\n\
            "

            event = Event()
            event.add('summary', lesson.subject.name)
            event.add('dtstart', event_start_datetime)
            event.add('dtend', event_end_datetime)
            event.add('location', lesson.location)
            event.add('description', description)
            if isinstance(repeat, int):
                event.add('rrule', {'freq': 'weekly', 'count': repeat})
            elif isinstance(repeat, date):
                event.add('rrule', {'freq': 'weekly', 'until': repeat})

            self.append(event)
        return self
    
    def add_alarms(self, alarms: Alarms | list[Alarm]):
        """
        Thêm các lời nhắc vào các sự kiện.

        Args:
            alarms (Alarms | list[Alarm]): Danh sách các lời nhắc.
        """
        for event in self:
            for alarm in alarms:
                event.add_component(alarm)
        return self
    
class Calendar(ICalendar):
    """
    Lớp đại diện cho lịch (calendar).
    """
    def add_events(self, events: Events | list[Event]):
        """
        Thêm các sự kiện vào lịch.

        Args:
            events (Events | list[Event]): Danh sách các sự kiện.
        """
        for event in events:
            self.add_component(event)
        return self
    
    def export_ical_as_str(self) -> str:
        """
        Xuất lịch ra dưới dạng dữ liệu ical.

        Returns:
            str: Chuỗi dữ liệu ical .
        """
        return self.to_ical().decode('utf-8')

    def export_ical(self, location: str, filename: str):
        """
        Xuất lịch ra file .ics.

        Args:
            location (str): Đường dẫn tới thư mục lưu file.
            filename (str): Tên file.

        Returns:
            str: Đường dẫn tới file .ics đã xuất.
        """
        data = self.to_ical()
        location = os.path.abspath(location)
        path = os.path.join(location, f"{filename}.ics")
        with open(path, 'wb') as f:
            f.write(data)
        return path