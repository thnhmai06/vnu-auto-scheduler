from datetime import date
from icalendar import Calendar
from DataImport.ClassIDs import get_ClassIds
from DataImport.ClassInfo import get_ClassInfo
from EventSchedule import (
    Alarm as AlarmScript,
    Event as EventScript,
    Calendar as CalendarScript
)
from Export.Calendar import ics as ics_export

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
    class_ids = get_ClassIds(
        file_path=file_dang_ky_mon, 
        header_name=header_dang_ky_mon
    )
    # print(class_ids)

    # Lấy thông tin các lớp học
    classes_info = get_ClassInfo(
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
    ics_export(calendar, location="../test", file_name="calendar")