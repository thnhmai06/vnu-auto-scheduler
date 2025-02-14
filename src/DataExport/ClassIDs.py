from bs4 import BeautifulSoup
from bs4.element import Tag, ResultSet

def get_ClassIds(file_path: str, header_name: str) -> list[str]:
    """
    Lấy tất cả dữ liệu ở trong cột có tên header_name

    Args:
        file_path (str): Đường dẫn đến file Đăng ký học
        header_name (str): Tên cột cần lấy dữ liệu

    Returns:
        list[str]: Danh sách dữ liệu
    """

    # Parsing file
    with open(file_path, "r", encoding="utf-8") as file:
        html = file.read()
    soup = BeautifulSoup(html, 'html.parser')

    # Tìm bảng chứa thông tin đăng ký môn học
    tables: ResultSet[Tag] = soup.find_all('table')
    table = None
    for tbl in tables:
        if tbl.find('th', string=header_name): 
            table = tbl
            break

    # Lấy tất cả các hàng của bảng
    rows: ResultSet[Tag] = table.find_all('tr')

    # Lấy tên các cột
    headers = []
    for header_tag in rows[0].find_all('th'):
        assert isinstance(header_tag, Tag)

        headers.append(header_tag.get_text(strip=True))

    # Tìm chỉ số của cột có tên là header_name
    header_index: int = None
    for index, header in enumerate(headers):
        if header == header_name:
            header_index = index
            break

    if header_index is None:
        return []

    # Lấy dữ liệu từ cột tương ứng
    column_data: list[str] = []
    for row in rows[1:]:
        cells: ResultSet[Tag] = row.find_all('td')
        if len(cells) > header_index:  # Bỏ qua các hàng không có đủ cột
            cell = cells[header_index].get_text(strip=True)
            if cell:  # Bỏ qua các dữ liệu trống
                column_data.append(cell)

    return column_data
        