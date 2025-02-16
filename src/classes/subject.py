import re
import pandas as pd
from datetime import time

class Subject:
    """
    Lớp đại diện cho một môn học.
    
    Attributes:
        id (str): Mã môn học.
        name (str): Tên môn học.
        credit (int): Số tín chỉ.
        status (str): Trạng thái đăng ký.
    """
    id: str
    name: str
    credit: int
    status: str

    def __new__(cls, id: str = None, name: str = None, 
                credit: int = None, status: str = None):
        """  
        Args:
            id (str, optional): Mã môn học.
            name (str, optional): Tên môn học.
            credit (int, optional): Số tín chỉ.
            status (str, optional): Trạng thái đăng ký.
        """
        self = super().__new__(cls)
        self.id = id
        self.name = name
        self.credit = credit
        self.status = status
        return self
    
    def __repr__(self):
        return self.id or super().__repr__()

class Period:
    """
    Lớp đại diện cho một thời gian học.
    
    Attributes:
        start (time): Thời gian bắt đầu.
        end (time): Thời gian kết thúc.
    """
    start: time
    end: time

    def __new__(cls, start: time = None, end: time = None):
        """     
        Args:
            start (time, optional): Thời gian bắt đầu.
            end (time, optional): Thời gian kết thúc.
        """
        self = super().__new__(cls)
        self.start = start
        self.end = end
        return self
        
    def __repr__(self):
        return f"{self.start.strftime('%H:%M')} -> {self.end.strftime('%H:%M')}" if self.start else super().__repr__()

    def delta(self):
        """
        Tính toán khoảng thời gian của tiết học.
        
        Returns:
            timedelta: Khoảng thời gian giữa thời gian kết thúc và thời gian bắt đầu.
        """
        return self.end - self.start
    
class PeriodReference(dict[int, Period]):
    """
    Lớp đại diện cho tham chiếu từ Tiết học -> Period.
    """
    def __init__(self, file_path: str):
        """
        Tham chiếu tiết học từ file.
        
        Args:
            file_path (str): Đường dẫn tới file Excel chứa dữ liệu tham chiếu.
        """
        df = pd.read_excel(file_path, sheet_name=0, usecols="A:C")
        
        PERIOD_NUM_HEADER = "Tiết"
        START_HEADER = "Bắt đầu"
        END_HEADER = "Kết thúc"
    
        for index, row in df.iterrows():
            period_number = row[PERIOD_NUM_HEADER]
            start_time = row[START_HEADER]
            end_time = row[END_HEADER]
            self[period_number] = Period(start=start_time, end=end_time)

    def reference(self, period: str):
        """
        Tham chiếu tiết học từ chuỗi định dạng.
        
        Args:
            period (str): Chuỗi định dạng tiết học (ví dụ: "1-3").
        
        Returns:
            Period: Đối tượng Period tương ứng.
        """
        PATTERN = r"\d+(-\d+)?"
        match = re.search(PATTERN, period)
        period = match.group()

        if "-" in period:
            start_period_num, end_period_num = map(int, period.split("-"))
        else:
            start_period_num = end_period_num = int(period)

        return Period(self[start_period_num].start, self[end_period_num].end)

class Lesson:
    """
    Lớp đại diện cho một buổi học.
    
    Attributes:
        weekday (int): Thứ của tuần ở dạng 0-based (0: Thứ 2, 1: Thứ 3, ..., 6: Chủ nhật).
        subject (Subject): Môn học.
        period (Period): Thời gian buổi học.
        location (str): Giảng đường.
        group (str): Nhóm.
    """
    weekday: int
    subject: Subject
    period: Period
    location: str
    group: str

    def __new__(cls, weekday: int = None, subject: Subject = None, 
                period: Period = None, location: str = None, group: str = None):
        """
        Args:
            weekday (int, optional): Thứ của tuần ở dạng 0-based (0: Thứ 2, 1: Thứ 3, ..., 6: Chủ nhật).
            subject (Subject, optional): Môn học.
            period (Period, optional): Thời gian buổi học.
            location (str, optional): Giảng đường.
            group (str, optional): Nhóm.
        """
        self = super().__new__(cls)
        self.weekday = weekday
        self.subject = subject
        self.period = period
        self.location = location
        self.group = group
        return self
    
    def __repr__(self):
        day_of_week = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ nhật"]
        return f"{self.subject.id} ({day_of_week[self.weekday]})" if self.period else super().__repr__()

class SimplifiedClass:
    """
    Lớp đại diện cho một lớp học chưa đầy đủ thông tin.

    Thông tin được cung cấp sẽ từ file **Kết quả đăng ký học**.
    
    Attributes:
        id (str): Mã lớp học.
        subject (Subject): Môn học.
        teacher (str): Giáo viên.
        tuition (int): Học phí. (nghìn VNĐ)
    """
    id: str
    subject: Subject
    teacher: str
    tuition: int

    def __new__(cls, id: str = None, subject: Subject = None, 
                teacher: str = None, tuition: int = None):
        """   
        Args:
            id (str, optional): Mã lớp học.
            subject (Subject, optional): Môn học.
            teacher (str, optional): Giáo viên.
            tuition (int, optional): Học phí. (nghìn VNĐ)
        """
        self = super().__new__(cls)
        self.id = id
        self.subject = subject
        self.teacher = teacher
        self.tuition = tuition
        return self
    
    def __repr__(self):
        return f"{self.id}" if self.id else super().__repr__()

class FulfilledClass(SimplifiedClass):
    """
    Lớp đại diện cho một lớp học đầy đủ thông tin.

    Thông tin được cung cấp sẽ từ file **Thời khóa biểu** do nhà trường gửi.
    
    Attributes:
        lessons (list[Lesson]): Danh sách các buổi học.
        periods (list[Period]): Danh sách các tiết học.
    """
    object().__init__()
    lessons: list[Lesson]

    def __new__(cls, id: str = None, subject: Subject = None, teacher: str = None, 
                lessons: list[Lesson] | Lesson = []):
        """
        Khởi tạo một đối tượng FulfilledClass mới.
        
        Args:
            id (str, optional): Mã lớp học.
            subject (Subject, optional): Môn học.
            teacher (str, optional): Giáo viên.
            lessons (list[Lesson] | Lesson, optional): Danh sách các buổi học.
        """
        self = super().__new__(cls)
        self.id = id
        self.subject = subject
        self.teacher = teacher
        if isinstance(lessons, Lesson):
            self.lessons = [lessons]
        else:
            self.lessons = lessons
        return self
    
    def __repr__(self):
        return f"{self.id} ({len(self.lessons)})" if len(self.lessons)>0 else super().__repr__()