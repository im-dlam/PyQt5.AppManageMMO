from main import *
from models import *
class FolderItemWidget(QWidget):
    def __init__(self, folder_name,widgets, parent=None):
        super().__init__(parent)
        
        self.widgets  =  widgets
        self.folder_name = folder_name
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        
        self.label = QLabel(folder_name)
        self.label.setStyleSheet("color: white;")
        layout.addWidget(self.label)
        
        layout.addStretch()  # This pushes the three-dot button to the far right
        
        self.options_button = QPushButton()
        icon4 = QIcon()
        icon4.addPixmap(QPixmap(":/icons/png/icons8-ellipsis-48.png"), QIcon.Normal, QIcon.Off)
        self.options_button.setIcon(icon4)
        self.options_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.options_button.setFixedSize(30, 30)
        self.options_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                text-align: center;
                font-size: 16px;
                                          
            }
            QPushButton::menu-indicator {
                image: none;  /* Hide the arrow icon */
            }
        """)
        layout.addWidget(self.options_button)

        # Create a QMenu for the options button
        self.options_menu = QMenu()
        self.options_menu.setStyleSheet("""
            QMenu {
    background-color:#242e5d;
    border: 0.5px solid rgb(65,84,133); /* Đường viền cho menu */
    border-radius: 4px; /* Làm tròn viền cho menu */
    color: #d0d4db;
    font-family: bold;
}

QMenu::item {
    padding: 10px 24px; /* Đệm cho các mục menu */
    color: #d0d4db; /* Màu chữ cho các mục menu */
    border-radius: 3px; /* Làm tròn viền cho các mục menu */
    height: 7px; /* Chiều cao của item */
    font-family: bold;
}

QMenu::item:selected {
    background-color: rgb(65,84,133); /* Màu nền khi mục được chọn */
    color: #d0d4db;
    height: 7px; /* Chiều cao của item khi được chọn */
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
        """)
        
        # Add a delete action to the menu
        delete_action = self.options_menu.addAction("Delete")
        delete_action.triggered.connect(self.delete_folder_qlist)

        # Connect the options button to show the menu
        self.options_button.setMenu(self.options_menu)
    def delete_folder_qlist(self):

        # Get the QListWidget that contains this item
        list_widget = self.parentWidget().parentWidget()

        # Find the QListWidgetItem that corresponds to this FolderItemWidget
        if self.folder_name == 'ALL':return
        for i in range(list_widget.count()):
            item = list_widget.item(i)
            # In ra văn bản của item
            if list_widget.itemWidget(item) is self:
                # Remove the QListWidgetItem from the QListWidget
                list_widget.takeItem(i)
                break
        self.removeName()

    # xóa table
    def removeName(self):
        SubjectSQL.DeleteTableName(self , name=self.folder_name,widgets=self.widgets)
        SubjectProcessFile.LoadNameTabelSQL(self , self.widgets)
        self.widgets.TableManage.clear()
        # tạo mới horizon
        QTableTools.SubjectNewHorizontalHeader(self , self.widgets)


        QTableTools.SubjectHiddenColumn(self , self.widgets)

        #######################################################################################
        # giới hạn chiều rộng của cột
        QTableTools.SetColumnWidthTableWidget(self , self.widgets)

class CreateFolderWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        
        self.add_button = QPushButton()
        self.add_button.setCursor(QCursor(Qt.PointingHandCursor))
        icon4 = QIcon()
        icon4.addPixmap(QPixmap(":/icons/png/icons8-add-48.png"), QIcon.Normal, QIcon.Off)
        self.add_button.setIcon(icon4)
        self.add_button.setFixedSize(30, 30)
        self.add_button.setStyleSheet("""
                QPushButton{
                background-color:#242e5d;
                border:none;
                color: rgb(203, 215, 255);
                }
                QPushButton:hover{
                background-color:#474d82;
                border-radius:3px;
                }
                QPushButton::menu-indicator {
                image: none;  /* Hide the arrow icon */
            }
        """)
        layout.addWidget(self.add_button)
        
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("Add folder")
        self.line_edit.setStyleSheet("""
            QLineEdit {
                background-color: transparent;
                color: white;
                border: none;
                padding: 5px;
            }
            QLineEdit:focus {
                border-bottom: 1px solid #baaaef;
            }
        """)
        layout.addWidget(self.line_edit)

class CustomMenuFolder(QMenu):
    def __init__(self, widgets):
        super().__init__()  # Không truyền tham số parent vào hàm khởi tạo lớp cơ sở
        self.widgets =  widgets

        item   = [widgets.ComboboxFile.itemText(i) for i in range(widgets.ComboboxFile.count())]
        # Create a QListWidget to contain the list of folders
        self.folder_list_widget = QListWidget()
        self.folder_list_widget.clear()
        self.folder_list_widget.setFocusPolicy(Qt.NoFocus)
        self.folder_list_widget.setStyleSheet("""
            QListWidget {
                background-color: #242e5d;
                border: none;
            }
            QScrollBar:horizontal {
                border: none;
               background-color: rgb(150, 173, 232);
                height: 5px;
                margin: 0px 0px 0 0px;
                border-radius: 5px;
            }
            QScrollBar:horizontal {
                border: none;
			background-color: rgb(150, 173, 232);

                height: 3px;
                margin: 0px 0px 0 0px;
                border-radius: 5px;
            }
            QScrollBar::handle:horizontal {
				 background-color: rgb(105, 122, 163);
			   
                min-width: 2px;
                border-radius: 5px;
            }
            QScrollBar::add-line:horizontal {
                border: none;
                width: 0px;
                background-color: none;
            }
            QScrollBar::sub-line:horizontal {
                border: none;
                background: none;
                width: 0px;
            }
            QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal {
                background: none;
            }
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: none;
            }
            QScrollBar:vertical {
                border: none;
				background-color: rgb(105, 122, 163);

                width: 3px;
                margin: 0px 0 0px 0;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background-color: rgb(150, 173, 232);
                min-height: 5px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical {
                border: none;
                background: none;
                height: 0px;
            }
            QScrollBar::sub-line:vertical {
                border: none;
                background: none;
                height: 0px;
            }
            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                background: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)

        
        # Add some folder items to the list
        for folder_name in item:
            self.add_folder(folder_name)

        folder_list_action = QWidgetAction(self)
        folder_list_action.setDefaultWidget(self.folder_list_widget)
        self.addAction(folder_list_action)

        # Add a spacer to push the add folder option to the bottom
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        spacer_action = QWidgetAction(self)
        spacer_action.setDefaultWidget(spacer)
        self.addAction(spacer_action)

        # Add the create folder widget at the bottom
        self.create_folder_widget = CreateFolderWidget()
        create_folder_action = QWidgetAction(self)
        create_folder_action.setDefaultWidget(self.create_folder_widget)
        self.addAction(create_folder_action)

        # Connect the add_button to the folder creation function
        self.create_folder_widget.add_button.clicked.connect(self.create_folder)

        # CSS Styling for the QMenu
        self.setStyleSheet("""
            QMenu {
    background-color:#242e5d;
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
        """)

    def add_folder(self, folder_name):
        item = QListWidgetItem()
        item_widget = FolderItemWidget(folder_name , self.widgets)
        item.setSizeHint(item_widget.sizeHint())
        self.folder_list_widget.addItem(item)
        self.folder_list_widget.setItemWidget(item, item_widget)

    def create_folder(self):
        self.folder_name = self.create_folder_widget.line_edit.text().strip()
        if self.folder_name:
            self.add_folder(self.folder_name)
            self.create_folder_widget.line_edit.clear()
        
        self.newFolderSQL()

        self.hide()

    # tạo table sql
    def newFolderSQL(self):
        item = [self.widgets.ComboboxFile.itemText(i) for i in range(self.widgets.ComboboxFile.count())]
        msg = Notification(self.widgets.centralwidget) 
        if self.folder_name in item:
            msg.SendMsg(
                ("Tên đã tồn tại !",       0)
                )
            return
        if self.folder_name == "":
            msg.SendMsg(
                ("Tên không thể bỏ trống !",       0)
                )
            return
        success = SubjectSQL.CreateTableNew(self, name= self.folder_name ,widgets=self.widgets)

        # /////////////////////////////////////////////
        SubjectProcessFile.LoadNameTabelSQL(self , self.widgets)
        if success:
            self.widgets.TableManage.clear()
            # tạo mới horizon
            QTableTools.SubjectNewHorizontalHeader(self , self.widgets)


            QTableTools.SubjectHiddenColumn(self , self.widgets)

            #######################################################################################
            # giới hạn chiều rộng của cột
            QTableTools.SetColumnWidthTableWidget(self , self.widgets)
            self.widgets.ComboboxFile.setCurrentText(self.folder_name)
