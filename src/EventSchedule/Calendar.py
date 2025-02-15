from icalendar import Calendar, Event

def import_event(calendar: Calendar, events: Event | list[Event]) -> Calendar:
    """
    Nhập sự kiện vào lịch

    Parameters:
        calendar (Calendar): Lịch cần nhập sự kiện
        events (Event | list[Event]): Sự kiện cần nhập

    Returns:
        Calendar: Lịch sau khi nhập sự kiện
    """
    if isinstance(events, Event):
        events = [events]
    for event in events:
        calendar.add_component(event)

    return calendar