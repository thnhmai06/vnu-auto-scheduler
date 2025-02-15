from DataImport.ClassIDs import get_ClassIds
from DataImport.ClassInfo import get_ClassInfo
from TimeCompare import TIME

if __name__ == "__main__":
    # Lấy thông tin cột
    class_ids = get_ClassIds(file_path="../test/ket-qua-dang-ky-mon-hoc.doc", header_name="Lớp môn học")
    # print(class_ids)

    # Lấy thông tin các lớp học
    class_info = get_ClassInfo(file_path="../test/có dư thừa.xlsx", class_ids=class_ids, header_name="Mã LHP")
    # print(class_info)
