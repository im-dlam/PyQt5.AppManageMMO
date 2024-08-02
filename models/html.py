
def note():
    """
    {
        "SQL":{
            1:     ("Danh mục đã tồn tại !",            0),
        -1:     ("Tạo danh mục thành công !",        1),
            200:   ("Xóa thành công danh mục ({}) !",   1),
            200:   ("Thêm thành công !",                1),
        -200:   ("Thêm thất bại !",                  0),
        -300:   ("Vui lòng chọn danh mục khác !",    0)
        },
        "data":{
            -1:    ("Thêm dữ liệu thành công !",        1),
            1:    ("Thêm dữ liệu thất bại !",          0),
            -200:  ("Vui lòng nhập dữ liệu !",          0),
        }

    }
    """


html = {
    "SQL":{
        1:     ("Danh mục đã tồn tại !",            0),
       -1:     ("Tạo danh mục thành công !",        1),
        200:   ("Xóa thành công danh mục ({}) !",   1),
        200:   ("Thêm thành công !",                1),
       -200:   ("Thêm thất bại !",                  0),
       -300:   ("Vui lòng chọn danh mục khác !",    0)
    },
    "data":{
         1:    ("Thêm dữ liệu thành công !",        1),
         -1:    ("Thêm dữ liệu thất bại !",          0),
        -200:  ("Vui lòng nhập dữ liệu !",          0),
        -300:  ("Unsupported Text Vietnamese" ,     0)
    }

}