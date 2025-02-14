import pandas as pd

def get_ClassInfo(file_path: str, class_ids: list[str], header_name: str) -> list[dict[str, str | int]]:
    """
    Lấy thông tin các lớp học

    Args:
        file_path (str): Đường dẫn đến file Thời khóa biểu
        class_ids (list[str]): Danh sách mã của các lớp học phần cần lấy thông tin
        header_name (str): Tên cột chứa Mã Lớp học phần

    Returns:
        list[dict[str, str | int]]: Danh sách thông tin của các lớp
    """
    
    # Đọc file và tạo DataFrame
    df = pd.read_excel(file_path, sheet_name=0, header=None)
    
    # Tìm vị trí table mà chứa cột header_name
    header_row_index = None
    for i, row in df.iterrows():
        if header_name in row.values:
            header_row_index = i
            break
    
    if header_row_index is None:
        raise ValueError(f"Header '{header_name}' not found in the file.")
    
    # Đặt cột header
    df.columns = df.iloc[header_row_index]
    df = df[header_row_index + 1:]
    
    # Lọc các lớp học theo class_ids
    filtered_df = df[df[header_name].isin(class_ids)]
    
    # Chuyển đổi DataFrame thành danh sách các từ điển
    class_info = filtered_df.to_dict(orient="records")

    return class_info