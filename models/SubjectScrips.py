central_script = """
                #centralWidget {{
                border-radius: {}px;
                background-color: white;
            }}
                """
central_script_menu = """
                #centralWidget {
                border-radius: 10px;
                background-color: #e2fffc;
            }
                """

QMenuRighClick = """
QMenu {
    background-color:rgba(28,39,85,220);
    border: 0.5px solid rgb(65,84,133); /* Đường viền cho menu */
    border-radius: 4px; /* Làm tròn viền cho menu */
    color: #d0d4db;
}

QMenu::item {
    padding: 10px 24px; /* Đệm cho các mục menu */
    background-color: transparent; /* Màu nền trong suốt cho các mục menu */
    color: #d0d4db; /* Màu chữ cho các mục menu */
    border-radius: 3px; /* Làm tròn viền cho các mục menu */
    height: 10px; /* Chiều cao của item */
}

QMenu::item:selected {
    background-color: rgb(65,84,133); /* Màu nền khi mục được chọn */
    color: #d0d4db;
    height: 10px; /* Chiều cao của item khi được chọn */
    border-radius: 2px; /* Làm tròn viền cho menu */
    padding: 10px 24px; /* Đệm cho các mục menu */
    font-family: bold;

}
QAction#ActionOtherCopy {
    color: #520066; /* Màu chữ đỏ cho action "Thêm..." */
        }
QMenu::separator {
    height: 0.5px;
    background: #526296;
    margin: 2px 0px 2px 0px;
}

QAction {
    color: #1d2783;
}

QAction:hover {
    background-color: #5a5a5a;
}

QMenu::icon {
    margin-left: 15px;  
}

       """
QMenuRighClickTable = """
QMenu {
    background-color:rgba(28,39,85,200);
    border: 0.5px solid rgb(65,84,133); /* Đường viền cho menu */
    border-radius: 4px; /* Làm tròn viền cho menu */
    color: #d0d4db;
}

QMenu::item {
    padding: 10px 24px; /* Đệm cho các mục menu */
    background-color: transparent; /* Màu nền trong suốt cho các mục menu */
    color: #d0d4db; /* Màu chữ cho các mục menu */
    border-radius: 3px; /* Làm tròn viền cho các mục menu */
    height: 10px; /* Chiều cao của item */
}

QMenu::item:selected {
    background-color: rgb(65,84,133); /* Màu nền khi mục được chọn */
    color: #d0d4db;
    height: 10px; /* Chiều cao của item khi được chọn */
    border-radius: 2px; /* Làm tròn viền cho menu */
    padding: 10px 24px; /* Đệm cho các mục menu */
    font-family: bold;

}

QMenu::separator {
    height: 0.5px;
    background: #526296;
    margin: 2px 0px 2px 0px;
}


QAction {
    color: #1d2783;
}


QAction:hover {
    background-color: #5a5a5a;
}

QMenu::icon {
    margin-left: 15px;  
}

       """


QMenuProfile = """
QMenu {
    background-color:rgba(28,39,85);
    border: 0.5px solid rgb(65,84,133); /* Đường viền cho menu */
    border-radius: 4px; /* Làm tròn viền cho menu */
    color: #d0d4db;
    font-family: bold;
}

QMenu::item {
    padding: 10px 24px; /* Đệm cho các mục menu */
    color: #d0d4db; /* Màu chữ cho các mục menu */
    border-radius: 3px; /* Làm tròn viền cho các mục menu */
    height: 10px; /* Chiều cao của item */
    font-family: bold;
}

QMenu::item:selected {
    background-color: rgb(65,84,133); /* Màu nền khi mục được chọn */
    color: #d0d4db;
    height: 10px; /* Chiều cao của item khi được chọn */
    border-radius: 2px; /* Làm tròn viền cho menu */
    padding: 10px 24px; /* Đệm cho các mục menu */
    font-family: bold;

}
QAction#ActionOtherCopy {
    color: #520066; /* Màu chữ đỏ cho action "Thêm..." */
        }
QMenu::separator {
    height: 0.5px;
    background: #526296;
    margin: 2px 0px 2px 0px;
}

QAction {
    color: #1d2783;
}

QAction:hover {
    background-color: #5a5a5a;
}

QMenu::icon {
    margin-left: 15px;  
}
"""


scripProxyImport = """
QPushButton{
border:none;
border-radius:2px;
background-color:#6065c7;
color: rgb(255, 233, 253);
}
QPushButton:hover{
border:none;
border-radius:3px;
color: rgb(255, 233, 253);
background-color:#6369ce;
}
"""

scripProxyAdd = """
QPushButton{
border:none;
border-radius:2px;
background-color: #29b7a5;
color: rgb(255, 233, 253);
}
QPushButton:hover{
border:none;
border-radius:3px;
color: rgb(255, 233, 253);
background-color: #2bc2ae;
}
"""
scriptButtonStop = """
                    QPushButton{
                    border:none;
                    border-radius:5px;
                    color: rgb(255, 255, 255);
                    border: 1px gray #6bd4c1 ;
                    background-color: rgb(255, 84, 135);
                    }

                    QPushButton:hover{
                    border:none;
                    border-radius:5px;
                    color: rgb(255, 255, 255);
                    border: 1px gray #6bd4c1 ;
                    background-color: rgb(255, 94, 164);
                    }
                    QPushButton:checked{
                    border:none;
                    border-radius:5px;
                    color: rgb(255, 255, 255);
                    border: 1px gray #6bd4c1 ;
                    background-color: rgb(255, 94, 164);
                    }
"""
scriptButtonStart = """
QPushButton{
border:none;
border-radius:5px;
color: rgb(255, 255, 255);
border: 1px gray #6bd4c1 ;
background-color: rgb(100, 198, 180);
}
QPushButton:hover{
border:none;
border-radius:5px;
color: rgb(255, 255, 255);
border: 1px solid  rgb(211, 211, 211);
background-color: rgb(93, 184, 166);
}QPushButton:checked{
border:none;
border-radius:5px;
color: rgb(255, 255, 255);
border: 1px gray #6bd4c1 ;
background-color: rgb(108, 213, 194);
}
"""
