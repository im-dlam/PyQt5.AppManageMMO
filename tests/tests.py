import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPainter, QBrush
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget

class ShadowWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background:transparent;")

    def paintEvent(self, event):
        # Vẽ bóng mờ mỏng chỉ 1px
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        shadow_color = QColor(21,76,12)  # Đặt màu bóng
        painter.setBrush(QBrush(shadow_color))
        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 20, 20)  # Điều chỉnh kích thước 1px

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Kích thước cửa sổ chính
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: white; border-radius: 10px;")
        
        # Tạo ShadowWindow
        self.shadow_window = ShadowWindow(self)
        self.shadow_window.setGeometry(self.geometry().adjusted(-1, -1, 1, 1))  # Điều chỉnh viền bóng nhỏ hơn
        self.shadow_window.show()
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.shadow_window.setGeometry(self.geometry().adjusted(-1, -1, 1, 1))

    def moveEvent(self, event):
        super().moveEvent(event)
        self.shadow_window.move(self.x() - 1, self.y() - 1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
