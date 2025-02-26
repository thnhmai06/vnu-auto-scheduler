from flask import jsonify, current_app as app, Request
from src.utils.getClass import get_simplified_classes, get_detailed_classes

def handle_request(request: Request, args: dict, argv: dict):
    """
    Lấy thông tin các tiết học từ file đăng ký và thời khóa biểu.

    Args:
        request (Request): Request object từ Flask
        args (dict): Query parameters
        argv (dict): Request body (JSON)

    Returns:
        Response: JSON response với các trường hợp:
            - 200: Thành công
                {
                    "classes": [
                        {
                            "id": str,  # Mã lớp học phần
                            "subject": {
                                "id": str,  # Mã môn học
                                "name": str  # Tên môn học
                            },
                            "teacher": str,  # Tên giảng viên
                            "lessons": [
                                {
                                    "weekday": int,  # 0-6 (0: Thứ 2, 6: Chủ nhật)
                                    "period": str,  # Thời gian học (VD: "7:00 -> 9:00")
                                    "location": str,  # Địa điểm học
                                    "group": str,  # Nhóm học
                                    "is_practical": bool  # Có phải tiết TH/BT không
                                }
                            ]
                        }
                    ]
                }
            - 404: Không tìm thấy dữ liệu
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
        registered_file = argv.get('registered_file')
        schedule_file = argv.get('schedule_file')
        id_header = argv.get('id_header', 'Lớp môn học')
        
        # Lấy danh sách lớp học từ file đăng ký
        simple_classes = get_simplified_classes(registered_file, id_header)
        if not simple_classes:
            return jsonify({'error': 'Không tìm thấy lớp học nào'}), 404
            
        # Lấy thông tin chi tiết các lớp từ TKB
        detailed_classes = get_detailed_classes(schedule_file, [c.id for c in simple_classes], id_header)
        if not detailed_classes:
            return jsonify({'error': 'Không tìm thấy thông tin chi tiết lớp học'}), 404

        # Tạo response chứa thông tin các tiết học
        lessons_info = []
        for class_ in detailed_classes:
            class_info = {
                'id': class_.id,
                'subject': {
                    'id': class_.subject.id,
                    'name': class_.subject.name
                },
                'teacher': class_.teacher,
                'lessons': []
            }
            
            for lesson in class_.lessons:
                lesson_info = {
                    'weekday': lesson.weekday,
                    'period': str(lesson.period),
                    'location': lesson.location,
                    'group': lesson.group,
                    'is_practical': any(keyword in lesson.group for keyword in ["TH", "BT"])
                }
                class_info['lessons'].append(lesson_info)
                
            lessons_info.append(class_info)
            
        return jsonify({'classes': lessons_info})
        
    except Exception as e:
        app.logger.error(f"Error getting lessons info: {str(e)}")
        return jsonify({'error': 'An internal error has occurred!'}), 500