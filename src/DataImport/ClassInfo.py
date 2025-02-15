import pandas as pd
from numpy import ndarray

def standardizing(df: pd.DataFrame) -> pd.DataFrame:
    """
    Chuẩn hóa DataFrame

    Trong dữ liệu có thể chứa các cột trống, và sau các cột đó có thể có dữ liệu được đặt tên nhưng dư thừa khác
    Vì vậy ta cần "bo" bảng lại, để dữ liệu chỉ trong phạm vi cần thiết
    - Xóa các cột nan ở đầu
    - Khi đi từ đầu đến cuối mà phát hiện header cột là nan (tức là đã vượt quá phạm vi dữ liệu), 
    ta sẽ cắt bỏ các cột từ đó trở về sau, bao gồm cả các dữ liệu sau đó (not nan).

    Args:
        df (pd.DataFrame): DataFrame cần chuẩn hóa

    Returns:
        pd.DataFrame: DataFrame đã được chuẩn hóa
    """
    
    isna: ndarray = df.columns.isna()

    first_notna_index: int
    first_isna_after_notna: int

    for index, value in enumerate(isna):
        if not value:
            first_notna_index = index
            break

    for index in range(first_notna_index, len(isna)):
        if isna[index]:
            first_isna_after_notna = index
            break

    if first_isna_after_notna is not None:
        df = df.iloc[:, :first_isna_after_notna]

    return df

def get_ClassInfo(file_path: str, class_ids: list[str], header_name: str, sheet_name: str | int = 0) -> list[dict[str, str | int]]:
    """
    Lấy thông tin các lớp học

    Args:
        file_path (str): Đường dẫn đến file Thời khóa biểu
        class_ids (list[str]): Danh sách mã của các lớp học phần cần lấy thông tin
        header_name (str): Tên cột chứa Mã Lớp học phần
        sheet_name (str | int, optional): Tên hoặc chỉ số của sheet chứa dữ liệu. Mặc định là 0.

    Returns:
        list[dict[str, str | int]]: Danh sách thông tin của các lớp
    """
    
    # Đọc file và tạo DataFrame, nhưng bỏ header đi vì không biết hàng nào chứa header
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
    
    # Tìm vị trí table mà chứa cột header_name
    header_row_index = None
    for row_index, row in df.iterrows():
        if header_name in row.values:
            header_row_index = row_index
            break
    
    if header_row_index is None:
        raise ValueError(f"Header '{header_name}' not found in the file.")
    
    # Đặt cột header
    df.columns = df.iloc[header_row_index]
    df = df[header_row_index + 1:]
    
    # Lọc các lớp học theo class_ids
    df = df[df[header_name].isin(class_ids)]
    
    # Chuẩn hóa DataFrame
    df = standardizing(df)
    
    # Đảm bảo các cột của DataFrame là duy nhất (thêm hậu tố cho cột bị trùng lặp)
    df.columns = pd.Series(df.columns).apply(
        lambda x: x if pd.Series(df.columns).tolist().count(x) == 1 
        else f"{x}_{pd.Series(df.columns).tolist().count(x)}"
    )
    
    # Chuyển đổi DataFrame thành list dict
    class_info = df.to_dict(orient="records")

    return class_info