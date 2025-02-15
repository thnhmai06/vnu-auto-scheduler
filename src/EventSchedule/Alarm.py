from datetime import timedelta
from icalendar import Alarm

def create_alarm(before_list: list[int]) -> list[Alarm]:
    """
    Tạo nhắc nhở cho sự kiện

    Parameters:
        before_list (list[int]): Danh sách thời gian trước khi nhắc nhở

    Returns:
        list[Alarm]: Danh sách đối tượng nhắc nhở đã tạo
    """

    alarm_list: list[Alarm] = []
    for minutes in before_list:
        alarm = Alarm()
        alarm.add('ACTION', 'DISPLAY')
        alarm.add('TRIGGER', timedelta(minutes=-minutes))
        alarm_list.append(alarm)

    return alarm_list