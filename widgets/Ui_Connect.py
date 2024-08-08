from main import *
from PyQt5.QtWidgets import QMainWindow
import sys , io
from models import *
class CustomWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setMask(self.create_rounded_rect_mask(self.rect(), 10))

    def create_rounded_rect_mask(self, rect, radius):
        path = QPainterPath()
        rectF = QRectF(rect)  # Convert QRect to QRectF
        path.addRoundedRect(rectF, radius, radius)
        region = QRegion(path.toFillPolygon().toPolygon())
        return region
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        
        # Create a path for the window's background
        path = QPainterPath()
        rect = QRectF(0, 0, self.width(), self.height())
        path.addRoundedRect(rect, 10, 10)
        
        # Draw the window's background
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setBrush(QBrush(QColor(255, 255, 255)))  # Background color
        painter.drawPath(path)
        
        # Draw the border
        border_color = QColor(177, 21, 74)  # Red color
        border_width = 5  # Width of the border
        
        # Create a path for the border
        border_path = QPainterPath()
        border_rect = rect.adjusted(border_width // 2, border_width // 2, -border_width // 2, -border_width // 2)
        border_path.addRoundedRect(border_rect, 10, 10)
        
        # Set up the pen for the border
        border_pen = QPen(border_color, border_width)
        painter.setPen(border_pen)
        painter.setBrush(Qt.NoBrush)
        
        # Draw the border
        painter.drawPath(border_path)
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
        self.windows.setWindowFlags(Qt.FramelessWindowHint| Qt.WindowStaysOnTopHint)
        self.windows.setAttribute(Qt.WA_TranslucentBackground)

        # /////////////
        # tắt thao tác trên giao diện chính
        self.windows.setWindowModality(Qt.ApplicationModal)
        self.widgets.centralwidget.setStyleSheet("border-radius:5px; background-color: white;")
        self.resize = Resize(self.windows)
        self.windows.mousePressEvent = self.mousePressEvent  # Override mousePressEvent
        self.windows.mouseReleaseEvent = self.mouseReleaseEvent  # Override mouseReleaseEvent
        self.windows.mouseMoveEvent = self.mouseMoveEvent  # Override mouseMoveEvent
        self.windows.setMask(self.windows.create_rounded_rect_mask(self.windows.rect(), 10))  # Call create_rounded_rect_mask
        self.windows.show()


        return self.widgets, self.windows

    def create_rounded_rect_mask(self, rect, radius):
        path = QPainterPath()
        path.addRoundedRect(rect, radius, radius)
        region = QRegion(path.toFillPolygon().toPolygon())
        return region
    

    def paintEvent(self, event):
        painter = QPainter(self)
        path = QPainterPath()
        radius = 10  # Bán kính cạnh tròn
        

        
        # Vẽ hình chữ nhật với bán kính cạnh tròn
        path.addRoundedRect(self.rect(), radius, radius)
        
        # Vẽ nền của cửa sổ
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.fillPath(path, QBrush(QColor(255, 255, 255)))
        
        # Vẽ viền tròn quanh hình chữ nhật
        pen = painter.pen()
        pen.setColor(QColor(177, 21, 74))
        pen.setWidth(2)  # Đặt độ dày của viền
        painter.setPen(pen)
        
        # Vẽ đường viền xung quanh path đã vẽ
        painter.drawPath(path)
    def resizeEvent(self, event):
        super().resizeEvent(event)
        rect = widgets.centralwidget.rect()
        grip_width = 7  # Độ rộng của EdgeGrip
        self.left_grip.setGeometry(0, 0, grip_width, rect.height())
        self.right_grip.setGeometry(rect.width() - grip_width, 0, grip_width, rect.height())
        self.top_grip.setGeometry(0, 0, rect.width(), grip_width)
        self.bottom_grip.setGeometry(0, rect.height() - grip_width, rect.width(), grip_width)

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
    