from DataExport.ClassIDs import get_ClassIds
from DataExport.ClassInfo import get_ClassInfo

if __name__ == "__main__":
    # Lấy thông tin cột
    class_ids = get_ClassIds(file_path="", header_name="Lớp môn học")
    # print(class_ids)

    # Lấy thông tin các lớp học
    class_info = get_ClassInfo(file_path="", class_ids=class_ids, header_name="Mã LHP")
    # print(class_info)
