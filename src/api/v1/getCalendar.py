from datetime import datetime, timedelta
from flask import jsonify, Request
from classes.calendar import Calendar, Events, Alarms
from utils.getClass import get_simplified_classes, get_detailed_classes

def handle_request(request: Request, args: dict, argv: dict):
    """
    Tạo file lịch iCalendar từ thông tin đăng ký học.

    Args:
        request (Request): Request object từ Flask
        args (dict): Query parameters
        argv (dict): Request body (JSON) với các trường:
            registered_file (str): Đường dẫn đến file đăng ký học
            schedule_file (str): Đường dẫn đến file thời khóa biểu
            start_date (str): Ngày bắt đầu (YYYY-MM-DD)
            repeat (int | str, optional): Số tuần hoặc ngày kết thúc (YYYY-MM-DD). Mặc định: 15
            remind_before (list[int], optional): Danh sách số phút nhắc trước. Mặc định: [15]
            practical_delay (int, optional): Số tuần delay tiết TH/BT. Mặc định: 1
            practical_groups (list[str], optional): Danh sách nhóm TH/BT cần delay. Mặc định: []

    Returns:
        Response: Các trường hợp:
            - 200: File iCalendar (.ics)
                Content-Type: text/calendar
                Content-Disposition: attachment; filename=calendar.ics
            - 400: Thiếu tham số hoặc không tìm thấy dữ liệu
                {
                    "error": str  # Thông báo lỗi
                }
            - 500: Lỗi server
                {
                    "error": str  # Thông báo lỗi
                }

    Raises:
        Exception: Khi có lỗi xảy ra trong quá trình xử lý
    """
    try:
        # Kiểm tra các tham số bắt buộc
        required_params = ['registered_file', 'schedule_file', 'start_date']
        missing_params = [param for param in required_params if param not in argv]
        if missing_params:
            return jsonify({
                'error': f'Thiếu các tham số: {", ".join(missing_params)}'
            }), 400

        # Lấy và kiểm tra các tham số
        registered_file = argv['registered_file']
        schedule_file = argv['schedule_file']
        start_date = datetime.strptime(argv['start_date'], '%Y-%m-%d').date()
        
        # Tham số tùy chọn
        repeat = argv.get('repeat', 15)
        if isinstance(repeat, str):
            repeat = datetime.strptime(repeat, '%Y-%m-%d').date()
            
        remind_before = argv.get('remind_before', [15])
        if not isinstance(remind_before, list):
            remind_before = [remind_before]
            
        practical_delay = argv.get('practical_delay', 1)  # Mặc định delay 1 tuần
        practical_groups = argv.get('practical_groups', [])  # Danh sách nhóm TH/BT cần delay

        # Lấy danh sách lớp học
        simple_classes = get_simplified_classes(
            file_path=registered_file,
            id_header="Lớp môn học"
        )
        if not simple_classes:
            return jsonify({
                'error': 'Không tìm thấy thông tin lớp học trong file đăng ký'
            }), 400

        class_ids = [class_.id for class_ in simple_classes]
        detailed_classes = get_detailed_classes(
            file_path=schedule_file,
            id_list=class_ids,
            id_header="Mã lớp"
        )
        if not detailed_classes:
            return jsonify({
                'error': 'Không tìm thấy thông tin lớp học trong file thời khóa biểu'
            }), 400

        # Tạo lịch
        calendar = Calendar()
        for class_ in detailed_classes:
            # Tách thành 2 danh sách: tiết lý thuyết và tiết TH/BT
            theory_lessons = []
            practical_lessons = []
            
            for lesson in class_.lessons:
                # Kiểm tra nếu là tiết TH/BT dựa theo nhóm được chọn
                if lesson.group in practical_groups:
                    practical_lessons.append(lesson)
                else:
                    theory_lessons.append(lesson)
            
            # Tạo events cho tiết lý thuyết
            if theory_lessons:
                class_theory = class_.__class__(
                    id=class_.id,
                    subject=class_.subject,
                    teacher=class_.teacher
                )
                class_theory.lessons = theory_lessons
                
                theory_events = Events(
                    class_=class_theory,
                    start_first_week=start_date,
                    repeat=repeat
                )
                if remind_before:
                    theory_events.add_alarms(Alarms(remind_before))
                calendar.add_events(theory_events)
            
            # Tạo events cho tiết TH/BT với delay
            if practical_lessons:
                class_practical = class_.__class__(
                    id=class_.id,
                    subject=class_.subject,
                    teacher=class_.teacher
                )
                class_practical.lessons = practical_lessons
                
                practical_start = start_date + timedelta(weeks=practical_delay)
                practical_events = Events(
                    class_=class_practical,
                    start_first_week=practical_start,
                    repeat=repeat
                )
                if remind_before:
                    practical_events.add_alarms(Alarms(remind_before))
                calendar.add_events(practical_events)

        # Trả về dữ liệu iCal
        return calendar.export_ical_as_str(), 200, {
            'Content-Type': 'text/calendar',
            'Content-Disposition': 'attachment; filename=calendar.ics'
        }

    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500 