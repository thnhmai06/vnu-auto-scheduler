import pandas as pd
from bs4 import BeautifulSoup
from bs4.element import Tag, ResultSet
from classes.subject import SimpleClass, DetailedClass, Subject, Lesson, Timetable

PERIOD_REFERENCE_FILEPATH = "../../config/time.csv"
PERIOD_REFERENCE = Timetable(PERIOD_REFERENCE_FILEPATH)

def get_simplified_classes(file_path: str, id_header: str) -> list[SimpleClass]:
    """
    Lấy danh sách các lớp học phần từ file Kết quả Đăng ký học

    Parameters:
        file_path (str): Đường dẫn đến file Kết quả Đăng ký học
        id_header (str): Tên cột chứa Mã Lớp học phần

    Returns:
        list[SimpleClass]: Thông tin các lớp học phần đã đăng ký
    """
    with open(file_path, "r", encoding="utf-8") as file:
        html = file.read()
    soup = BeautifulSoup(html, 'html.parser')
    
    tables: ResultSet[Tag] = soup.find_all('table')
    table: Tag | None = next((tbl for tbl in tables if tbl.find('th', string=id_header)), None)

    if not table:
        return []

    rows: ResultSet[Tag] = table.find_all('tr')
    headers: list[str] = [header_tag.get_text(strip=True) for header_tag in rows[0].find_all('th')]

    # Sử dụng dict để map header với attribute
    header_mapping = {
        "Mã môn học": "subject.id",
        "Môn học": "subject.name", 
        "Lớp môn học": "id"
    }

    class_list: list[SimpleClass] = []
    for row in rows[1:]:
        class_ = SimpleClass()
        for index, cell in enumerate(row.find_all('td')):
            assert isinstance(cell, Tag)
            cell_text = cell.get_text(strip=True)
            header = headers[index]
            
            if header in header_mapping:
                attr = header_mapping[header]
                if "." in attr:
                    obj_name, attr_name = attr.split(".")
                    setattr(getattr(class_, obj_name), attr_name, cell_text)
                else:
                    setattr(class_, attr, cell_text)
                    
        class_list.append(class_)
    return class_list

def _standardize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Chuẩn hóa DataFrame

    Trong dữ liệu có thể chứa các cột trống, và sau các cột đó có thể có dữ liệu không cần thiết.
    Vì vậy ta cần "bo" bảng lại, để dữ liệu chỉ trong phạm vi cần thiết:
    - Xóa các cột nan ở đầu
    - Khi đi từ đầu đến cuối mà phát hiện header cột là nan (tức là đã vượt quá phạm vi dữ liệu), 
    ta sẽ xóa bỏ các cột từ đó trở về sau, bao gồm cả các dữ liệu sau đó (not nan).

    Parameters:
        df (pd.DataFrame): DataFrame cần chuẩn hóa

    Returns:
        pd.DataFrame: DataFrame đã được chuẩn hóa
    """
    isna = df.columns.isna()
    first_notna_index = next((index for index, value in enumerate(isna) if not value), None)
    first_isna_after_notna = next((index for index in range(first_notna_index, len(isna)) if isna[index]), None)

    if first_isna_after_notna is not None:
        df = df.iloc[:, :first_isna_after_notna]
    return df

def get_detailed_classes(file_path: str, id_list: list[str], id_header: str) -> list[DetailedClass]:
    """
    Lấy thông tin chi tiết các lớp học phần

    Parameters:
        file_path (str): Đường dẫn đến file Thời khóa biểu
        id_list (list[str]): Danh sách mã của các lớp học phần cần lấy thông tin
        id_header (str): Tên cột chứa Mã Lớp học phần
        
    Returns:
        list[DetailedClass]: Danh sách chi tiết các lớp học phần
    """
    df = pd.read_excel(file_path, header=None)
    
    header_row_index = next((row_index for row_index, row in df.iterrows() if id_header in row.values), None)
    if header_row_index is None:
        return []

    df.columns = df.iloc[header_row_index]
    df = df.iloc[header_row_index + 1:].reset_index(drop=True)
    df = _standardize_dataframe(df)
    df = df[df[id_header].isin(id_list)]
    if df.empty:
        return []

    classes: dict[str, DetailedClass] = {}
    data: list[dict[str, str]] = df.to_dict(orient="records")
    for lesson in data:
        class_id = lesson[id_header]

        if class_id not in classes:
            class_ = DetailedClass(
                id=class_id,
                subject=Subject(
                    id=lesson["Mã học phần"],
                    name=lesson["Học phần"]
                ),
                teacher=lesson["Giảng viên"]
            )
            classes[class_id] = class_

        classes[class_id].add_lesson(
            Lesson(
                weekday=lesson["Thứ"],
                location=lesson["Giảng đường"],
                group=lesson["Nhóm"],
                period=PERIOD_REFERENCE.reference(lesson["Tiết"])
            )
        )
    
    return list(classes.values())