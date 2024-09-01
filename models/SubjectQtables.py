from main import *
from . SubjectScrips import *
from . SubjectNotifications import *
from . sql import *
index_name = {"c_user":2,"status":3,"work":4,"proxy":5,"message":6,"password":7,"code":8,"cookie":9,"access_token":10,"email":11,"passemail":12,"user-agent":13}
headers = ['','#', 'UID', 'Trạng thái', 'Kịch Bản', 'Proxy', 'Tin nhắn', 
                'Mật Khẩu', '2FA', 'Cookie', 'FB.token', 'Mail', 'password.mail', 
                'User Agent', 'Hoạt động']


# ///////////////////////////////////////
# xử lý dữ liệu
class DataGenerator(QThread):
    data_signal = pyqtSignal(list)

    def __init__(self, total_items, batch_size, current_batch, data , parent=None):
        super().__init__(parent)
        self.total_items = total_items
        self.batch_size = batch_size
        self.current_batch = current_batch
        self.data  = data
    def run(self):
        start_index = self.current_batch * self.batch_size

        print("SATRT :",start_index)
        end_index = min(start_index + self.batch_size, self.total_items)
        data_batch = []
        for i in range(start_index, end_index):

            if len(data_batch) == 100:break
            try:
                data_batch.append(self.data[i])
            except:break
        self.data_signal.emit(data_batch)
          


class QTableTools(WindowInterface):

    # bỏ chọn
    def UnCheckbox(self , widgets):
        for row in range(widgets.TableManage.rowCount()):
            widgets.TableManage.item(row, 0).setCheckState(False)
        
        widgets.label_select.setText("(0)")
        widgets.label_running.setText("(0)")

    def ChangeAccount(self , widgets , obj , code):
        # Cập nhật trạng thái tài khoản
        if code:
            color =  QColor(64, 191, 128)
            text =  "LIVE"
            SQL(obj['SQL']).SQLUpdateDataFromKey({'key':'status','content':'LIVE','id':obj['uid']})
        else:
            text =  "DIE"
            color =  QColor(255, 84, 135) # color die
            SQL(obj['SQL']).SQLUpdateDataFromKey({'key':'status','content':'DIE','id':obj['uid']})

        # cập nhật hiển thị trạng thái
        item_category = QTableTools.SubjectItemsText(
                self, text=text, color=color, size_font=8)
        if code:
            item_category.setIcon(QIcon(r".\icons\png\icons8-dot-24_live.png"))
        else:
            item_category.setIcon(QIcon(r".\icons\png\icons8-dot-24_red.png"))
        widgets.TableManage.setItem(obj['row'], 3, item_category)
    def CopyColumnContentDoubleClick(self, widgets ,row , column):
        if column == 2:
            # Lấy nội dung của ô
            item = widgets.TableManage.item(row, column)
            if item:
                text = item.text()
                
                # Sao chép nội dung vào clipboard
                clipboard = QApplication.clipboard()
                clipboard.setText(text)
                msg = Notification(self)
                msg.SendMsg(("Sao chép thành công !",1))
    def SetColumnWidthTableWidget(self,widgets):
        widgets.TableManage.setColumnWidth(0, 30)  # -> vị trí CHECKBOX
        widgets.TableManage.setColumnWidth(1, 70)  # -> vị trí ID COUNT
        widgets.TableManage.setColumnWidth(3, 90)  # -> vị trí STATUS
        widgets.TableManage.setColumnWidth(2, 150)  # -> vị trí UID COUNT
        widgets.TableManage.setColumnWidth(9, 250) # -> vị trí Cookie
        widgets.TableManage.setColumnWidth(6, 100) # -> vị trí Message
    # /////////////////////////////////////
    # phần này thêm các horizontalHeader vào cho bảng 
    def HandleScroll(self,scrollbar , data):
        max_scroll_value = scrollbar.maximum()
        current_scroll_value = scrollbar.value()

        if current_scroll_value == max_scroll_value:

            # ////////////////////////////////
            # load thêm dữ liệu data có điều kiện
            self.ProcessingQThreadDataItemsCondition(data=data)
    def handle_header_clicked(self, logicalIndex , widgets):
        if logicalIndex == 0:
            all_checked = True
            for row in range(widgets.TableManage.rowCount()):
                if widgets.TableManage.item(row, 0).checkState() == Qt.Unchecked:
                    all_checked = False
                    break
            for row in range(widgets.TableManage.rowCount()):
                widgets.TableManage.item(row, 0).setCheckState(Qt.Checked if not all_checked else Qt.Unchecked)

    
    def SubjectHiddenColumn(self , widgets):
        widgets.TableManage.setColumnHidden(7,True)
        widgets.TableManage.setColumnHidden(9,True)
        widgets.TableManage.setColumnHidden(8,True)
        widgets.TableManage.setColumnHidden(10,True)
        widgets.TableManage.setColumnHidden(11,True)
        widgets.TableManage.setColumnHidden(12,True)
        widgets.TableManage.setColumnHidden(13,True)

    # ///////////////////////////////////////
    # tạo item text 
    def SubjectItemsText(self , text , color , size_font):

        item = QTableWidgetItem(text)
        font = QFont('MesloLGLDZ Nerd Font',size_font)
        font.setBold(True)
        item.setFont(font)
        # ///////////////////////////
        # màu của chữ
        item.setForeground(color) 
        # ////////////////////////////
        item.setBackground(QColor(38, 49, 98))
        item.setTextAlignment(Qt.AlignCenter | Qt.AlignLeft | Qt.AlignVCenter)
        return item
    


    # /////////////////////////////////////
    # tạo header text ảo
    def SubjectNewHorizontalHeader(self , widgets):
        global headers
        widgets.TableManage.setColumnCount(len(headers))
        widgets.TableManage.setRowCount(0)  # Xóa tất cả các dòng

        widgets.TableManage.horizontalHeader().setStretchLastSection(True)
        # Thay thế tiêu đề cột đầu tiên bằng một widget tùy chỉnh có checkbox
        header_widget = HeaderCheckboxWidget('')  # Tiêu đề trống cho checkbox
        header_view = widgets.TableManage.horizontalHeader()

        # Option 2: Manually setting geometry
        header_widget.setParent(header_view)
        # ///////////////////////////////////////
        header_widget.setGeometry(4.3, -2, 43, 50)  # tọa độ checkbox căn giữa

        # Cập nhật tiêu đề cho các cột còn lại
        for i, text in enumerate(headers, start=0):
            item = QTableWidgetItem(text)
            font = QFont('Montserrat', 12)
            font.setBold(True)
            item.setFont(font)
            item.setForeground(QColor(163, 163, 194))
            item.setBackground(QColor(255, 255, 255, 255))
            item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            widgets.TableManage.setHorizontalHeaderItem(i, item)

            # Tính toán chiều rộng của cột dựa trên nội dung của cell
            metrics = QFontMetrics(font)
            width = metrics.horizontalAdvance(text) + 50

            widgets.TableManage.setColumnWidth(i, width)  # -> vị trí CHECKBOX
        
    # ////////////////////////////////////////////
    # add hiệu ứng selection cho table widget

    def AddSelectionItems(self, widgets):
        widgets.TableManage.setItemDelegate(ColorDelegate())
        widgets.TableManage.setSelectionBehavior(QTableWidget.SelectRows)

    # ///////////////////////////////
    # xóa hiêu ứng focus khi người dùng nhấn vào ô sẽ hiện 1 vòng ô slide box xung quanh ô đó
    def remove_focus(self, widgets):
        widgets.setFocusPolicy(Qt.NoFocus)
    
    # ////////////////////////////////
    # //////////////////////////////////////////////////////////
    # thêm dữ liệu từ mảng vào bảng
    # [{}...]

    # /////////////////////////
    #tạo checkbox table
    def CheckboxNew(self):
        checkbox = QTableWidgetItem()
        checkbox.setCheckState(Qt.Checked)
        checkbox.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
        checkbox.setCheckState(Qt.CheckState.Unchecked)
        checkbox.setForeground(QBrush(QColor("#00C2A8")))
        # # //////////////////////////
        # # hàm này căn chỉnh text ở giữa
        checkbox.setTextAlignment(Qt.AlignCenter)
        return checkbox

# /////////////////////////////////////////
# checkbox
class CheckBoxHeader(QHeaderView):
    def __init__(self, orientation, parent=None):
        super(CheckBoxHeader, self).__init__(orientation, parent)
        self.isOn = False

    def paintSection(self, painter, rect, logicalIndex):
        painter.save()
        super(CheckBoxHeader, self).paintSection(painter, rect, logicalIndex)
        painter.restore()

        if logicalIndex == 0:  # Chỉ thêm checkbox vào cột đầu tiên
            option = QStyleOptionButton()
            # Căn giữa checkbox
            option.rect = QRect(
                rect.x() + (rect.width() - 20) // 2, 
                rect.y() + (rect.height() - 20) // 2, 
                20, 20
            )
            option.state = QStyle.State_Enabled | QStyle.State_Active
            if self.isOn:
                option.state |= QStyle.State_On
            else:
                option.state |= QStyle.State_Off
            self.style().drawControl(QStyle.CE_CheckBox, option, painter)

    def mousePressEvent(self, event):
        index = self.logicalIndexAt(event.pos())
        if index == 0:
            self.isOn = not self.isOn
            self.updateSection(0)
        super(CheckBoxHeader, self).mousePressEvent(event)
    

# /////////////////////////////////
# click chuột select color 1 dòng
class ColorDelegate(QStyledItemDelegate):
    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        # change highlight color of cells in table
        color = QColor(255,255,255 )
        option.palette.setColor(QPalette.Highlight, color)
        QStyledItemDelegate.paint(self, painter, option, index)
        QStyledItemDelegate.paint(self, painter, option, index)
        # Hide the border of the selected cell in qtablewidget
        itemOption = QStyleOptionViewItem(option)
        if option.state & QStyle.State_HasFocus:
            itemOption.state = itemOption.state ^ QStyle.State_HasFocus
        super().paint(painter, itemOption, index)


# //////////////////////////////
# tạo ô checkbox cho tablewidget
class HeaderCheckboxWidget(QWidget):
    def __init__(self, label, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()
        self.checkbox = QCheckBox()
        self.checkbox.stateChanged.connect(self.__all__checkbox)
        self.label = QLabel(label)
        # /////////////////////
        # chỉnh màu cho cùng với màu của các header
        # phần còn lại các cột khác ở trong css TableManage
        self.setStyleSheet("""               
            background-color: rgb(38, 49, 98);
            border-radius:5px;
                           """)
        layout.addWidget(self.checkbox)
        layout.addWidget(self.label)
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)
        self.setFixedHeight(31)  # Đặt chiều cao cố định cho widget header

    def setCheckState(self, state):
        self.checkbox.setCheckState(state)

    def checkState(self):
        return self.checkbox.checkState()
    
    def __all__checkbox(self):
        print("ok")
    


class RoundedBorderDelegate(QStyledItemDelegate):
    def __init__(self,  parent , color , bold):
        super(RoundedBorderDelegate, self).__init__(parent)
        self.color = color
        self.bold = bold

    def paint(self, painter, option, index):
        painter.save()
        
        # Clip the painting region to the cell
        painter.setClipRect(option.rect)

        # Get the text and icon from the index
        text = index.data(Qt.DisplayRole)
        icon = index.data(Qt.DecorationRole)

        # Set the font
        font = QFont('Roboto', 8)
        if self.bold:
            font.setBold(True)
        painter.setFont(font)

        # Calculate font metrics
        font_metrics = QFontMetrics(font)
        text_width = font_metrics.width(text)
        text_height = font_metrics.height()

        # Set padding and icon size
        padding = 5
        icon_size = 12
        spacing = 3
        rect_width = text_width + 2 * padding + (icon_size if icon else 0) + (spacing if icon else 0)
        rect_height = text_height + padding

        # Center the rectangle within the cell
        rect_x = option.rect.x() + (option.rect.width() - rect_width) / 2
        rect_y = option.rect.y() + (option.rect.height() - rect_height) / 2

        # Ensure the rectangle does not exceed the cell width
        rect_width = min(rect_width, option.rect.width())

        # Define the rectangle for the rounded border
        rect = QRect(rect_x, rect_y, rect_width, rect_height)

        # Draw the rounded rectangle
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(self.color))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, 8, 8)

        # Draw the icon if present
        if icon:
            icon_rect = QRect(rect.left() + padding, rect.top() + (rect_height - icon_size) / 2, icon_size, icon_size)
            icon.paint(painter, icon_rect)

        # Draw the text
        text_rect_x = rect.left() + padding + (icon_size if icon else 0) + (spacing if icon else 0)
        text_rect = QRect(text_rect_x, rect.top(), rect_width - padding - (icon_size if icon else 0) - (spacing if icon else 0), rect_height)
        painter.setPen(QColor(255, 255, 255))
        painter.drawText(text_rect, Qt.AlignVCenter, text)

        painter.restore()

    def sizeHint(self, option, index):
        font = QFont('Roboto', 8)
        if self.bold:
            font.setBold(True)
        font_metrics = QFontMetrics(font)
        text = index.data(Qt.DisplayRole)
        text_width = font_metrics.width(text)
        text_height = font_metrics.height()
        padding = 5
        icon_size = 12 if index.data(Qt.DecorationRole) else 0
        spacing = 3 if icon_size else 0
        return QSize(text_width + 2 * padding + icon_size + spacing, text_height + padding)
    
# tạo qmenu xóa shadow
class CustomMenu(QMenu):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Tắt bóng của QMenu
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
    def showEvent(self, event):
        super().showEvent(event)
        self.setStyleSheet(QMenuRighClickTable)


class CustomHeaderHorizontal(QHeaderView):
    def __init__(self, parent=None):
        super(CustomHeaderHorizontal, self).__init__(Qt.Horizontal, parent)
        
        # Create a QToolButton for the menu
        self.menu_button = QToolButton(self)
        self.menu_button.setIcon(QIcon('./icons/png/icons8-menu-67.png'))  # Path to your menu icon
        self.menu_button.setPopupMode(QToolButton.InstantPopup)

        # Set the button to have a transparent background
        self.menu_button.setStyleSheet("background: transparent; border: none;")

        # Create a QMenu and add actions
        contextMenu = CustomMenu(self)
        font = QFont("blood",8)
        font.setBold(True)
        contextMenu.setFont(font)
        contextMenu.addAction("Đóng toàn bộ", self.option1)
        contextMenu.addAction("Chỉnh sửa", self.option2)
        contextMenu.setMinimumWidth(150)
        contextMenu.setMaximumWidth(150)
        self.menu_button.setMenu(contextMenu)

        # Set button position and size
        self.menu_button.setGeometry(10, 5, 30, 30)  # Adjust as needed

    def option1(self):
        print("Option 1 selected")

    def option2(self):
        print("Option 2 selected")

    def resizeEvent(self, event):
        super(CustomHeaderHorizontal, self).resizeEvent(event)
        # Adjust the button position if needed
        self.menu_button.move(self.width() - self.menu_button.width() - 5, (self.height() - self.menu_button.height()) // 2)

    def paintSection(self, painter, rect, logicalIndex):
        painter.save()
        painter.fillRect(rect, QColor(200, 200, 200))  # Adjust the color as needed
        painter.setPen(Qt.NoPen)
        painter.restore()
        super(CustomHeaderHorizontal, self).paintSection(painter, rect, logicalIndex)

