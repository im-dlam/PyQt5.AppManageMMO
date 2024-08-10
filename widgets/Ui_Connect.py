from main import *
from PyQt5.QtWidgets import QMainWindow
import sys , io
from models import *
class CustomWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_TranslucentBackground)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Màu của bóng mờ
        shadow_color = QColor(0, 0, 0, 160)
        painter.setBrush(QBrush(shadow_color))

        # Tạo một hình chữ nhật bao quanh cửa sổ với bóng mờ 1px
        rect = self.rect().adjusted(1, 1, -1, -1)
        painter.drawRoundedRect(rect, 10, 10)

        # Vẽ một hình chữ nhật để kiểm tra mask
        painter.setBrush(QBrush(Qt.red))  # Đặt màu nền tạm thời là đỏ
        painter.drawRect(self.rect())

        super().paintEvent(event)

    def create_rounded_rect_mask(self, rect, radius):
        path = QPainterPath()
        rect_f = QRectF(rect)  # Chuyển đổi QRect sang QRectF
        path.addRoundedRect(rect_f, radius, radius)
        region = QRegion(path.toFillPolygon().toPolygon())
        return region


class Overlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setGeometry(parent.rect())
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(27,165,148,20))
    
class Ui_Connect(QMainWindow):
    def __init__(self):
        super().__init__()
        self.windows = None
        self.widgets = None

    def show_ui(self, Ui):
        self.windows = CustomWindow()
        self.widgets = Ui()
        self.widgets.setupUi(self.windows)

        # Đặt các thuộc tính cho cửa sổ


        # /////////////
        # tắt thao tác trên giao diện chính
        self.windows.setWindowModality(Qt.ApplicationModal)
        self.resize = Resize(self.windows)
        self.windows.mousePressEvent = self.mousePressEvent  # Override mousePressEvent
        self.windows.mouseReleaseEvent = self.mouseReleaseEvent  # Override mouseReleaseEvent
        self.windows.mouseMoveEvent = self.mouseMoveEvent  # Override mouseMoveEvent
        self.windows.setMask(self.windows.create_rounded_rect_mask(self.windows.rect(), 10))  # Call create_rounded_rect_mask
        # Tạo ShadowWindow và thiết lập vị trí, kích thước

        self.windows.show()

        return self.widgets, self.windows


    

  
    def resizeEvent(self, event):
        super().resizeEvent(event)

    def mousePressEvent(self, event):
        self.resize.mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.resize.mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        self.resize.mouseMoveEvent(event)

class Resize:
    def __init__(self, window):
        self.window = window
        self.resizing = False
        self.moving = False
        self.margin = 10
        self.oldPos = QPoint()
        self.window.setMouseTracking(True)
        self.custom_cursor = QCursor(QPixmap("./icons/png/mouse.png").scaled(32, 32))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos()
            rect = self.window.rect()
            pos = self.window.mapFromGlobal(self.oldPos)

            if pos.x() < self.margin or pos.x() > rect.width() - self.margin or pos.y() < self.margin or pos.y() > rect.height() - self.margin:
                self.resizing = True
            else:
                self.moving = True

    def mouseReleaseEvent(self, event):
        self.resizing = False
        self.moving = False

    def mouseMoveEvent(self, event):
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

    def moveWindow(self, globalPos):
        diff = globalPos - self.oldPos
        new_pos = self.window.pos() + diff
        self.window.move(new_pos)
        self.oldPos = globalPos
class Functions_Scripts:
    @staticmethod
    def scripts_run(scripts):
        msg , vars = {} , {}
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        # try:
        exec(scripts,vars,msg)
        # output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        return msg
        # except Exception as error:
        #     print(error)
        #     return None
    