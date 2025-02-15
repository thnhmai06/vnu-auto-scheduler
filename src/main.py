from DataImport.ClassIDs import get_ClassIds
from DataImport.ClassInfo import get_ClassInfo
from TimeCompare import TIME

if __name__ == "__main__":
    # Input
    alarm_list: list[int] = [15, 30, 45]
    file_dang_ky_mon = "../test/ket-qua-dang-ky-mon-hoc.doc"
    header_dang_ky_mon = "Lớp môn học"
    file_thoi_khoa_bieu = "../test/có dư thừa.xlsx"
    header_thoi_khoa_bieu = "Mã LHP"
    
    # Lấy thông tin cột
    class_ids = get_ClassIds(
        file_path=file_dang_ky_mon, 
        header_name=header_dang_ky_mon
    )
    # print(class_ids)

    # Lấy thông tin các lớp học
    class_info = get_ClassInfo(
        file_path=file_thoi_khoa_bieu, 
        class_ids=class_ids, 
        header_name=header_thoi_khoa_bieu
    )
    # print(class_info)

    print(2)
