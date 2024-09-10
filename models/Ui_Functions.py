from main import *
from PyQt5.QtMultimedia import QSound 
from . SubjectTools import *
import json , pathlib
_combox_item = ["","c_user","password","code","cookie","access_token","email","passemail","user-agent","proxy","mailkp","passmailkp","phone","birthday"]

# /////////////////////////////
# tạo thanh thông báo tin nhắn ẩn hiện

class Search(QThread):
    def __init__(self,widgets, searchText ,parent=None) -> None:
        super().__init__(parent)
        self.widgets = widgets
        self.searchText = searchText
    def run(self  ):
        self.search()

        self.quit()
    def search(self):
        for row in range(self.widgets.TableManage.rowCount()):
            match = False
            try:
                for col in range(self.widgets.TableManage.columnCount()):
                    item = self.widgets.TableManage.item(row, col)
                    if item and self.searchText in item.text().lower():
                        match = True
                        break
                self.widgets.TableManage.setRowHidden(row, not match)
            except Exception as KeyError:
                print(KeyError)
class Functions(WindowInterface):

    # ////////////////////////////////
    # cập nhật thông số tài khoản hiển thị

    def AnimatedToggleButton(self,FrameID):
        self.your_dir  = pathlib.Path.cwd().joinpath("models/json/config.json")
        filedumps = json.loads(open(self.your_dir,"r",encoding="utf-8").read())
        btn_list  = {
                "FrameID_ProfileLog":"id.Profile",
                "FrameID_Backup":"id.Backup",
                "FrameID_Proxy1":"id.Proxy",
                "FrameID_Proxy2":"id.Proxyauto",
                "FrameID_AutoSortSize":"id.BrowserAuto",
                "FrameID_BrowserOptimization":"id.BrowserOptimize",
                "FrameID_ContentChatGpt":"id.chatgpt",
                "FrameID_ChromeHeadless":"id.BrowserHeadless"
            }
        def ButtonConectUpdate(button):

            with open(self.your_dir,"r",encoding="utf-8") as r:
                filedumps = json.loads(r.read())
                r.close()

            filedumps['config'].update(
                {
                    btn_list[button.objectName()] : button.isChecked() 
                    }
                )
        
            with open(self.your_dir,"w",encoding="utf-8") as r:
                json.dump(
                    filedumps,
                    r,
                    indent=4,
                    ensure_ascii=0
                )
                r.close()
        for frame in FrameID:
            button = AnimatedToggle(
                    checked_color = "#6b7db3",
                    pulse_checked_color="#4040bf"
                )
            button.setMinimumSize(50,30)
            # thêm objectname
            button.setObjectName(frame.objectName())


            # thêm layout cho nút
            layout_button = QVBoxLayout()
            layout_button.addWidget(button)
            frame.setLayout(layout_button)
            button.setChecked(filedumps["config"][btn_list[frame.objectName()]])
            button.clicked.connect(lambda checked, btn=button: ButtonConectUpdate(btn))

    def UpdateLabelTotalAccount(self , widgets , total):
        widgets.label_total.setText(f"({str(total)})")


    def AnimationSwitchMenu(self , widgets):
        if widgets.frame_main_icons.width() == 100:
            widgets.frame_main_text.setMaximumSize(200,16777215)
            widgets.frame_main_icons.setMaximumSize(0,16777215)
        else:
            widgets.frame_main_icons.setMaximumSize(100,16777215)
            widgets.frame_main_text.setMaximumSize(0,16777215)


    # ////////////////////////////////////
    # phần này sử dụng để gọi âm thanh khi mở ứng dụng   
    def OpenSoundApp(self):
        sound = QSound("./icons/audio/open.wav")
        sound.play("./icons/audio/open.wav")

    # ////////////////////////////////////
    # phần này sử dụng âm thanh khi người dùng click vào các nút  
    def ButtonPlaySound(self, buttons):
        def sound():
            QSound.play('./icons/audio/button.wav')
            
        for button in buttons:
            button.clicked.connect(lambda:sound())
    
    
    # ////////////////////////////////////
    # ResizeMode dùng hoạt động khi người dừng nhấn vào nút phóng to (maximum)
    def ResizeMode(self, widgets):
        # ////////////////////
        # nếu full màn hình -> chuyển về trạng thái cửa sổ size ban đầu
        if self.isMaximized():
            self.showNormal()
            widgets.bgApp.setStyleSheet("""
                                QFrame#bgApp{
                                border-radius:7px;
                                border:2px solid #29356a;
                                }
                                QFrame#frame_main{
                                background-color:#263162;
                                border-radius:7px;
                                }
                                """)
        else:
            widgets.bgApp.setStyleSheet("""
                                QFrame#bgApp{
                                border-radius:0px;
                                border:2px solid #29356a;
                                }
                                QFrame#frame_main{
                                background-color:#263162;
                                border-radius:0px;
                                }
                                """)
            # //////////////////////////
            # maximum hoạt động phóng to màn hình app
            self.showMaximized()
            # /////////////////////////
            # tắt border viền trở về mặc định cạnh vuông
    

    # //////////////////////////////////
    # ShadowFrameConditional : functions \ nhận tham số : Object , QColor để làm hiệu ứng bóng mờ , thêm sinh động cho ứng dụng
    def ShadowFrameConditional(self , widgest_value , color):
        set_effect =  QGraphicsDropShadowEffect(self)
        set_effect.setBlurRadius(17)
        set_effect.setOffset(0,0)
        set_effect.setColor(color)
        set_effect.setXOffset(0)
        set_effect.setYOffset(0)
        widgest_value.setGraphicsEffect(set_effect)
    

    # ///////////////////////////////////////
    # SwitchButtonToolsCssChecked : sử dụng để tạo hiệu ứng nút thả khi người dùng click các nút ở cột menu , hoạt động luân phiên mình các nút đó 
    # Ex : btn_profile , btn_hide , btn_proxies ...
    def SwitchButtonToolsCssChecked(self  , buttons):
        def toggle_buttons(clicked_button):
            for button in buttons:
                if button == clicked_button:
                    button.setChecked(True)
                else:
                    button.setChecked(False)
        for button in buttons:
            button.setCheckable(True)
            button.clicked.connect(lambda checked, btn=button: toggle_buttons(btn))
    
    # ////////////////////////////////
    # phần này thêm hiệu ứng css hover cho các button và hiệu ứng checked khi nhấn . 
    # màu chủ đâọ là xanh nhạt hihi
    def SwitchButtonCssChecked(self  , buttons):
        def toggle_buttons(clicked_button):
            for button in buttons:
                if button == clicked_button:
                    button.setChecked(True)

                else:
                    button.setChecked(False)
        for button in buttons:
            button.setCheckable(True)
            button.clicked.connect(lambda checked, btn=button: toggle_buttons(btn))




    # //////////////////////////////
    # set icons profile
    def set_icons(self , widgets):
        script = """QPushButton{
                        border:none;
                        border-image: url(:/icons/png/e2537e3974afaef1f7be.jpg);
                        border-radius:5px;
                    }
                    QPushButton:hover{
                        border:none;
                        border-image: url(:/icons/png/e2537e3974afaef1f7be.jpg);
                        border-radius:5px;
                        border:0.5px solid #6b5fc3;
                    }
                    QPushButton::menu-indicator { image: none; }"""
        widgets.btn_profile.setStyleSheet(script)


    # ////////////////////////////// 
    # hàm này có tác dụng show các item lên các combobox ở phần hiển thị nhập dữ liệu tài khoản 
    def ComboboxProcessItem(self, widgets : object, line: str , data : hash):
        global _combox_item
        # string to split
        # ///////////////////////
        # data to hash {} , line to string
        line = line .split("|")
        combobox_ = [widgets.combox_1 , widgets.combox_2 , widgets.combox_3,
                     widgets.combox_4 , widgets.combox_5 , widgets.combox_6,
                     widgets.combox_7 , widgets.combox_8 , widgets.combox_9,
                     widgets.combox_10, widgets.combox_11, widgets.combox_12,
                     widgets.combox_13, widgets.combox_14
                     ] 
        
        for i , r in enumerate(_combox_item):
            combobox_[i].addItems(_combox_item)

        for  i , w in enumerate(line):
            for name_ in data:
                if w != "" and w == data[name_]:
                    combobox_[i].setCurrentText(name_)


    # /////////////////////////////////
    # phần này tác dụng khi người dùng nhấn ô checkbox đầu tiên sẽ tự động luân phiên đổi trạng thái 
    def AutoSwitchCheckboxStatus(self , widgets : object):

        def checkbox_clicked(row, column):
            status = 0
            if column == 0:
                checkbox_widget = widgets.TableManage.item(row, 0)
                if checkbox_widget:
                    if checkbox_widget.checkState():
                        checkbox_widget.setCheckState(Qt.CheckState.Unchecked)
                        status = 1
                    else:
                        checkbox_widget.setCheckState(Qt.CheckState.Checked)
                
            
        widgets.TableManage.cellClicked.connect(lambda row , colums,: checkbox_clicked(row , colums))
    

    

# ////////////////////////////////
# tạo icon khi di chuyển gần mép app
class EdgeGrip(QWidget):
    def __init__(self, parent, edge):
        super().__init__(parent)
        self.edge = edge
        if edge in (Qt.LeftEdge, Qt.RightEdge):
            self.setCursor(Qt.SizeHorCursor)
        elif edge in (Qt.TopEdge, Qt.BottomEdge):
            self.setCursor(Qt.SizeVerCursor)
        self.setMouseTracking(True)
# //////////////////////////////////
# sử dụng QThread để xử lý dữ liệu nhập -> trả về hàm on_processing_finished(str , Object) ở hàm main.py



# ///////////////////////////////////
# hàm này có trách nhiệm tự động căn chỉnh checkbox vào chính giữa cột ở bảng
class CheckBoxStyle(QProxyStyle):
    def subElementRect(self, element, option, widget=None):
        r = super().subElementRect(element, option, widget)
        if element == QStyle.SE_ItemViewItemCheckIndicator:
            r.moveCenter(option.rect.center())
        return r

# /////////////////////////////////////////
# hiệu ứng css thanh cuộn ở bảng khi di chuột vào sẽ có hiệu ứng hover
class CustomScrollBar(QScrollBar):
    def __init__(self, parent=None, orientation=Qt.Vertical):
        super().__init__(orientation, parent)
        self.setStyleSheet(self.default_style())

    def default_style(self):
        return """     
        """
    def hover_style(self):
        return """
            QScrollBar:horizontal {
                border: none;
                background: rgb(150, 173, 232);
                height: 7px;
                margin: 0px 0px 0 0px;
                border-radius: 5px;
            }
            QScrollBar::handle:horizontal {
                background-color: rgb(105, 122, 163);
                min-width: 10px;
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
                background: rgb(105, 122, 163);
                width: 7px;
                margin: 0px 0 0px 0;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background-color: rgb(150, 173, 232);
                min-height: 20px;
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
        """

    def enterEvent(self, event):
        self.setStyleSheet(self.hover_style())
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet(self.default_style())
        super().leaveEvent(event)
    # //////////////////////////////////////////////////
# xóa focus qcombobox

class NoFocusProxyStyle(QProxyStyle):
    def drawPrimitive(self, element, option, painter, widget):
        if element == QStyle.PE_FrameFocusRect:
            return  # Bỏ qua việc vẽ focus rectangle
        super().drawPrimitive(element, option, painter, widget)
# ///////////////////////////////////////////
# phần này tác dụng di chuyển ứng dụng , xóa các thanh status , menu mặc định
# kéo dãn khi khi dùng chuột ở các mép
# min size ở mặc định không quá 400,700 kéo nhỏ
class Resize:
    def __init__(self, window):
        self.window = window
        self.resizing = False
        self.moving = False
        self.margin = 10
        self.oldPos = QPoint()
        self.window.setMouseTracking(True)


        self.custom_cursor = QCursor(QPixmap("./icons/png/mouse.png").scaled(32, 32))

    # ////////////////////////////////////
    # phần này để kiểm tra chuột vào vùng mép để kéo
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos()
            rect = self.window.rect()
            pos = self.window.mapFromGlobal(self.oldPos)

            if pos.x() < self.margin or pos.x() > rect.width() - self.margin or pos.y() < self.margin or pos.y() > rect.height() - self.margin:
                self.resizing = True
            else:
                self.moving = True

    # ///////////////////////////////////////
    # phần này để đổi trạng thái 
    def mouseReleaseEvent(self, event: QMouseEvent):
        self.resizing = False
        self.moving = False

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton:
            if self.resizing:
                self.resizeWindow(event.globalPos())
            elif self.moving:
                self.moveWindow(event.globalPos())
        else:
            self.updateCursorShape(event.globalPos())
    


    def updateCursorShape(self, globalPos):
        rect = self.window.rect()
        margin = self.margin
        pos = self.window.mapFromGlobal(globalPos)

        if self.resizing:
            self.window.setCursor(self.custom_cursor)
        elif pos.x() < margin and pos.y() < margin:
            self.window.setCursor(QCursor(Qt.SizeFDiagCursor))
        elif pos.x() > rect.width() - margin and pos.y() > rect.height() - margin:
            self.window.setCursor(QCursor(Qt.SizeFDiagCursor))
        elif pos.x() < margin and pos.y() > rect.height() - margin:
            self.window.setCursor(QCursor(Qt.SizeBDiagCursor))
        elif pos.x() > rect.width() - margin and pos.y() < margin:
            self.window.setCursor(QCursor(Qt.SizeBDiagCursor))
        elif pos.x() < margin or pos.x() > rect.width() - margin:
            self.window.setCursor(QCursor(Qt.SizeHorCursor))
        elif pos.y() < margin or pos.y() > rect.height() - margin:
            self.window.setCursor(QCursor(Qt.SizeVerCursor))
        else:
            self.window.setCursor(QCursor(Qt.ArrowCursor))

    # /////////////////////////////////////////////////////////////////////
    # hiệu ứng kéo dãn ứng dụng
    def resizeWindow(self, globalPos):
        diff = globalPos - self.oldPos
        new_rect = self.window.geometry()

        if self.oldPos.x() < self.window.frameGeometry().left() + self.margin:
            new_rect.setLeft(new_rect.left() + diff.x())
        elif self.oldPos.x() > self.window.frameGeometry().right() - self.margin:
            new_rect.setRight(new_rect.right() + diff.x())
        if self.oldPos.y() < self.window.frameGeometry().top() + self.margin:
            new_rect.setTop(new_rect.top() + diff.y())
        elif self.oldPos.y() > self.window.frameGeometry().bottom() - self.margin:
            new_rect.setBottom(new_rect.bottom() + diff.y())

        self.window.setGeometry(new_rect)
        self.oldPos = globalPos

    # ///////////////////////////////////////////
    # hiệu ứng di chuyển ứng dụng ><
    def moveWindow(self, globalPos):
        diff = globalPos - self.oldPos
        new_pos = self.window.pos() + diff
        self.window.move(new_pos)
        self.oldPos = globalPos