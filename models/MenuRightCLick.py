from .SubjectScrips import QMenuRighClick , QMenuProfile
from main import *
from models import *
from models.sql.SQLModules import *
import os , ctypes
widgets , window_widgets , msg = None , None , None
contextMenu = None
class CustomMenuStyle(QProxyStyle):
    def pixelMetric(self, metric, option=None, widget=None):
        if metric == QStyle.PM_SubMenuOverlap:
            return 10  # Adjust this value to control the distance
        return super().pixelMetric(metric, option, widget)
class CustomMenu(QMenu):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Tắt bóng của QMenu
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
    def showEvent(self, event):
        super().showEvent(event)
        self.setStyleSheet("""

QMenu {
    padding-left:5px;
    padding-right:5px;
    padding-top:3px;
    padding-bottom:3px;
    background-color:#242e5d;
    border: 0.5px solid rgb(65,84,133); /* Đường viền cho menu */
    border-radius: 5px; /* Làm tròn viền cho menu */
    color: #d0d4db;
    font-family: bold;
}
QMenu::item {
        min-height: 12px;  /* Adjust the height of each menu item */
        min-width: 100px;  /* Adjust the width of each menu item */
        padding: 5px;     /* Add padding around the text */
        color: #d0d4db; /* Màu chữ cho các mục menu */
        border-radius: 3px; /* Làm tròn viền cho các mục menu */
        font-family: bold;
    }

QMenu::item:selected {
    background-color:#313C71; /* Màu nền khi mục được chọn */
    color: #d0d4db;
    border-radius: 2px; /* Làm tròn viền cho menu */
    font-family: bold;

}
QAction#ActionOtherCopy {
    color: #520066; /* Màu chữ đỏ cho action "Thêm..." */
        }
QMenu::separator {
        height: 1px;
        background: #526296;
        margin: 1px 3px 1px 3px;
                           
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

class CustomMenuProfile(QMenu):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Tắt bóng của QMenu
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
    def showEvent(self, event):
        super().showEvent(event)
        self.setStyleSheet(QMenuProfile)
class FrameRightClick(QFrame):
    def __init__(self, widgets_, parent=None):
        super().__init__(parent)
        global widgets , msg
        widgets = widgets_
        widgets.TableManage.setContextMenuPolicy(Qt.CustomContextMenu)
        widgets.TableManage.customContextMenuRequested.connect(self.showContextMenu)
        msg = Notification(widgets.centralwidget) 

    def NewActionQMenu(self , dir , text , subject: object):
        global contextMenu
        content = QAction(QIcon(dir),text, self)
        content.triggered.connect(subject)
        contextMenu.addAction(content)
    def showContextMenu(self, position):
        global contextMenu , widgets
        your_dir = os.getcwd() + "/icons/png"
        contextMenu = CustomMenu(self)
        contextMenu.setStyle(CustomMenuStyle())

        # //////////////////////////
        # Khỏi chạy tài khoản
        self.NewActionQMenu(
            dir=f"",
            text="Giải Checkpoint 956",
            subject=self.SubjectNewFolder
            )
        self.NewActionQMenu(
            dir=f"",
            text="Giải Checkpoint 282",
            subject=self.SubjectNewFolder
            )
        # //////////////////////////
        contextMenu.addSeparator()

        self.NewActionQMenu(
            dir=f"",
            text="Mở Browser",
            subject=self.SubjectNewFolder
            )
        # //////////////////////////


        contextMenu.setMinimumWidth(250)
        contextMenu.setMaximumWidth(250)
        contextMenu.exec_(widgets.TableManage.mapToGlobal(position))



    # ////////////////////////////////
    # GUI tạo danh mục
    def SubjectNewFolder(self):
        global window_widgets
        window_widgets , windows_ui = Ui_Connect.show_ui(self, Ui_CreateFolder)
        window_widgets.pushButton.clicked.connect(self.CreateFolder)
        window_widgets.pushButton.clicked.connect(lambda:windows_ui.close())
        window_widgets.btn_close.clicked.connect(lambda:windows_ui.close())
        windows_ui.show()

    # ///////////////////////////
    # GUI xóa danh mục
    def CreateFolder(self):
        global msg
        NameText = window_widgets.lineEdit.text()
        if NameText == "":
            msg.SendMsg(
                ("Tên không thể bỏ trống !",       0)
                )
            return
        success = SubjectSQL.CreateTableNew(self, name= NameText ,widgets=widgets)

        # /////////////////////////////////////////////
        SubjectProcessFile.LoadNameTabelSQL(self , widgets)
        if success:
            widgets.TableManage.clear()
            # tạo mới horizon
            QTableTools.SubjectNewHorizontalHeader(self , widgets)


            QTableTools.SubjectHiddenColumn(self , widgets)

            #######################################################################################
            # giới hạn chiều rộng của cột
            QTableTools.SetColumnWidthTableWidget(self , widgets)
            widgets.ComboboxFile.setCurrentText(NameText)


    def _on_resize(self, event):
        global msg
        msg.move_notification()
        QMainWindow.resizeEvent(self, event)
