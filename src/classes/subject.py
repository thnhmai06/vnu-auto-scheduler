import re
import pandas as pd
from datetime import time, datetime, date, timedelta
from dataclasses import dataclass, field

@dataclass
class Subject:
    """
    Một môn học.
    
    Attributes:
        id (str): Mã môn học.
        name (str): Tên môn học.
    """
    id: str
    name: str

@dataclass
class Period:
    """
    Khoảng thời gian học liên tiếp cùng một môn. (ví dụ: 1, 1-3)
    
    Attributes:
        start (time): Thời gian bắt đầu.
        end (time): Thời gian kết thúc.
    """
    start: time
    end: time

    def __repr__(self):
        return f"{self.start.strftime('%H:%M')} -> {self.end.strftime('%H:%M')}" if self.start else super().__repr__()

    def delta(self) -> timedelta:
        """
        Tính toán khoảng thời gian sẽ học.
        
        Returns:
            timedelta: Khoảng thời gian giữa thời gian bắt đầu và kết thúc.
        
        Raises:
            ValueError: Nếu start hoặc end là None
        """
        if not (self.start and self.end):
            raise ValueError("start and end time must not be None")
        
        start_dt = datetime.combine(date.today(), self.start)
        end_dt = datetime.combine(date.today(), self.end)
        return end_dt - start_dt

class Timetable(dict[int, Period]):
    """
    Thời gian học tập và giảng dạy.

    Attributes:
        file (str): Đường dẫn tới file CSV chứa dữ liệu tham chiếu.
    """
    file: str

    def __init__(self, file_path: str):
        """
        Tham chiếu tiết học từ file.
        
        Args:
            file_path (str): Đường dẫn tới file CSV chứa dữ liệu tham chiếu.
        """
        NUM_HEADER = "num"
        START_HEADER = "start"
        END_HEADER = "end"
        TIME_FORMAT = "%H:%M:%S"
    
        df = pd.read_csv(file_path)

        self.file = file_path
        for index, row in df.iterrows():
            num = int(row[NUM_HEADER])
            start_time = datetime.strptime(row[START_HEADER], TIME_FORMAT).time()
            end_time = datetime.strptime(row[END_HEADER], TIME_FORMAT).time()
            self[num] = Period(start=start_time, end=end_time)

    def reference(self, period: str) -> Period:
        """
        Tham chiếu thời gian tiết học từ chuỗi định dạng.
        
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

    def reload(self):
        """
        Tải lại dữ liệu từ file.
        """
        self.__init__(self.file)

@dataclass
class Lesson:
    """
    Một buổi học.
    
    Attributes:
        weekday (int): Thứ của tuần ở dạng 0-based (0: Thứ 2, 1: Thứ 3, ..., 6: Chủ nhật).
        period (Period): Thời gian buổi học.
        location (str): Giảng đường.
        group (str): Nhóm.
    """
    weekday: int
    period = Period()
    location: str
    group: str

    def __post_init__(self):
        if isinstance(self.weekday, str):
            self.weekday = 6 if self.weekday == "CN" else int(self.weekday) - 2

    def __repr__(self):
        day_of_week = ["Thứ hai", "Thứ ba", "Thứ tư", "Thứ năm", "Thứ sáu", "Thứ bảy", "Chủ nhật"]
        return f"({day_of_week[self.weekday]}) {self.period.__repr__()}" if self.period else super().__repr__()

@dataclass
class SimpleClass:
    """
    Lớp học đã đăng kí trên cổng Đăng kí môn.

    Thông tin được lấy từ file **Kết quả đăng ký học**.
    
    Attributes:
        id (str): Mã lớp học.
        subject (Subject): Môn học.
    """
    id: str
    subject = Subject()

@dataclass
class DetailedClass(SimpleClass):
    """
    Lớp học đối chiếu từ Thời khóa biểu.

    Thông tin được lấy file **Thời khóa biểu** do nhà trường gửi.
    
    Attributes:
        lessons (list[Lesson]): Danh sách các buổi học.
        teacher: str: Tên giảng viên.
    """
    lessons: list[Lesson] = field(default_factory=list)
    teacher: str

    def __repr__(self):
        return f"{self.id} ({len(self.lessons)})" if len(self.lessons) > 0 else super().__repr__()
    
    def add_lesson(self, lesson: Lesson) -> None:
        """
        Thêm một buổi học vào danh sách các buổi học.
        
        Args:
            lesson (Lesson): Buổi học cần thêm.
            
        Returns:
            None
        """
        self.lessons.append(lesson)