from . SubjectScrips import QMenuRighClick , QMenuProfile
from main import *
from models import *
from models.sql.SQLModules import *
import os 
widgets , window_widgets , msg = None , None , None
contextMenu = None
class CustomMenu(QMenu):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Tắt bóng của QMenu
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
    def showEvent(self, event):
        super().showEvent(event)
        self.setStyleSheet(QMenuProfile)

class CustomMenuProfile(QMenu):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Tắt bóng của QMenu
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
    def showEvent(self, event):
        super().showEvent(event)
        self.setStyleSheet(QMenuRighClick)
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

        # //////////////////////////
        # Khỏi chạy tài khoản
        self.NewActionQMenu(
            dir=f"{your_dir}/icons8-run-command-26.png",
            text="Run Now",
            subject=self.SubjectNewFolder
            )
        
        # //////////////////////////
        contextMenu.addSeparator()
        # //////////////////////////

        font = QFont("Montserrat",7)
        font.setBold(True)
        # //////////////////////////
        # Menu hiển thị con
        MenuShow =  CustomMenu(self)
        MenuShow.setTitle("Hiển thị")
        MenuShow.setIcon(QIcon(f"{your_dir}/icons8-eye-24.png"))
        MenuShow.addAction("Live")
        MenuShow.addAction("Die")
        MenuShow.setStyleSheet(QMenuRighClick)
        MenuShow.setFont(font)
        contextMenu.addMenu(MenuShow)
        # ///////////////////////////////////////
        contextMenu.addSeparator()


        # //////////////////////////
        # Menu coppy . delete
        MenuShow =  CustomMenu(self)
        MenuShow.setTitle("Copy")
        MenuShow.setIcon(QIcon(f"{your_dir}/icons8-copy-48.png"))
        MenuShow.addAction("UID")
        MenuShow.addAction("Password")
        MenuShow.addAction("UID|PassWord|2FA")
        MenuShow.addAction("Cookie")
        MenuShow.addAction("Token")
        MenuShow.addAction("Thêm ...")
        MenuShow.setStyleSheet(QMenuRighClick)
        MenuShow.setFont(font)
        contextMenu.addMenu(MenuShow)

        # ///////////////////////////
        self.NewActionQMenu(
            dir=f"{your_dir}/icons8-close-26.png",
            text="Xóa Tài khoản này",
            subject=self.SubjectNewFolder
            )
        font = QFont("Montserrat",8)
        font.setBold(True)
        contextMenu.setFont(font)
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
