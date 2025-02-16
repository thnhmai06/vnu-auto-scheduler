import pandas as pd
from bs4 import BeautifulSoup
from bs4.element import Tag, ResultSet
from classes.subject import SimplifiedClass, FulfilledClass

def getSimplifiedClass(file_path: str, id_header: str) -> list[SimplifiedClass]:
    """
    Lấy danh sách các lớp học phần từ file Kết quả Đăng ký học

    Parameters:
        file_path (str): Đường dẫn đến file Kết quả Đăng ký học
        id_header (str): Tên cột chứa Mã Lớp học phần

    Returns:
        list[str]: Thông tin các lớp học phần đã đăng ký
    """

    # Parsing file Kết quả đăng ký học
    with open(file_path, "r", encoding="utf-8") as file:
        html = file.read()
    soup = BeautifulSoup(html, 'html.parser')

    # Tìm bảng chứa thông tin đăng ký môn học
    tables: ResultSet[Tag] = soup.find_all('table')
    table = None
    for tbl in tables:
        if tbl.find('th', string=id_header): 
            table = tbl
            break

    # Lấy các hàng của bảng
    rows: ResultSet[Tag] = table.find_all('tr')

    # Lấy tên của các cột (header)
    headers = []
    for header_tag in rows[0].find_all('th'):
        assert isinstance(header_tag, Tag)
        headers.append(header_tag.get_text(strip=True))

    # Tìm vị trí cột Mã lớp học phần
    header_index: int = None
    for index, header in enumerate(headers):
        if header == id_header:
            header_index = index
            break
    if header_index is None:
        return []

    # Điền thông tin các lớp học phần vào list
    class_list = []
    for row in rows[1:]:
        class_ = SimplifiedClass()
        for index, cell in enumerate(row.find_all('td')):
            assert isinstance(cell, Tag)
            cell_text = cell.get_text(strip=True)
            match headers[index]:
                case "Mã môn học":
                    class_.subject.id = cell_text
                case "Môn học":
                    class_.subject.name = cell_text
                case "Số tín chỉ":
                    class_.subject.credit = cell_text
                case "Trạng thái":
                    class_.subject.status = cell_text
                case "Học phí":
                    class_.tuition = int(cell_text.replace(',', '')) / 1000
                case "Lớp môn học":
                    class_.id = cell_text
        class_list.append(class_) 
    return class_list

def _standardizing_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Chuẩn hóa DataFrame

    Trong dữ liệu có thể chứa các cột trống, và sau các cột đó có thể có dữ liệu được đặt tên nhưng dư thừa khác
    Vì vậy ta cần "bo" bảng lại, để dữ liệu chỉ trong phạm vi cần thiết
    - Xóa các cột nan ở đầu
    - Khi đi từ đầu đến cuối mà phát hiện header cột là nan (tức là đã vượt quá phạm vi dữ liệu), 
    ta sẽ cắt bỏ các cột từ đó trở về sau, bao gồm cả các dữ liệu sau đó (not nan).

    Parameters:
        df (pd.DataFrame): DataFrame cần chuẩn hóa

    Returns:
        pd.DataFrame: DataFrame đã được chuẩn hóa
    """
    
    isna = df.columns.isna()

    first_notna_index: int
    for index, value in enumerate(isna):
        if not value:
            first_notna_index = index
            break
        
    first_isna_after_notna: int = None
    for index in range(first_notna_index, len(isna)):
        if isna[index]:
            first_isna_after_notna = index
            break

    if first_isna_after_notna is not None:
        df = df.iloc[:, :first_isna_after_notna]
    return df

# def getFulfilledClass(file_path: str, simplified_classes: list[SimplifiedClass], header_name: str, sheet_name: str | int = 0) -> list[FulfilledClass]:
#     """
#     Lấy thông tin chi tiết các lớp học phần

#     Parameters:
#         file_path (str): Đường dẫn đến file Thời khóa biểu
#         class_ids (list[str]): Danh sách mã của các lớp học phần cần lấy thông tin
#         header_name (str): Tên cột chứa Mã Lớp học phần
#         sheet_name (str | int, optional): Tên hoặc chỉ số của sheet chứa dữ liệu. Mặc định là 0.

#     Returns:
#         dict[str, list[dict[str, str | int]]]: Danh sách các lớp đã được gộp lại theo mã lớp học phần
#     """
#     # Đọc file và tạo DataFrame, nhưng bỏ header đi vì không biết hàng nào chứa header
#     df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
    
#     # Tìm vị trí table mà chứa cột header_name
#     header_row_index = None
#     for row_index, row in df.iterrows():
#         if header_name in row.values:
#             header_row_index = row_index
#             break
    
#     # Đặt cột header
#     df.columns = df.iloc[header_row_index]
#     df = df[header_row_index + 1:]
    
#     # Chuẩn hóa DataFrame
#     df = _standardizing_dataframe(df)

#     # Lọc các lớp học theo class_ids
#     df = df[df[header_name].isin(class_ids)]
    
#     # Chuyển đổi DataFrame thành danh sách
#     class_info: list[dict[str, str | int]] = df.to_dict(orient="records")

#     # Gộp các phần tử có cùng mã lớp học phần thành một list, với key là mã lớp học phần
#     class_info_merged: dict[str, list[dict[str, str | int]]] = {}
#     for class_ in class_info:
#         class_id = class_[header_name]
#         if class_id not in class_info_merged:
#             class_info_merged[class_id] = []
#         class_info_merged[class_id].append(class_)

#     return class_info_merged