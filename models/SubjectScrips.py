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
    background-color: #ffffff; /* Màu nền cho menu */
    border: 0.5px solid #f2f2f2; /* Đường viền cho menu */
    border-radius: 4px; /* Làm tròn viền cho menu */
    color: #0f2b4b;
}

QMenu::item {
    padding: 10px 24px; /* Đệm cho các mục menu */
    background-color: transparent; /* Màu nền trong suốt cho các mục menu */
    color: #4b69a5; /* Màu chữ cho các mục menu */
    border-radius: 3px; /* Làm tròn viền cho các mục menu */
    height: 10px; /* Chiều cao của item */
}

QMenu::item:selected {
    background-color: #f5edf6; /* Màu nền khi mục được chọn */
    color: #6d43c4;
    height: 10px; /* Chiều cao của item khi được chọn */
    border-radius: 2px; /* Làm tròn viền cho menu */
    padding: 10px 24px; /* Đệm cho các mục menu */
}
QAction#ActionOtherCopy {
    color: #520066; /* Màu chữ đỏ cho action "Thêm..." */
        }
QMenu::separator {
    height: 0.5px;
    background: #e6e6e6;
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
    background-color: #e1e0ff; /* Màu nền cho menu */
    border: 0.5px solid #e4e4ec; /* Đường viền cho menu */
    border-radius: 4px; /* Làm tròn viền cho menu */
    color: #6d43c4;
    font-family: bold;
}

QMenu::item {
    padding: 10px 24px; /* Đệm cho các mục menu */
    background-color: transparent; /* Màu nền trong suốt cho các mục menu */
    color: #4b69a5; /* Màu chữ cho các mục menu */
    border-radius: 3px; /* Làm tròn viền cho các mục menu */
    height: 10px; /* Chiều cao của item */
}

QMenu::item:selected {
    background-color: #ceccff; /* Màu nền khi mục được chọn */
    color: #6d43c4;
    border-radius: 2px; /* Làm tròn viền cho menu */
    padding: 10px 24px; /* Đệm cho các mục menu */
    font-family: bold;
}

QMenu::separator {
    height: 0.5px;
    background: #e6e6e6;
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