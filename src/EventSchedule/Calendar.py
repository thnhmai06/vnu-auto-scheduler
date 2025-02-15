from icalendar import Calendar, Event

def import_to_calendar(calendar: Calendar, event_list: list[Event]) -> Calendar:
    """
    Nhập danh sách sự kiện vào lịch

    Args:
        calendar (Calendar): Lịch cần nhập sự kiện
        event_list (list[Event]): Danh sách sự kiện cần nhập

    Returns:
        Calendar: Lịch sau khi nhập sự kiện
    """
    for event in event_list:
        calendar.add_component(event)

    return calendar