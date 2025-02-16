from datetime import date
from icalendar import Calendar
from utils.import_ import get_class_list, getFulfilledClass
from utils.schedule import (
    Alarm as AlarmScript,
    Event as EventScript,
    Calendar as CalendarScript
)
from utils.export import ics as export_ics

if __name__ == "__main__":
    # Input
    alarm_list: list[int] = [15, 30, 45]
    file_dang_ky_mon = "../test/ket-qua-dang-ky-mon-hoc.doc"
    header_dang_ky_mon = "Lớp môn học"
    file_thoi_khoa_bieu = "../test/không dư thừa.xlsx"
    header_thoi_khoa_bieu = "Mã LHP"
    start_date = date.today()
    end_date = date(2025, 12, 31)
    
    # Lấy thông tin cột
    class_ids = get_class_list(
        file_path=file_dang_ky_mon, 
        id_header=header_dang_ky_mon
    )
    # print(class_ids)

    # Lấy thông tin các lớp học
    classes_info = getFulfilledClass(
        file_path=file_thoi_khoa_bieu, 
        class_ids=class_ids, 
        header_name=header_thoi_khoa_bieu
    )
    # print(class_info)

    # Tạo lịch
    calendar = Calendar()
    alarms = AlarmScript.create_alarm(alarm_list)
    for class_name, class_info in classes_info.items():
        for lession in class_info:
            event = EventScript.create_event(
                data=lession, 
                name_header="Học phần", 
                day_of_the_week_header="Thứ", 
                start_date=start_date, 
                period_header="Tiết", 
                location_header="Giảng đường",
                loop=end_date
            )
            event = EventScript.import_alarm(event, alarms)
            calendar = CalendarScript.import_event(calendar, event)

    # Xuất lịch
    export_ics(calendar, location="../test", file_name="calendar")