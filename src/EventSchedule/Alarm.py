from datetime import timedelta
from icalendar import Alarm

def create_alarm(before_list: list[int]) -> Alarm:
    """
    Tạo nhắc nhở cho sự kiện

    Args:
        before_list (list[int]): Danh sách thời gian trước khi nhắc nhở

    Returns:
        icalendar.Alarm: Đối tượng nhắc nhở đã tạo
    """
    alarm = Alarm()
    alarm.add('ACTION', 'DISPLAY')
    for minutes in before_list:
        alarm.add('TRIGGER', timedelta(minutes=-minutes))
    # alarm.add('DESCRIPTION', 'Reminder')
    return alarm