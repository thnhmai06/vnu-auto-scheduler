import icalendar

def create_event(data: dict, title_header: str, day_of_the_week_header: str, period_header: str, location_header: str) -> icalendar.Event:
    """
    Create an iCalendar event from a dictionary.
    """
    event = icalendar.Event()
    
    return event