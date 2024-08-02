import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPainterPath, QRegion

class CustomWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom Window")
        self.setFixedSize(400, 300)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background-color: white;")
        
        # Set rounded corners
        self.setMask(self.create_rounded_rect_mask(self.rect(), 10))
        

    def create_rounded_rect_mask(self, rect, radius):
        path = QPainterPath()
        rectF = QRectF(rect)  # Convert QRect to QRectF
        path.addRoundedRect(rectF, radius, radius)
        region = QRegion(path.toFillPolygon().toPolygon())
        return region

class Ui_Connect:
    def __init__(self):
        self.windows = None
        self.widgets = None

    def show_ui(self, Ui):
        self.windows = CustomWindow()  # Use CustomWindow instead of QMainWindow
        self.widgets = Ui()
        self.widgets.setupUi(self.windows)
        
        # Đặt các thuộc tính cho cửa sổ
        self.windows.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.windows.setAttribute(Qt.WA_TranslucentBackground)
        self.widgets.centralwidget.setStyleSheet("border-radius:5px; background-color: white;")
        self.resize = Resize(self.windows)
        self.windows.mousePressEvent = self.mousePressEvent  # Override mousePressEvent
        self.windows.mouseReleaseEvent = self.mouseReleaseEvent  # Override mouseReleaseEvent
        self.windows.mouseMoveEvent = self.mouseMoveEvent  # Override mouseMoveEvent
        self.windows.setMask(self.windows.create_rounded_rect_mask(self.windows.rect(), 10))  # Call create_rounded_rect_mask
        self.windows.show()
        return self.widgets, self.windows

class Resize:
    def __init__(self, window):
        self.window = window
        self.window.installEventFilter(self)
        self.is_resizing = False

    def eventFilter(self, obj, event):
        # Add your resizing logic here
        return super().eventFilter(obj, event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = Ui_Connect()
    class Ui:
        def setupUi(self, MainWindow):
            MainWindow.setObjectName("MainWindow")
            MainWindow.resize(800, 600)
            self.centralwidget = QWidget(MainWindow)
            self.centralwidget.setObjectName("centralwidget")
            MainWindow.setCentralWidget(self.centralwidget)
    ui = Ui()
    main_window.show_ui(ui)
    sys.exit(app.exec_())
